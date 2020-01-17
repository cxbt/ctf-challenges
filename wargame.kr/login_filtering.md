# login filtering

## 문제

```
I have accounts. but, it's blocked.

can you login bypass filtering?
```

## 풀이

문제에 들어가면 로그인 폼과 PHP 소스를 볼 수 있다.

```php
<?php
... 
  $row=mysql_fetch_array(mysql_query("select * from user where id='$id' and ps=md5('$ps')"));

  if(isset($row['id'])){
   if($id=='guest' || $id=='blueh4g'){
    echo "your account is blocked";
   }else{
    echo "login ok"."<br />";
    echo "Password : ".$key;
   }
  }else{
   echo "wrong..";
  }
...
?>

<!--

you have blocked accounts.

guest / guest
blueh4g / blueh4g1234ps

-->
```

로그인 할수 있는 계정이 주어져 있는 것 같긴 한데 아예 조건문으로 주어진 계정을 막아버린다.

MySQL이나 MSSQL은 기본적으로 쿼리에서 **대소문자 구별을 하지 않는다**(case-insensitive). 그렇기 때문에 `guest`가 아닌 `GUEST`로 ID를 주고 로그인을 하면 쿼리 결과값도 나오고 조건문도 쉽게 통과할 수 있다.