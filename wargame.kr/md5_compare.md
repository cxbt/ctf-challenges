# md5_compare

## 문제

```
JUST COMPARE ONLY.

with the other value :D
```

## 풀이

입력 값이 2개가 있는데, 하나는 Alphabet만, 하나는 숫자만을 받아서 각각의 md5 해시값을 구해 해시값이 같으면 통과할 수 있다.

```php
if (!ctype_alpha($v1)) {$chk = false;}
if (!is_numeric($v2) ) {$chk = false;}
if (md5($v1) != md5($v2)) {$chk = false;}
```

감사하게도 php.net [매뉴얼](https://www.php.net/manual/en/function.md5.php)에 있는 `md5` 함수에 대한 문서에서 댓글 중 하나가 친절하게도 Type Juggling 예시를 알려준다. 문자열 `0e12341234`은 PHP에 의해 숫자로 인식되어 0^12341234 로 표현된다. 0은 당연히 몇 제곱을 하든 0이기 때문에 `0e`로 시작하는 모든 문자열은 다 0으로 표현된다. 

그냥 나오는 예시를 입력하면 된다ㅋ