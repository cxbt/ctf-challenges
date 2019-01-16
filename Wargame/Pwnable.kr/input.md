# input - 4 pt

## 문제

```text
Mom? how can I pass my input to a computer program?

ssh input2@pwnable.kr -p2222 (pw:guest)
```

## 풀이

`input`의 소스코드를 보자.

```c
input2@ubuntu:~$ ls
flag  input  input.c
input2@ubuntu:~$ cat input.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>

int main(int argc, char* argv[], char* envp[]){
        printf("Welcome to pwnable.kr\n");
        printf("Let's see if you know how to give input to program\n");
        printf("Just give me correct inputs then you will get the flag :)\n");

        // argv
        if(argc != 100) return 0;
        if(strcmp(argv['A'],"\x00")) return 0;
        if(strcmp(argv['B'],"\x20\x0a\x0d")) return 0;
        printf("Stage 1 clear!\n");

        // stdio
        char buf[4];
        read(0, buf, 4);
        if(memcmp(buf, "\x00\x0a\x00\xff", 4)) return 0;
        read(2, buf, 4);
        if(memcmp(buf, "\x00\x0a\x02\xff", 4)) return 0;
        printf("Stage 2 clear!\n");

        // env
        if(strcmp("\xca\xfe\xba\xbe", getenv("\xde\xad\xbe\xef"))) return 0;
        printf("Stage 3 clear!\n");

        // file
        FILE* fp = fopen("\x0a", "r");
        if(!fp) return 0;
        if( fread(buf, 4, 1, fp)!=1 ) return 0;
        if( memcmp(buf, "\x00\x00\x00\x00", 4) ) return 0;
        fclose(fp);
        printf("Stage 4 clear!\n");

        // network
        int sd, cd;
        struct sockaddr_in saddr, caddr;
        sd = socket(AF_INET, SOCK_STREAM, 0);
        if(sd == -1){
                printf("socket error, tell admin\n");
                return 0;
        }
        saddr.sin_family = AF_INET;
        saddr.sin_addr.s_addr = INADDR_ANY;
        saddr.sin_port = htons( atoi(argv['C']) );
        if(bind(sd, (struct sockaddr*)&saddr, sizeof(saddr)) < 0){
                printf("bind error, use another port\n");
                return 1;
        }
        listen(sd, 1);
        int c = sizeof(struct sockaddr_in);
        cd = accept(sd, (struct sockaddr *)&caddr, (socklen_t*)&c);
        if(cd < 0){
                printf("accept error, tell admin\n");
                return 0;
        }
        if( recv(cd, buf, 4, 0) != 4 ) return 0;
        if(memcmp(buf, "\xde\xad\xbe\xef", 4)) return 0;
        printf("Stage 5 clear!\n");

        // here's your flag
        system("/bin/cat flag");
        return 0;
}
```

프로그램에 적절한 입력값을 주면 `flag`를 찾을 수 있다.

### 스테이지 1

```c
// argv
if(argc != 100) return 0;
if(strcmp(argv['A'],"\x00")) return 0;
if(strcmp(argv['B'],"\x20\x0a\x0d")) return 0;
printf("Stage 1 clear!\n");
```

단계 통과 조건은 다음과 같다.

- 파라미터 개수가 100개여야 한다. 호출할 때 프로그램 이름을 제외하면 99개의 파라미터를 넘겨줘야 한다.
- 65번째 파라미터 값은 `\x00` 이어야 한다.
- 66번째 파라미터 값은 `\x20\x0a\x0d` 이어야 한다.

일단 레벨 1을 통과해 보자. 서버에 `pwntools`이 깔려있길래 그걸 썼다.

```python
from pwn import *

argv = []
for i in range(100):
        argv += 'A'
argv[65] = '\x00'
argv[66] = '\x20\x0a\x0d'
p = process(argv, shell=False, executable='/home/input2/input')
print p.recvuntil('!')
```

이렇게 하면

