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

- 아무래도 사용 쓰임새랑 파라미터를 보아하니 `0x80482e0`은 `memset`같은 초기화용 함수인것 같다.
- `0x80482f0`은 `strcmp`같은 문자열 비교 함수가 아닐까 조심스럽게... 예상해본다.

일단 BASE64로 인코딩한 `\xef\xbe\xad\xde`값을 넣으면 `correct`함수의 검증을 통과할 수 있다. 문제는 `auth`함수의 MD5 해쉬값 찾는 검증과정인데... `\xef\xbe\xad\xde`값 뒤에 어떤값을 넣든 `int`로 캐스팅 되기 때문에 `correct`함수의 검증과정은 피할수 있다. 이걸 BF로 계속 돌려서 찾아야 되려나...?