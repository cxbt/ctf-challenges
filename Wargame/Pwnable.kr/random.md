# random - 1 pt

```text
Daddy, teach me how to use random value in programming!

ssh random@pwnable.kr -p2222 (pw:guest)
```

# random 소스코드를 보자!

```c
random@ubuntu:~$ ls
flag  random  random.c
random@ubuntu:~$ cat random.c
#include <stdio.h>

int main(){
        unsigned int random;
        random = rand();        // random value!

        unsigned int key=0;
        scanf("%d", &key);

        if( (key ^ random) == 0xdeadbeef ){
                printf("Good!\n");
                system("/bin/cat flag");
                return 0;
        }

        printf("Wrong, maybe you should try 2^32 cases.\n");
        return 0;
}
```

## 정말로 2^32 경우의 수를 다 해봐야 돼나요??

```c
random@ubuntu:~$ gdb -q random
Reading symbols from random...(no debugging symbols found)...done.
(gdb) set disassembly-flavor intel
(gdb) disas main
Dump of assembler code for function main:
   0x00000000004005f4 <+0>:     push   rbp
   0x00000000004005f5 <+1>:     mov    rbp,rsp
   0x00000000004005f8 <+4>:     sub    rsp,0x10
   0x00000000004005fc <+8>:     mov    eax,0x0
   0x0000000000400601 <+13>:    call   0x400500 <rand@plt>
   0x0000000000400606 <+18>:    mov    DWORD PTR [rbp-0x4],eax
   0x0000000000400609 <+21>:    mov    DWORD PTR [rbp-0x8],0x0
   0x0000000000400610 <+28>:    mov    eax,0x400760
   0x0000000000400615 <+33>:    lea    rdx,[rbp-0x8]
   0x0000000000400619 <+37>:    mov    rsi,rdx
   0x000000000040061c <+40>:    mov    rdi,rax
   0x000000000040061f <+43>:    mov    eax,0x0
   0x0000000000400624 <+48>:    call   0x4004f0 <__isoc99_scanf@plt>
   0x0000000000400629 <+53>:    mov    eax,DWORD PTR [rbp-0x8]
   0x000000000040062c <+56>:    xor    eax,DWORD PTR [rbp-0x4]
   0x000000000040062f <+59>:    cmp    eax,0xdeadbeef
   0x0000000000400634 <+64>:    jne    0x400656 <main+98>
   0x0000000000400636 <+66>:    mov    edi,0x400763
   0x000000000040063b <+71>:    call   0x4004c0 <puts@plt>
   0x0000000000400640 <+76>:    mov    edi,0x400769
   0x0000000000400645 <+81>:    mov    eax,0x0
   0x000000000040064a <+86>:    call   0x4004d0 <system@plt>
   0x000000000040064f <+91>:    mov    eax,0x0
   0x0000000000400654 <+96>:    jmp    0x400665 <main+113>
   0x0000000000400656 <+98>:    mov    edi,0x400778
   0x000000000040065b <+103>:   call   0x4004c0 <puts@plt>
   0x0000000000400660 <+108>:   mov    eax,0x0
   0x0000000000400665 <+113>:   leave
   0x0000000000400666 <+114>:   ret
End of assembler dump.
```

`main+18`을 보면 `rand` 함수 결과값을 `rbp-0x4`에 넣는 걸 볼 수 있습니다. 그런데...

```text
(gdb) b *main+33
Breakpoint 1 at 0x400615
(gdb) run
Starting program: /home/random/random

Breakpoint 1, 0x0000000000400615 in main ()
(gdb) x/d $rbp-0x4
0x7ffc0b68e51c: 1804289383
(gdb) run
The program being debugged has been started already.
Start it from the beginning? (y or n) c
Please answer y or n.
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program: /home/random/random

Breakpoint 1, 0x0000000000400615 in main ()
(gdb) x/d $rbp-0x4
0x7ffda162f48c: 1804289383
(gdb) run
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program: /home/random/random

Breakpoint 1, 0x0000000000400615 in main ()
(gdb) x/d $rbp-0x4
0x7ffd8bb255fc: 1804289383
```

값을 할당한 이후 라인에 breakpoint를 걸고 `rbp-0x4`에 들어간 값을 보면 위와 같이 값이 같습니다. 이는 rand()함수의 seed가 같아서 같은 값이 나오게 되는거죠ㅋ

## 그래서...

> 1804289383 XOR 0xdeadbeef = 0xB526FB88

그래서 3039230856 (=0xB526FB88)을 넣으면 flag를 획득할수 있는거죠ㅎ

```text
random@ubuntu:~$ ./random
3039230856
Good!
Mommy, I thought libc random is unpredictable...
random@ubuntu:~$
```