```bash
input2@ubuntu:~$ python /tmp/nvm.py
[+] Starting local process '/home/input2/input': Done
Welcome to pwnable.kr
Let's see if you know how to give input to program
Just give me correct inputs then you will get the flag :)
Stage 1 clear!
[*] Stopped program '/home/input2/input'
```

1단계 통과!

### 스테이지 2

```c
// stdio
char buf[4];
read(0, buf, 4);
if(memcmp(buf, "\x00\x0a\x00\xff", 4)) return 0;
read(2, buf, 4);
if(memcmp(buf, "\x00\x0a\x02\xff", 4)) return 0;
printf("Stage 2 clear!\n");
```

`stdin`에서 4바이트 받고, `stderr`에서 4바이트 받는다.

```python
from pwn import *

f = open('/tmp/nvm2', 'w')      #  여기추가
f.write('\x00\x0a\x02\xff')     #  여기추가
f.close()                       #  여기추가

argv = []
for i in range(100):
        argv += 'A'
argv[65] = '\x00'
argv[66] = '\x20\x0a\x0d'
p = process(argv, shell=False, stderr=open('/tmp/nvm2'), executable='/home/input2/input')       #  여기수정
print p.recvuntil('!')

p.write('\x00\x0a\x00\xff')     #  여기추가
print p.recvuntil('!')          #  여기추가
```

그대로 스크립트에 추가해 주자.

```bash
input2@ubuntu:~$ python /tmp/nvm.py
[+] Starting local process '/home/input2/input': Done
Welcome to pwnable.kr
Let's see if you know how to give input to program
Just give me correct inputs then you will get the flag :)
Stage 1 clear!

Stage 2 clear!
[*] Stopped program '/home/input2/input'
```

좋아요

### 스테이지 3

```c
// env
if(strcmp("\xca\xfe\xba\xbe", getenv("\xde\xad\xbe\xef"))) return 0;
printf("Stage 3 clear!\n");
```

환경변수만 집어넣어주면 된다.

```python
from pwn import *

f = open('/tmp/nvm2', 'w')
f.write('\x00\x0a\x02\xff')
f.close()

argv = []
for i in range(100):
        argv += 'A'
argv[65] = '\x00'
argv[66] = '\x20\x0a\x0d'
env_me = {"\xde\xad\xbe\xef" : "\xca\xfe\xba\xbe"}
p = process(argv, shell=False, stderr=open('/tmp/nvm2'), executable='/home/input2/input', env=env_me)
print p.recvuntil('!')

p.write('\x00\x0a\x00\xff')
print p.recvuntil('!')
print p.recvuntil('!')
```

이렇게 process 객체 만들때 환경변수 딕셔너리도 같이 넣어 준다.

```bash
input2@ubuntu:~$ python /tmp/nvm.py
[+] Starting local process '/home/input2/input': Done
Welcome to pwnable.kr
Let's see if you know how to give input to program
Just give me correct inputs then you will get the flag :)
Stage 1 clear!

Stage 2 clear!

Stage 3 clear!
[*] Process '/home/input2/input' stopped with exit code 0
```

### 스테이지 4

```c
// file
FILE* fp = fopen("\x0a", "r");
if(!fp) return 0;
if( fread(buf, 4, 1, fp)!=1 ) return 0;
if( memcmp(buf, "\x00\x00\x00\x00", 4) ) return 0;
fclose(fp);
printf("Stage 4 clear!\n");
```

`\x0a`라는 파일을 읽기 전용으로 열어서 `\x00\x00\x00\x00`을 읽어와서 비교한다.

```python
from pwn import *

argv = ['A' for i in range(100)]
argv[65] = '\x00'
argv[66] = '\x20\x0a\x0d'

f = open('/tmp/nvm2', 'w')
f.write('\x00\x0a\x02\xff')
f.close()

f = open('\x0a', 'w')
f.write('\x00\x00\x00\x00')
f.close()

env_me = {"\xde\xad\xbe\xef" : "\xca\xfe\xba\xbe"}

p = process(argv, shell=False, stderr=open('/tmp/nvm2'), executable='/home/input2/input', env=env_me)

# Round 1
print p.recvuntil('!')
# Round 2
p.write('\x00\x0a\x00\xff')
print p.recvuntil('!')
# Round 3
print p.recvuntil('!')
# Round 4
print p.recvuntil('!')
```

