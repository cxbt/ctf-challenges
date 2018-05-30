# leg - 2 pt

```text
Daddy told me I should study arm.
But I prefer to study my leg!

Download : http://pwnable.kr/bin/leg.c
Download : http://pwnable.kr/bin/leg.asm

ssh leg@pwnable.kr -p2222 (pw:guest)
```

## ARM이라니

```c
ch4sis@ubuntu:leg$ cat leg.c
#include <stdio.h>
#include <fcntl.h>
int key1(){
        asm("mov r3, pc\n");
}
int key2(){
        asm(
        "push   {r6}\n"
        "add    r6, pc, $1\n"
        "bx     r6\n"
        ".code   16\n"
        "mov    r3, pc\n"
        "add    r3, $0x4\n"
        "push   {r3}\n"
        "pop    {pc}\n"
        ".code  32\n"
        "pop    {r6}\n"
        );
}
int key3(){
        asm("mov r3, lr\n");
}
int main(){
        int key=0;
        printf("Daddy has very strong arm! : ");
        scanf("%d", &key);
        if( (key1()+key2()+key3()) == key ){
                printf("Congratz!\n");
                int fd = open("flag", O_RDONLY);
                char buf[100];
                int r = read(fd, buf, 100);
                write(0, buf, r);
        }
        else{
                printf("I have strong leg :P\n");
        }
        return 0;
}
ch4sis@ubuntu:leg$ cat leg.asm
(gdb) disass main
Dump of assembler code for function main:
   0x00008d3c <+0>:     push    {r4, r11, lr}
   0x00008d40 <+4>:     add     r11, sp, #8
   0x00008d44 <+8>:     sub     sp, sp, #12
   0x00008d48 <+12>:    mov     r3, #0
   0x00008d4c <+16>:    str     r3, [r11, #-16]
   0x00008d50 <+20>:    ldr     r0, [pc, #104]  ; 0x8dc0 <main+132>
   0x00008d54 <+24>:    bl      0xfb6c <printf>
   0x00008d58 <+28>:    sub     r3, r11, #16
   0x00008d5c <+32>:    ldr     r0, [pc, #96]   ; 0x8dc4 <main+136>
   0x00008d60 <+36>:    mov     r1, r3
   0x00008d64 <+40>:    bl      0xfbd8 <__isoc99_scanf>
   0x00008d68 <+44>:    bl      0x8cd4 <key1>
   0x00008d6c <+48>:    mov     r4, r0
   0x00008d70 <+52>:    bl      0x8cf0 <key2>
   0x00008d74 <+56>:    mov     r3, r0
   0x00008d78 <+60>:    add     r4, r4, r3
   0x00008d7c <+64>:    bl      0x8d20 <key3>
   0x00008d80 <+68>:    mov     r3, r0
   0x00008d84 <+72>:    add     r2, r4, r3
   0x00008d88 <+76>:    ldr     r3, [r11, #-16]
   0x00008d8c <+80>:    cmp     r2, r3
   0x00008d90 <+84>:    bne     0x8da8 <main+108>
   0x00008d94 <+88>:    ldr     r0, [pc, #44]   ; 0x8dc8 <main+140>
   0x00008d98 <+92>:    bl      0x1050c <puts>
   0x00008d9c <+96>:    ldr     r0, [pc, #40]   ; 0x8dcc <main+144>
   0x00008da0 <+100>:   bl      0xf89c <system>
   0x00008da4 <+104>:   b       0x8db0 <main+116>
   0x00008da8 <+108>:   ldr     r0, [pc, #32]   ; 0x8dd0 <main+148>
   0x00008dac <+112>:   bl      0x1050c <puts>
   0x00008db0 <+116>:   mov     r3, #0
   0x00008db4 <+120>:   mov     r0, r3
   0x00008db8 <+124>:   sub     sp, r11, #8
   0x00008dbc <+128>:   pop     {r4, r11, pc}
   0x00008dc0 <+132>:   andeq   r10, r6, r12, lsl #9
   0x00008dc4 <+136>:   andeq   r10, r6, r12, lsr #9
   0x00008dc8 <+140>:                   ; <UNDEFINED> instruction: 0x0006a4b0
   0x00008dcc <+144>:                   ; <UNDEFINED> instruction: 0x0006a4bc
   0x00008dd0 <+148>:   andeq   r10, r6, r4, asr #9
End of assembler dump.
(gdb) disass key1
Dump of assembler code for function key1:
   0x00008cd4 <+0>:     push    {r11}           ; (str r11, [sp, #-4]!)
   0x00008cd8 <+4>:     add     r11, sp, #0
   0x00008cdc <+8>:     mov     r3, pc
   0x00008ce0 <+12>:    mov     r0, r3
   0x00008ce4 <+16>:    sub     sp, r11, #0
   0x00008ce8 <+20>:    pop     {r11}           ; (ldr r11, [sp], #4)
   0x00008cec <+24>:    bx      lr
End of assembler dump.
(gdb) disass key2
Dump of assembler code for function key2:
   0x00008cf0 <+0>:     push    {r11}           ; (str r11, [sp, #-4]!)
   0x00008cf4 <+4>:     add     r11, sp, #0
   0x00008cf8 <+8>:     push    {r6}            ; (str r6, [sp, #-4]!)
   0x00008cfc <+12>:    add     r6, pc, #1
   0x00008d00 <+16>:    bx      r6
   0x00008d04 <+20>:    mov     r3, pc
   0x00008d06 <+22>:    adds    r3, #4
   0x00008d08 <+24>:    push    {r3}
   0x00008d0a <+26>:    pop     {pc}
   0x00008d0c <+28>:    pop     {r6}            ; (ldr r6, [sp], #4)
   0x00008d10 <+32>:    mov     r0, r3
   0x00008d14 <+36>:    sub     sp, r11, #0
   0x00008d18 <+40>:    pop     {r11}           ; (ldr r11, [sp], #4)
   0x00008d1c <+44>:    bx      lr
End of assembler dump.
(gdb) disass key3
Dump of assembler code for function key3:
   0x00008d20 <+0>:     push    {r11}           ; (str r11, [sp, #-4]!)
   0x00008d24 <+4>:     add     r11, sp, #0
   0x00008d28 <+8>:     mov     r3, lr
   0x00008d2c <+12>:    mov     r0, r3
   0x00008d30 <+16>:    sub     sp, r11, #0
   0x00008d34 <+20>:    pop     {r11}           ; (ldr r11, [sp], #4)
   0x00008d38 <+24>:    bx      lr
End of assembler dump.
(gdb)
```

