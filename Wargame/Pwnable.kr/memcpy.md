# memcpy - 10 pt

## 문제

```text
Are you tired of hacking?, take some rest here.
Just help me out with my small experiment regarding memcpy performance. 
after that, flag is yours.

http://pwnable.kr/bin/memcpy.c

ssh memcpy@pwnable.kr -p2222 (pw:guest)
```

`memcpy`는 SIMD 명령어를 이용해 메모리 영역을 복사하는 것과 운영체제 시스템 콜을 사용해 메모리를 복사하는 방법의 시간차를 보여주는 프로그램이다. 사용자에게 입력받는 것은 10번의 실험 동안 사용할 메모리 복사 영역의 크기이다. 각각 N번째 라운드마다 `2^(N+2) ~ 2^(N+3)`의 범위를 주어 선택하게 한다. 간단하게 실험을 10번 하기만 하면 되는데, 자꾸 4라운드 5라운드에서 부터 프로그램이 세그폴트가 나서 `memcpy`가 비정상적으로 종료된다는 것이다...?

## 풀이

이 문제는 취약점을 응용하는 문제가 아니다. `fast_memcpy` 함수에 있는 인라인 어셈블리를 보도록 하겠다.

```assembly
__asm__ __volatile__ (
"movdqa (%0), %%xmm0\n"
"movdqa 16(%0), %%xmm1\n"
"movdqa 32(%0), %%xmm2\n"
"movdqa 48(%0), %%xmm3\n"
"movntps %%xmm0, (%1)\n"
"movntps %%xmm1, 16(%1)\n"
"movntps %%xmm2, 32(%1)\n"
"movntps %%xmm3, 48(%1)\n"
::"r"(src),"r"(dest):"memory");
dest += 64;
src += 64;
```

나 같은 경우에는 이 문제를 고등학교 1학년 때인가? 그 때 처음 접해봤는데 그 때는 [인라인 어셈블리](https://wiki.kldp.org/KoreanDoc/html/EmbeddedKernel-KLDP/app3.basic.html)가 뭔지 저 처음보는 [명령어](https://3dmpengines.tistory.com/1807?category=774908)(`movdqa`, `movntps`)는 뭔지 몰랐다. 저 명령어는 SIMD 연산을 할 때 사용하는 명령어 이다. 메모리 조작이나 연산 같은걸 좀 더 빨리 할 수 있도록 정렬된 메모리에서 수행하는 게 SIMD 연산인데, 나중에 실험 결과를 보면 그냥 메모리를 하나하나 복사하는 것보다 SIMD 연산으로 메모리를 복사하는 것이 몇 백배는 빠른 것을 확인할 수 있다. 저기 위에 링크 걸린 블로그에 좀더 세부적으로 설명이 되어 있다. 우리가 그 중에서 주목할 곳은 이 부분이다.

> movdqa
> 
> a : align  : 메모리가 정렬된 상태로 정렬돈 메모리를 레지스터로 복사 시킬때에는 16개의 바이트의 메모리가 모두 붙어 있기 때문에 캐쉬에서 레지스터로 옮길때 부하없이 로드할 수 있다 (하단 그림 참조)

SIMD 연산의 기본 전제는 `메모리가 정렬된 상태`이다. 소스 코드를 보면 인라인 어셈블리로 메모리 복사를 수행할 뿐, 메모리를 정렬하는 작업은 없다. 그래서 `fast_memcpy`함수가 처음엔 잘 되는데 이후에는 메모리가 정렬이 안되어 있는지 세그폴트가 발생하는 것이다.

실험 전 메모리 공간 크기를 조정할 때 좀 요리조리 맞춰 끼우면 될것 같다. 이를 위해 소스코드 맨 위의 주석처럼 프로그램을 빌드해서 디버거로 잘 살펴봤는데...

```assembly
specify the memcpy amount between 64 ~ 128 : 64
specify the memcpy amount between 128 ~ 256 : 128
...
EDX  0x804c460 ◂— 0x0
0x80487b9 <fast_memcpy+33>    movdqa xmm0, xmmword ptr [eax]
...
EDX  0x804c4a8 ◂— 0x0
0x80487b9 <fast_memcpy+33>    movdqa xmm0, xmmword ptr [eax]
```

저렇게 64바이트 크기 메모리 공간을 복사할 때는 `dest`가 `0x804c460`, 16바이트 단위로 정렬되어 있다. 그런데 128바이트 크기 메모리 공간을 복사할 때는 `dest`가 `0x804c4a8`로 정렬이 안되어 있는 걸 확인 할 수 있다. 그래서 `malloc`으로 메모리 공간을 할당 받을 때 64바이트에서 8바이트를 늘리면 뒤에 128바이트로 실험 할때도 정렬이 되게 된다. 이와 같은게 전체 실험에 해당되서 64바이트 부터 `최소 범위+8`값으로 입력을 하게 되면 실험을 성공적으로 끝낼 수 있다!