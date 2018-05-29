# Level 1 - Gremlin

## 문제

![prob](screenshot/L1_Gremlin_prob.PNG)

## 문제 의도

- php 소스를 읽을 줄 아는가?
- 아주 간단한 SQL Injection을 할 수 있는가?

## 코드 분석

```php
<?php
  include "./config.php";
  /* LOS 사이트의 공통으로 사용되는 함수들을 넣어놓은 라이브러리를 include 하는 것 같다.
     아랫줄에 나오는 login_chk() 나 dbconnect() 같은 함수들을 정의해 놓았을 것 같다.*/
  login_chk();
  /* 사이트에서 문제를 풀고 있는 사용자의 로그인 상태를 체크하는 함수 인 것 같다.
     이 함수의 기능은 문제 URL에 로그인 하지 않고 각 문제에 접속했을 때 페이지 접근을
     차단 하는 것이라고 추정했다. 실제로 실험해 본 결과 문제 URL로 로그인 과정 없이
     접근할 시엔 문제 페이지가 아닌 los.eagle-jump.org로 리다이렉션 되는 것을
     확인 할 수 있었다. */
  dbconnect();
  /* SQL Injection 대상인 DB에 연결하는 코드가 들어있을 것이라고 예상된다. */
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~");
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");
  /* preg_match() 함수는 정규표현식을 이용해 2번째 인자와 패턴이 매치되는
     횟수를 반환하는 함수이다. 정규표현식을 잘 모르지만 ‘/prob’ '.()/i'와
     같은 문자열을 찾는 식이 아닐까 생각된다. 4, 5번 라인은 GET으로 받은
     id와 pw에서 이 같은 문자열이 들어있는 값을 필터링하는 조건문이 아닐까 생각된다. */
  $query = "select id from prob_gremlin where id='{$_GET[id]}' and pw='{$_GET[pw]}'";
  /* GET으로 받은 id와 pw값을 합쳐 쿼리문을 만들었다. */
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  /* 페이지에서 자신이 만든 쿼리를 보여주는 기능을 하는 코드이다. */
  $result = @mysql_fetch_array(mysql_query($query));
  /* 6번째 라인에서 만든 쿼리를 DB에 보내 결과를 받아오는 코드이다.
     내가 전에 웹 어플리케이션 만들 때 DB에 쿼리를 넣을 때 mysqli_query()로
     쿼리와 객체를 같이 넘겨줬는데 mysql_query()는 config파일에서 정의한
     함수가 아닐까 추측한다. 아무튼 mysql_query()에서 받은 레코드들의 배열
     result 변수에 넘겨주는 것 같다. */
  if($result['id']) solve("gremlin");
  /* 만약 result 변수에 id 필드가 존재한다면 solve("gremlin")을 호출해
     문제를 해결 한 것으로 간주하여 문제 사이트 서버에게 문제 해결 여부를
     알리는 것 같다. */
  highlight_file(__FILE__);
  /* highlight_file() 함수는 인자로 받은 파일의 코드를 php syntax에 알맞게
     코드를 색칠해서 페이지에 프린트 하는 함수로, 여기서는 파일의 전체 경로와
     이름을 포함한 __FILE__ 마법 상수(?)를 넘겨줘서 이 페이지의 소스를 보여준다. */
?>
```

## 문제 풀이

문제의 목적은 result변수의 id 필드 값이 존재하기만 하면 되므로, 쿼리를 통해 어떤 레코드든 가져오기만 하면 된다. id 필드에 **' or 1=1 -- -** 를 넣으면 id필드에는 빈 문자열이 들어가게 되고, 그 뒤에 where 조건문에 **or 1=1** 이 들어가게 되면서 모든 레코드가 조회된다. 뒤의 **--** 는 id 필드 값 이후 쿼리를 주석 처리시키므로 변조한 쿼리가 정상적인 쿼리처럼 바뀌게 된다.

![solve](screenshot/L1_Gremlin_clear.PNG)