# flag - 7 pt

```text
Papa brought me a packed present! let's open it.

Download : http://pwnable.kr/bin/flag

This is reversing task. all you need is binary
```

## flag를 뜯어보...?

문제에서 주어진 `flag` 실행파일을 보면 디버깅 심볼이 제거되있고 정적 링킹되어있는 것을 볼 수 있다.

```bash
cxbt@CXBT:Desktop$ curl -O http://pwnable.kr/bin/flag
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  327k  100  327k    0     0  1873k      0 --:--:-- --:--:-- --:--:-- 1881k
cxbt@CXBT:Desktop$ file flag
flag: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, stripped
```

`flag`를 gdb로 열어서 `main`함수를 디스어셈블하면 전과는 다르게 전혀 알아볼수 없게 되어 있다. 여기서 좀 삽질을 하다가 이 키워드를 찾고 고민을 그만 두게 되었다.

그렇다 이 파일은 UPX로 패킹되어 있어서 전혀 알아볼 수 없던 것이었다. UPX 패킹을 풀어보고 다시 코드를 보자.

## 그래서 정답은...

```c
(gdb) disas main
Dump of assembler code for function main:
   0x0000000000401164 <+0>:     push   rbp
   0x0000000000401165 <+1>:     mov    rbp,rsp
   0x0000000000401168 <+4>:     sub    rsp,0x10
   0x000000000040116c <+8>:     mov    edi,0x496658
   0x0000000000401171 <+13>:    call   0x402080 <puts>
   0x0000000000401176 <+18>:    mov    edi,0x64
   0x000000000040117b <+23>:    call   0x4099d0 <malloc>
   0x0000000000401180 <+28>:    mov    QWORD PTR [rbp-0x8],rax
   0x0000000000401184 <+32>:    mov    rdx,QWORD PTR [rip+0x2c0ee5]        # 0x6c2070 <flag>
   0x000000000040118b <+39>:    mov    rax,QWORD PTR [rbp-0x8]
   0x000000000040118f <+43>:    mov    rsi,rdx
   0x0000000000401192 <+46>:    mov    rdi,rax
   0x0000000000401195 <+49>:    call   0x400320
   0x000000000040119a <+54>:    mov    eax,0x0
=> 0x000000000040119f <+59>:    leave
   0x00000000004011a0 <+60>:    ret
End of assembler dump.
(gdb) x/s 0x6c2070
0x6c2070 <flag>:        "(fI"
(gdb) x/x $rbp-0x8
0x7fffffffe428: 0xb0
(gdb) x/4x $rbp-0x8
0x7fffffffe428: 0xb0    0x96    0x6c    0x00
(gdb) x/s 0x6c96b0
0x6c96b0:       "UPX...? sounds like a delivery service :)"
```

오예