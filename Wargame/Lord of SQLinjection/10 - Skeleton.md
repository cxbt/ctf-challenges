# Level 10 - Skeleton

## 문제

![문제](screenshot/L10_Skeleton_prob.PNG)

## 문제 의도

- php 소스를 읽을 줄 아는가?

## 코드 분석

```php
<?php
  include "./config.php";
  login_chk();
  dbconnect();
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");
  $query = "select id from prob_skeleton where id='guest' and pw='{$_GET[pw]}' and 1=0";
  echo "<hr>query : <strong>{$query}</strong><hr><br>";
  $result = @mysql_fetch_array(mysql_query($query));
  if($result['id'] == 'admin') solve("skeleton");
  highlight_file(__FILE__);
?>
```

## 문제 풀이

솔직히 이 문제는 그동안 배워온 방법을 쓰면 되게 쉽게 풀린다. 문제 만든 사람이 뭘 유도하려고 했는지 잘 모르겠다. **or 1** 로 모든 레코드를 가져온뒤 **and id='admin'** 으로 id필드가 'admin'인 레코드를 가져오도록 하고 **-- -** 로 뒤의 where 조건문을 무력화 시키면 된다.

![solve](screenshot/L10_Skeleton_clear.PNG)