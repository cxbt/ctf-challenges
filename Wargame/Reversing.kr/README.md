# Reversing.kr

리버싱 초짜가 쓰는 풀이 보고서.

## 문제 목록

- [Easy Crack](Easy_Crack.md) : 첫번째 문제

### 풀기 전에 생각하면 좋은거

- 입력값은 언제나 `a1b2c3d4e5...`과 같이 위치를 판별할 수 있는 걸로 주면 디버깅 할때 편하다.
- Label을 설정해 놓으면 디버깅 할때 편하다.
- IA-32 Instruction이 헷갈리면 [이 문서](https://www.intel.com/content/dam/www/public/us/en/documents/manuals/64-ia-32-architectures-software-developer-instruction-set-reference-manual-325383.pdf)를 읽어보자.
- Top-Down으로 보면 도움이 될때가 많았다. 계속 파고파다가 ntdll까지 가지말고 넓은 시야에서 봐보자.