# Pwnable.kr

BOB 취약점 트랙에 들어가면 하루? 숙제로 준다는 pwnable.kr이다.

말도안돼

참고로 사이트에 있는 그림은 [Ragnarok M: Eternal Love](https://www.ragnaroketernallove.com/)라는 게임에서 나온 카드 그림이다. 

(~~개인적으로 너구리가 귀여운것 같다~~)

![nuguri](screenshot/card_20001.jpg)

## 문제

- Toddler's Bottle
  - [fd](fd.md) : 파일 디스크립터
  - [collision](collision.md) : 포인터
  - [bof](bof.md) : 버퍼 오버플로우
  - [flag](flag.md) : 바이너리 패킹
  - [passcode](passcode.md) : GOT Overwrite
  - [random](random.md) : rand 사용의 부적절한 예?
  - [input](input.md) : 여러가지 입출력 코딩
  - [leg](leg.md) : Fetch-Decode-Execute
  - [mistake](mistake.md) : 연산자 우선순위
  - [shellshock](shellshock.md) : 문제 이름 그대로
  - [coin1](coin1.md) : 코딩코딩
  - [blackjack](blackjack.md) : 뭔가 이상한 코드
  - [lotto](lotto.md) : 숫자 검증하는 로직을 잘보자
  - [cmd1](cmd1.md) : 환경변수
  - [cmd2](cmd2.md) : 쉘을 잘 써먹자
  - [uaf](uaf.md) : Use-After-Free
  - [memcpy]()
  - [asm](asm.md) : 64비트 쉘코드 짜기
  - [unlink](unlink.md) : Heap 오버플로우, Unlink 매크로를 활용한 익스플로잇
  - [blukat](blukat.md) : 권한설정
  - [horcruxes]()
- Rookiss
  - [simple login](simple_login.md) : EBP, ESP, EIP 컨트롤