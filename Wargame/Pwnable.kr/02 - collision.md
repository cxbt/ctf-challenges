# collision - 3 pt

```text
Daddy told me about cool MD5 hash collision today.
I wanna do something like that too!

ssh col@pwnable.kr -p2222 (pw:guest)
```

## 일단 SSH로 연결해보자

```text
cxbt@CXBT:dsm2016$ ssh col@pwnable.kr -p2222
col@pwnable.kr's password:
 ____  __    __  ____    ____  ____   _        ___      __  _  ____
|    \|  |__|  ||    \  /    ||    \ | |      /  _]    |  |/ ]|    \
|  o  )  |  |  ||  _  ||  o  ||  o  )| |     /  [_     |  ' / |  D  )
|   _/|  |  |  ||  |  ||     ||     || |___ |    _]    |    \ |    /
|  |  |  `  '  ||  |  ||  _  ||  O  ||     ||   [_  __ |     \|    \
|  |   \      / |  |  ||  |  ||     ||     ||     ||  ||  .  ||  .  \
|__|    \_/\_/  |__|__||__|__||_____||_____||_____||__||__|\_||__|\_|

- Site admin : daehee87.kr@gmail.com
- IRC : irc.netgarage.org:6667 / #pwnable.kr
- Simply type "irssi" command to join IRC now
- files under /tmp can be erased anytime. make your directory under /tmp
- to use peda, issue `source /usr/share/peda/peda.py` in gdb terminal
Last login: Thu May 17 16:47:57 2018 from 129.219.8.222
col@ubuntu:~$ ls -al
total 36
drwxr-x---  5 root    col     4096 Oct 23  2016 .
drwxr-xr-x 87 root    root    4096 Dec 27 23:17 ..
d---------  2 root    root    4096 Jun 12  2014 .bash_history
-r-sr-x---  1 col_pwn col     7341 Jun 11  2014 col
-rw-r--r--  1 root    root     555 Jun 12  2014 col.c
-r--r-----  1 col_pwn col_pwn   52 Jun 11  2014 flag
dr-xr-xr-x  2 root    root    4096 Aug 20  2014 .irssi
drwxr-xr-x  2 root    root    4096 Oct 23  2016 .pwntools-cache
col@ubuntu:~$ id
uid=1005(col) gid=1005(col) groups=1005(col)
```

`col` 실행파일의 소스코드는 다음과 같다.

```c
col@ubuntu:~$ cat col.c
#include <stdio.h>
#include <string.h>
unsigned long hashcode = 0x21DD09EC;
unsigned long check_password(const char* p){
        int* ip = (int*)p;
        int i;
        int res=0;
        for(i=0; i<5; i++){
                res += ip[i];
        }
        return res;
}

int main(int argc, char* argv[]){
        if(argc<2){
                printf("usage : %s [passcode]\n", argv[0]);
                return 0;
        }
        if(strlen(argv[1]) != 20){
                printf("passcode length should be 20 bytes\n");
                return 0;
        }

        if(hashcode == check_password( argv[1] )){
                system("/bin/cat flag");
                return 0;
        }
        else
                printf("wrong passcode.\n");
        return 0;
}
```

```asm
Dump of assembler code for function check_password:
   0x08048494 <+0>:     push   ebp
   0x08048495 <+1>:     mov    ebp,esp
   0x08048497 <+3>:     sub    esp,0x10
   0x0804849a <+6>:     mov    eax,DWORD PTR [ebp+0x8]
   0x0804849d <+9>:     mov    DWORD PTR [ebp-0x4],eax
   0x080484a0 <+12>:    mov    DWORD PTR [ebp-0x8],0x0
   0x080484a7 <+19>:    mov    DWORD PTR [ebp-0xc],0x0
   0x080484ae <+26>:    jmp    0x80484c2 <check_password+46>
   0x080484b0 <+28>:    mov    eax,DWORD PTR [ebp-0xc]
   0x080484b3 <+31>:    shl    eax,0x2
   0x080484b6 <+34>:    add    eax,DWORD PTR [ebp-0x4]
   0x080484b9 <+37>:    mov    eax,DWORD PTR [eax]
   0x080484bb <+39>:    add    DWORD PTR [ebp-0x8],eax
   0x080484be <+42>:    add    DWORD PTR [ebp-0xc],0x1
   0x080484c2 <+46>:    cmp    DWORD PTR [ebp-0xc],0x4
   0x080484c6 <+50>:    jle    0x80484b0 <check_password+28>
   0x080484c8 <+52>:    mov    eax,DWORD PTR [ebp-0x8]
   0x080484cb <+55>:    leave
   0x080484cc <+56>:    ret

