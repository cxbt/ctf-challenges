# Content Security Policy

## Stage12

```
X-XSS-Protection: 0
Content-Security-Policy: script-src 'self' 'unsafe-inline'; frame-src 'self'
```

`frame-src`가 self가 되면서 직접적으로 쿠키를 넘겨주는 방법이 막히게 되었다. 그렇다면 인라인 자바스크립트로 `<IMG>` 태그를 생성하면서 `src`를 내 서버와 쿠키값을 넣어 설정한다.

## Stage14

```
X-XSS-Protection: 0
Content-Security-Policy: script-src 'self' 'sha256-6FYe68L0Glf1hGqIn0L6jIYjc+MFEOCqK/DbJ7gxWnk='; frame-src http://*.knock.xss.moe https://*.knock.xss.moe
```

`script-src` 지시부에 `sha256`이 추가되면서 인라인 자바스크립트 조차 막혔다ㅎㅎ 조졌네