# blukat - 3 pt

## 문제

```text
Sometimes, pwnable is strange...
hint: if this challenge is hard, you are a skilled player.

ssh blukat@pwnable.kr -p2222 (pw: guest)
```

## 풀이

코드는 다음과 같다.

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <fcntl.h>
char flag[100];
char password[100];
char* key = "3\rG[S/%\x1c\x1d#0?\rIS\x0f\x1c\x1d\x18;,4\x1b\x00\x1bp;5\x0b\x1b\x08\x45+";
void calc_flag(char* s){
        int i;
        for(i=0; i<strlen(s); i++){
                flag[i] = s[i] ^ key[i];
        }
        printf("%s\n", flag);
}
int main(){
        FILE* fp = fopen("/home/blukat/password", "r");
        fgets(password, 100, fp);
        char buf[100];
        printf("guess the password!\n");
        fgets(buf, 128, stdin);
        if(!strcmp(password, buf)){
                printf("congrats! here is your flag: ");
                calc_flag(password);
        }
        else{
                printf("wrong guess!\n");
                exit(0);
        }
        return 0;
}
```

디스어셈블한 `main` 함수를 보자.

```assembly
   0x00000000004007fa <+0>:     push   rbp
   0x00000000004007fb <+1>:     mov    rbp,rsp
   0x00000000004007fe <+4>:     add    rsp,0xffffffffffffff80
   0x0000000000400802 <+8>:     mov    rax,QWORD PTR fs:0x28
   0x000000000040080b <+17>:    mov    QWORD PTR [rbp-0x8],rax
   0x000000000040080f <+21>:    xor    eax,eax
   0x0000000000400811 <+23>:    mov    esi,0x40096a
   0x0000000000400816 <+28>:    mov    edi,0x40096c
   0x000000000040081b <+33>:    call   0x400660 <fopen@plt>
   0x0000000000400820 <+38>:    mov    QWORD PTR [rbp-0x78],rax
   0x0000000000400824 <+42>:    mov    rax,QWORD PTR [rbp-0x78]
   0x0000000000400828 <+46>:    mov    rdx,rax
   0x000000000040082b <+49>:    mov    esi,0x64
   0x0000000000400830 <+54>:    mov    edi,0x6010a0
   0x0000000000400835 <+59>:    call   0x400640 <fgets@plt>
   0x000000000040083a <+64>:    mov    edi,0x400982
   0x000000000040083f <+69>:    call   0x4005f0 <puts@plt>
   0x0000000000400844 <+74>:    mov    rdx,QWORD PTR [rip+0x200835]        # 0x601080 <stdin@@GLIBC_2.2.5>
   0x000000000040084b <+81>:    lea    rax,[rbp-0x70]
   0x000000000040084f <+85>:    mov    esi,0x80
   0x0000000000400854 <+90>:    mov    rdi,rax
   0x0000000000400857 <+93>:    call   0x400640 <fgets@plt>
   0x000000000040085c <+98>:    lea    rax,[rbp-0x70]
   0x0000000000400860 <+102>:   mov    rsi,rax
   0x0000000000400863 <+105>:   mov    edi,0x6010a0
   0x0000000000400868 <+110>:   call   0x400650 <strcmp@plt>
   0x000000000040086d <+115>:   test   eax,eax
   0x000000000040086f <+117>:   jne    0x4008a0 <main+166>
   0x0000000000400871 <+119>:   mov    edi,0x400996
   0x0000000000400876 <+124>:   mov    eax,0x0
   0x000000000040087b <+129>:   call   0x400620 <printf@plt>
   0x0000000000400880 <+134>:   mov    edi,0x6010a0
   0x0000000000400885 <+139>:   call   0x400786 <calc_flag>
   0x000000000040088a <+144>:   mov    eax,0x0
   0x000000000040088f <+149>:   mov    rcx,QWORD PTR [rbp-0x8]
   0x0000000000400893 <+153>:   xor    rcx,QWORD PTR fs:0x28
   0x000000000040089c <+162>:   je     0x4008b9 <main+191>
   0x000000000040089e <+164>:   jmp    0x4008b4 <main+186>
   0x00000000004008a0 <+166>:   mov    edi,0x4009b4
   0x00000000004008a5 <+171>:   call   0x4005f0 <puts@plt>
   0x00000000004008aa <+176>:   mov    edi,0x0
   0x00000000004008af <+181>:   call   0x400670 <exit@plt>
   0x00000000004008b4 <+186>:   call   0x400610 <__stack_chk_fail@plt>
   0x00000000004008b9 <+191>:   leave
   0x00000000004008ba <+192>:   ret
```

`add rsp,0xffffffffffffff80` 이거 같은 경우엔 그냥 `rsp`에서 `~0xffffffffffffff80` 값을 뺀것과 같다. 아직도 비트 연산이 헷갈리네...

일단 `fgets`에서 BOF가 발생하는 것 같다. Canary가 있어서 리턴 주소를 덮을 수 없다.

간단하게 생각하자. `password`값만 알면 된다. 혹시 디버거로 저기에 멈춰서 `password`값을 얻을 수 있지 않을까? 했는데

```assembly
(gdb) x/100s 0x6010a0
0x6010a0 <password>:    "cat: password: Permission denied\n"
```

읭??? `fopen`으로 데이터를 가져오는데 뭔가 많이 본듯한 문자열이 있다. 설마 저게 내용은 아니겠지? 했는데

```bash
blukat@ubuntu:~$ ./blukat
guess the password!
cat: password: Permission denied
congrats! here is your flag: Pl3as_DonT_Miss_youR_GrouP_Perm!!
```

??????

파일 권한을 살펴보자.

```bash
blukat@ubuntu:~$ id
uid=1104(blukat) gid=1104(blukat) groups=1104(blukat),1105(blukat_pwn)
blukat@ubuntu:~$ ls -al
total 36
drwxr-x---  4 root blukat     4096 Aug 15 22:55 .
drwxr-xr-x 93 root root       4096 Oct 10 22:56 ..
-r-xr-sr-x  1 root blukat_pwn 9144 Aug  8 06:44 blukat
-rw-r--r--  1 root root        645 Aug  8 06:43 blukat.c
dr-xr-xr-x  2 root root       4096 Aug 15 22:55 .irssi
-rw-r-----  1 root blukat_pwn   33 Jan  6  2017 password
drwxr-xr-x  2 root root       4096 Aug 15 22:55 .pwntools-cache
```

`cat`으로 password를 쳤을 때 나오던 경고 문구가 사실 내용이었다ㅋ 그룹권한에 읽기가 있었기 때문에 읽을 수 있었다 헿

```
blukat@ubuntu:~$ cat /etc/shadow
cat: /etc/shadow: Permission denied
blukat@ubuntu:~$ cat password
cat: password: Permission denied
```

뭐 권한 안봤으면 속았을 수도...? 아 근데 만약 권한이 없었다면 이걸 어떻게 했어야 되려나 방법이 없지 않을까???

문제는 정직했던 걸로ㅋ