Dump of assembler code for function main:
   0x080484cd <+0>:     push   ebp
   0x080484ce <+1>:     mov    ebp,esp
   0x080484d0 <+3>:     push   edi
   0x080484d1 <+4>:     and    esp,0xfffffff0
   0x080484d4 <+7>:     sub    esp,0x90
   0x080484da <+13>:    mov    eax,DWORD PTR [ebp+0xc]
   0x080484dd <+16>:    mov    DWORD PTR [esp+0x1c],eax
   0x080484e1 <+20>:    mov    eax,gs:0x14
   0x080484e7 <+26>:    mov    DWORD PTR [esp+0x8c],eax
   0x080484ee <+33>:    xor    eax,eax
   0x080484f0 <+35>:    cmp    DWORD PTR [ebp+0x8],0x1
   0x080484f4 <+39>:    jg     0x8048514 <main+71>
   0x080484f6 <+41>:    mov    eax,DWORD PTR [esp+0x1c]
   0x080484fa <+45>:    mov    edx,DWORD PTR [eax]
   0x080484fc <+47>:    mov    eax,0x8048680
   0x08048501 <+52>:    mov    DWORD PTR [esp+0x4],edx
   0x08048505 <+56>:    mov    DWORD PTR [esp],eax
   0x08048508 <+59>:    call   0x8048380 <printf@plt>
   0x0804850d <+64>:    mov    eax,0x0
   0x08048512 <+69>:    jmp    0x8048592 <main+197>
   0x08048514 <+71>:    mov    eax,DWORD PTR [esp+0x1c]
   0x08048518 <+75>:    add    eax,0x4
   0x0804851b <+78>:    mov    eax,DWORD PTR [eax]
   0x0804851d <+80>:    mov    DWORD PTR [esp+0x18],0xffffffff
   0x08048525 <+88>:    mov    edx,eax
   0x08048527 <+90>:    mov    eax,0x0
   0x0804852c <+95>:    mov    ecx,DWORD PTR [esp+0x18]
   0x08048530 <+99>:    mov    edi,edx
   0x08048532 <+101>:   repnz scas al,BYTE PTR es:[edi]
   0x08048534 <+103>:   mov    eax,ecx
   0x08048536 <+105>:   not    eax
   0x08048538 <+107>:   sub    eax,0x1
   0x0804853b <+110>:   cmp    eax,0x14
   0x0804853e <+113>:   je     0x8048553 <main+134>
   0x08048540 <+115>:   mov    DWORD PTR [esp],0x8048698
   0x08048547 <+122>:   call   0x80483a0 <puts@plt>
   0x0804854c <+127>:   mov    eax,0x0
   0x08048551 <+132>:   jmp    0x8048592 <main+197>
   0x08048553 <+134>:   mov    eax,DWORD PTR [esp+0x1c]
   0x08048557 <+138>:   add    eax,0x4
   0x0804855a <+141>:   mov    eax,DWORD PTR [eax]
   0x0804855c <+143>:   mov    DWORD PTR [esp],eax
   0x0804855f <+146>:   call   0x8048494 <check_password>
   0x08048564 <+151>:   mov    edx,DWORD PTR ds:0x804a020
   0x0804856a <+157>:   cmp    eax,edx
   0x0804856c <+159>:   jne    0x8048581 <main+180>
   0x0804856e <+161>:   mov    DWORD PTR [esp],0x80486bb
   0x08048575 <+168>:   call   0x80483b0 <system@plt>
   0x0804857a <+173>:   mov    eax,0x0
   0x0804857f <+178>:   jmp    0x8048592 <main+197>
   0x08048581 <+180>:   mov    DWORD PTR [esp],0x80486c9
   0x08048588 <+187>:   call   0x80483a0 <puts@plt>
   0x0804858d <+192>:   mov    eax,0x0
   0x08048592 <+197>:   mov    edx,DWORD PTR [esp+0x8c]
   0x08048599 <+204>:   xor    edx,DWORD PTR gs:0x14
   0x080485a0 <+211>:   je     0x80485a7 <main+218>
   0x080485a2 <+213>:   call   0x8048390 <__stack_chk_fail@plt>
   0x080485a7 <+218>:   mov    edi,DWORD PTR [ebp-0x4]
   0x080485aa <+221>:   leave
   0x080485ab <+222>:   ret
