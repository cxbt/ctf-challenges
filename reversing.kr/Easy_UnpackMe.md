# Easy UnpackMe

## 문제

- 첨부파일
  - "Easy_UnpackMe.exe" PE32 executable (GUI) Intel 80386, for MS Windows
  - ReadMe.txt
- 목표 : OEP 찾기?
- 사용 도구 : OllyDbg v1.10

![1](screenshots/Easy_UnpackMe_1.PNG)

## 풀이

OEP는 `Original Entry Point`의 약자로 프로그램 코드의 맨 처음 시작점을 의미한다. 이번 문제는 OEP를 찾아서 인증하면 될것같다. 설정을 바꾸지 않았다면 일반적으로 디버거는 각 Module Entry 마다 중단점을 설정하기 때문에 실행파일에 이상한게 없다면 `Easy_UnpackMe` 모듈에 들어갈때 처음 주소를 OEP로 찾을 수 있을 것이다. 그런데...

![2](screenshots/Easy_UnpackMe_2.PNG)

디버거 마저 "이 바이너리는 PE헤더에 명시된 코드 영역 바깥쪽에 OEP가 설정되어 있습니다! 아마도 이 파일은 스스로 압축 해제 하거나 수정하는 것 같네요!" 라고 알려준다. OEP를 찾으려면 프로그램 자체가 압축을 해제해야 할 것 같다.

```assembly
0040A08F       B9 00904000      MOV ECX,Easy_Unp.00409000
0040A094       BA EE944000      MOV EDX,Easy_Unp.004094EE
0040A099       3BCA             CMP ECX,EDX
0040A09B       74 26            JE SHORT Easy_Unp.0040A0C3
0040A09D       8031 10          XOR BYTE PTR DS:[ECX],10
0040A0A0       41               INC ECX
0040A0A1       3BCA             CMP ECX,EDX
0040A0A3       74 1E            JE SHORT Easy_Unp.0040A0C3
0040A0A5       8031 20          XOR BYTE PTR DS:[ECX],20
0040A0A8       41               INC ECX
0040A0A9       3BCA             CMP ECX,EDX
0040A0AB       74 16            JE SHORT Easy_Unp.0040A0C3
0040A0AD       8031 30          XOR BYTE PTR DS:[ECX],30
0040A0B0       41               INC ECX
0040A0B1       3BCA             CMP ECX,EDX
0040A0B3       74 0E            JE SHORT Easy_Unp.0040A0C3
0040A0B5       8031 40          XOR BYTE PTR DS:[ECX],40
0040A0B8       41               INC ECX
0040A0B9       3BCA             CMP ECX,EDX
0040A0BB       74 06            JE SHORT Easy_Unp.0040A0C3
0040A0BD       8031 50          XOR BYTE PTR DS:[ECX],50
0040A0C0       41               INC ECX
0040A0C1       EB D6            JMP SHORT Easy_Unp.0040A099
```

계속 XOR로 뭔가를 디코딩 하다가 `00401150`로 뛰게 되는데 보니까 함수 프롤로그다!