## 몇가지 ARM에 관한 상식

- `int function(a, b, c)`로 분기할 때, `r1`, `r2`, `r3` 순으로 각각 `a`, `b`, `c` 데이터를 넣게 된다.
- ARM은 `fetch-decode-execute`라는 3단계 파이프라인을 거치기 때문에, 실제 명령어 실행은 2라인 뒤에서 된다.
- 함수의 `Return`값은 `r0` 레지스터에 저장되게 된다.

## key1을 보자

```c
Dump of assembler code for function key1:
   0x00008cd4 <+0>:     push    {r11}           ; (str r11, [sp, #-4]!)
   0x00008cd8 <+4>:     add     r11, sp, #0
->   0x00008cdc <+8>:     mov     r3, pc
->   0x00008ce0 <+12>:    mov     r0, r3
->   0x00008ce4 <+16>:    sub     sp, r11, #0
   0x00008ce8 <+20>:    pop     {r11}           ; (ldr r11, [sp], #4)
   0x00008cec <+24>:    bx      lr
```

함수의 리턴값은 `r0`에 저장된다고 했다. 우리가 볼건 `r0`값의 변화 뿐이다ㅋ `0x8cdc`에서 `pc`값을 `r3`에 넣고, `r3`에 넣은 값을 다시 `r0`에 넣는걸 볼 수 있는데, 파이프라인을 기억하자. 명령어는 2라인 뒤에서 실행된다. 2라인 뒤인 `0x8ce4`에서 `mov r3, pc`가 실행되게 되면서 `key1()`의 리턴값은 `0x8ce4`가 된다.

## key2를 보자 흐흐

```c
Dump of assembler code for function key2:
   0x00008cf0 <+0>:     push    {r11}           ; (str r11, [sp, #-4]!)
   0x00008cf4 <+4>:     add     r11, sp, #0
   0x00008cf8 <+8>:     push    {r6}            ; (str r6, [sp, #-4]!)
   0x00008cfc <+12>:    add     r6, pc, #1
   0x00008d00 <+16>:    bx      r6
->   0x00008d04 <+20>:    mov     r3, pc
->   0x00008d06 <+22>:    adds    r3, #4
   0x00008d08 <+24>:    push    {r3}
   0x00008d0a <+26>:    pop     {pc}
   0x00008d0c <+28>:    pop     {r6}            ; (ldr r6, [sp], #4)
->   0x00008d10 <+32>:    mov     r0, r3
   0x00008d14 <+36>:    sub     sp, r11, #0
   0x00008d18 <+40>:    pop     {r11}           ; (ldr r11, [sp], #4)
   0x00008d1c <+44>:    bx      lr
End of assembler dump.
```

`key1`에서 한 것 처럼 생각하면, `0x8d04`의 `mov r3, pc`는 `0x8d08`에 갈때 실행 되므로, `key2()`의 리턴값은 거기에 4를 더한 (`0x8d06` 참고) `0x8d0c`가 된다.

## key3를 보자 헤헤

```c
Dump of assembler code for function key3:
   0x00008d20 <+0>:     push    {r11}           ; (str r11, [sp, #-4]!)
   0x00008d24 <+4>:     add     r11, sp, #0
->   0x00008d28 <+8>:     mov     r3, lr
->   0x00008d2c <+12>:    mov     r0, r3
   0x00008d30 <+16>:    sub     sp, r11, #0
   0x00008d34 <+20>:    pop     {r11}           ; (ldr r11, [sp], #4)
   0x00008d38 <+24>:    bx      lr
```

`key3`으로 분기할때 `branch link`가 생성되었다. 그말인즉슨 돌아갈 리턴 어드레스가 `lr`에 저장되어 있다는 것이다. `key3`으로 분기하는 `bl` 명령어 다음 주소인 `0x8d80`가 들어있다. 그래서 `key3()` 리턴값은 `0x8d80`이 된다ㅋ

## 그래서

`0x8ce4` + `0x8d0c` + `0x8d80` = `0x1a770` = 108400

아하

```text
/ $ ./leg
Daddy has very strong arm! :
108400
Congratz!
My daddy has a lot of ARMv5te muscle!
```