스테이지 2랑 동일하게 파일을 그때마다 하나 만들어 준다.

```bash
input2@ubuntu:/tmp$ python nvm.py
[+] Starting local process '/home/input2/input': Done
Welcome to pwnable.kr
Let's see if you know how to give input to program
Just give me correct inputs then you will get the flag :)
Stage 1 clear!

Stage 2 clear!

Stage 3 clear!

Stage 4 clear!
[*] Stopped program '/home/input2/input'
```

### 스테이지 5

```c
// network
int sd, cd;
struct sockaddr_in saddr, caddr;
sd = socket(AF_INET, SOCK_STREAM, 0);
if(sd == -1){
        printf("socket error, tell admin\n");
        return 0;
}
saddr.sin_family = AF_INET;
saddr.sin_addr.s_addr = INADDR_ANY;
saddr.sin_port = htons( atoi(argv['C']) );
if(bind(sd, (struct sockaddr*)&saddr, sizeof(saddr)) < 0){
        printf("bind error, use another port\n");
        return 1;
}
listen(sd, 1);
int c = sizeof(struct sockaddr_in);
cd = accept(sd, (struct sockaddr *)&caddr, (socklen_t*)&c);
if(cd < 0){
        printf("accept error, tell admin\n");
        return 0;
}
if( recv(cd, buf, 4, 0) != 4 ) return 0;
if(memcmp(buf, "\xde\xad\xbe\xef", 4)) return 0;
printf("Stage 5 clear!\n");
```

67번째 파라미터 값을 포트번호로 설정해서 loopback으로 연결을 기다린다. 그리고 받은 값이 `\xde\xad\xbe\xef`이면 된다.

```python
from pwn import *

argv = ['A' for i in range(100)]
argv[ord('A')] = '\x00'
argv[ord('B')] = '\x20\x0a\x0d'
argv[ord('C')] = '13371'

f = open('/tmp/nvm2', 'w')
f.write('\x00\x0a\x02\xff')
f.close()

f = open('\x0a', 'w')
f.write('\x00\x00\x00\x00')
f.close()

env_me = {"\xde\xad\xbe\xef" : "\xca\xfe\xba\xbe"}

p = process(argv, shell=False, stderr=open('/tmp/nvm2'), executable='/home/input2/input', env=env_me)

# Round 1
print p.recvuntil('!')
# Round 2
p.write('\x00\x0a\x00\xff')
print p.recvuntil('!')
# Round 3
print p.recvuntil('!')
# Round 4
print p.recvuntil('!')
# Round 5
r = remote('127.0.0.1', argv[ord('C')])
r.send('\xde\xad\xbe\xef')
p.interactive()
```

이렇게 하고 홈 디렉토리에 있는 flag로 가는 링크를 만들어 준다.

```bash
input2@ubuntu:/tmp/nvm$ ln -s /home/input2/flag flag
input2@ubuntu:/tmp/nvm$ python nvm.py
[+] Starting local process '/home/input2/input': Done
Welcome to pwnable.kr
Let's see if you know how to give input to program
Just give me correct inputs then you will get the flag :)
Stage 1 clear!

Stage 2 clear!

Stage 3 clear!

Stage 4 clear!
[+] Opening connection to 127.0.0.1 on port 13371: Done
[*] Switching to interactive mode

Stage 5 clear!
Mommy! I learned how to pass various input in Linux :)
[*] Process '/home/input2/input' stopped with exit code 0
[*] Got EOF while reading in interactive
```

### 결론

1. pwntool로 process 객체를 만든다.
2. 파라미터, 환경변수, 표준에러 등을 만들어서 넘겨준다.
3. process 객체에 적절한 입력을 넣어준다.
4. 파일도 만든다.
5. remote로 연결해 데이터를 보낸다.

끝!