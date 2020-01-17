# already got

## 문제

```
can you see HTTP Response header?
```

## 풀이

문제에 들어가보면 `you've already got key! :p` 라고 말한다.

문제 설명 처럼 HTTP Response 헤더를 보면 플래그를 찾을 수 있다.

```
HTTP/1.1 200 OK
Date: Tue, 02 Apr 2019 07:27:21 GMT
Server: Apache/2.4.18 (Ubuntu)
FLAG: 0809d597ca3eb29a3c***************753297f
Content-Length: 27
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: text/html; charset=UTF-8
```