```

## 아이고 이걸 어떻게 푸냐

`flag`를 얻기 위해선 정적으로 저장되어 있는 `hashcode`값과 입력한 `passcode`가 같아야 한다. 그런데 어떻게 같게 하지...?

## 포인터, 변수, 별의별것

아래의 코드가 우리가 입력한 `passcode`를 계산하는 루틴이다. `passcode`는 각 문자를 `int`포인터로 캐스팅해 `int res`에 누적해 간다. 이때 저장하는 변수의 자료가 `int`란 것에 주목하자. `int`형은 32비트에선 4바이트의 공간을 차지하고, 만약 값이 표현할수 있는 범위(-2^32-1 ~ 2^31)를 넘게 되면 오버플로우나 언더플로우가 발생한다. 이때 넘친 값은 그냥 사라지게 된다.

```c
unsigned long check_password(const char* p){
        int* ip = (int*)p;
        int i;
        int res=0;
        for(i=0; i<5; i++){
                res += ip[i];
        }
        return res;
}
```

만약 문자 하나하나를 `int`형 포인터로 캐스팅하게 되면 어떻게 될까?

```text
char* p = [a][b][c][d][a][b][c][d][a][b][c][d] ...
int* ip = [0x64636261][0x64636261][0x64636261] ...
```

`char`자료형은 1바이트, `int`자료형은 4바이트 크기를 가지므로 `char*`가 `int*`로 캐스팅 되면 문자 4개가 세트로 정수형으로 표현되게 된다. 이때 정수값은 각 문자의 코드값을 이어 붙인 것처럼 된다. 스택에 문자열이 어떤 모양으로 저장 되어있는지 생각하면 떠올리기 쉽다.

결론은 `argv[1]`으로 준 문자열 인수는 4개가 합쳐져서 하나의 정수로 표현되고, `res`에 값이 더해지게 된다.

## 포인터를 생각해 보자

`hashcode`는 0x21DD09EC이고, `passcode`는 무조건 20바이트 길이를 가져야 하므로, 간단하게 `passcode`를 (0x21DD09EC/5)를 5번 이어붙인것처럼 만들도록 하겠다. 뭔 말인지 모르겠으면 다시 위에 올라가서 생각해 보자. 이때 0x21DD09EC가 5로 나눠지지 않는 다는 문제가 발생하는데, 나는 간단하게 4바이트 외의 값은 무시된다는 것을 이용해 0x*1*21DD09EC를 5로 나눈 값을 `passcode`로 사용했다. 어차피 5번 더해서 생긴 0x100000000은 무시되기 때문에 상관없다ㅋ

```text
0x021DD09EC = 0x0877427B * 4
0x121DD09EC = 0x39F901FC * 5
```

## 그래서 어떻게 할까요

```text
col@ubuntu:~$ ./col `python -c "print '\xfc\x01\xf9\x39'*5"`
daddy! I just managed to create a hash collision :)
```

위에 언급한것 처럼 0x39F901FC를 5번 이어붙힌 `passcode`를 프로그램 인자로 넣으면 `hashcode`와 `passcode`가 같아지면서 문제를 해결할 수 있게 된다!