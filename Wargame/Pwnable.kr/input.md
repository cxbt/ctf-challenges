# input - 4 pt

```text
Mom? how can I pass my input to a computer program?

ssh input2@pwnable.kr -p2222 (pw:guest)
```

## SSH로 접속한다 실시

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

## 레벨 1

```c
        // argv
        if(argc != 100) return 0;
        if(strcmp(argv['A'],"\x00")) return 0;
        if(strcmp(argv['B'],"\x20\x0a\x0d")) return 0;
        printf("Stage 1 clear!\n");
```

단계 통과 조건은 다음과 같다.

- 매개변수가 딱 100개이다. (물론 99개를 넣어야 된다)
- `argv['A']` = `argv[65]` 이 `\x00` 이어야 한다.
- `argv['B']` = `argv[66]` 이 `\x20\x0a\x0d` 이어야 한다.

일단 레벨 1을 통과해 보자. 아래는 위 루틴을 디스어셈블한 결과이다.

```c
   0x0000000000400994 <+64>:    cmp    DWORD PTR [rbp-0x54],0x64
        if(argc != 100)
   0x0000000000400998 <+68>:    je     0x4009a4 <main+80>
   0x000000000040099a <+70>:    mov    eax,0x0
   0x000000000040099f <+75>:    jmp    0x400c9a <main+838>
        return 0;
   0x00000000004009a4 <+80>:    mov    rax,QWORD PTR [rbp-0x60]
   0x00000000004009a8 <+84>:    add    rax,0x208
   0x00000000004009ae <+90>:    mov    rax,QWORD PTR [rax]
   0x00000000004009b1 <+93>:    movzx  eax,BYTE PTR [rax]
   0x00000000004009b4 <+96>:    test   al,al
        if(strcmp(argv['A'], "\x00"))
   0x00000000004009b6 <+98>:    je     0x4009c2 <main+110>
   0x00000000004009b8 <+100>:   mov    eax,0x0
   0x00000000004009bd <+105>:   jmp    0x400c9a <main+838>
        return 0;
   0x00000000004009c2 <+110>:   mov    rax,QWORD PTR [rbp-0x60]
   0x00000000004009c6 <+114>:   add    rax,0x210
   0x00000000004009cc <+120>:   mov    rax,QWORD PTR [rax]
   0x00000000004009cf <+123>:   mov    rdx,rax
   0x00000000004009d2 <+126>:   mov    eax,0x400e2a
   0x00000000004009d7 <+131>:   mov    ecx,0x4
   0x00000000004009dc <+136>:   mov    rsi,rdx
   0x00000000004009df <+139>:   mov    rdi,rax
   0x00000000004009e2 <+142>:   repz cmps BYTE PTR ds:[rsi],BYTE PTR es:[rdi]
   0x00000000004009e4 <+144>:   seta   dl
   0x00000000004009e7 <+147>:   setb   al
   0x00000000004009ea <+150>:   mov    ecx,edx
   0x00000000004009ec <+152>:   sub    cl,al
   0x00000000004009ee <+154>:   mov    eax,ecx
   0x00000000004009f0 <+156>:   movsx  eax,al
   0x00000000004009f3 <+159>:   test   eax,eax
   0x00000000004009f5 <+161>:   je     0x400a01 <main+173>
   0x00000000004009f7 <+163>:   mov    eax,0x0
   0x00000000004009fc <+168>:   jmp    0x400c9a <main+838>
   0x0000000000400a01 <+173>:   mov    edi,0x400e2e
   0x0000000000400a06 <+178>:   call   0x400780 <puts@plt>
        printf("Stage 1 clear!\n");
```