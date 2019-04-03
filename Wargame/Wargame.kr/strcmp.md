# strcmp

## 문제

```
if you can bypass the strcmp function, you get the flag.
```

## 풀이

입력값과 `sha1(md5(rand().file_get_contents("/var/lib/dummy_file")).rand())` 값을 `strcmp`에 집어 넣었을 때 `0`이 나오면 된다.

```php
<?php
    require("../lib.php"); // for auth_code function

    $password = sha1(md5(rand().file_get_contents("/var/lib/dummy_file")).rand());

    if (isset($_GET['view-source'])) {
        show_source(__FILE__);
        exit();
    }else if(isset($_POST['password'])){
        sleep(1); // do not brute force!
        if (strcmp($_POST['password'], $password) == 0) {
            echo "Congratulations! Flag is <b>" . auth_code("strcmp") ."</b>";
            exit();
        } else {
            echo "Wrong password..";
        }
    }

?>
```

PHP 버전마다 다르지만, `strcmp` 함수에서 [배열과 문자열을 비교](https://hackability.kr/entry/PHP-strcmp-%EC%B7%A8%EC%95%BD%EC%A0%90%EC%9D%84-%EC%9D%B4%EC%9A%A9%ED%95%9C-%EC%9D%B8%EC%A6%9D-%EC%9A%B0%ED%9A%8C)하게 되면 `NULL`을 반환하게 된다. 그리고 `NULL`과 `0`은 PHP 특유의 Loose Comparison에서 같다고 표현된다.

Request를 서버에 보낼 때 배열처럼 보내려면 아래와 같이 중괄호를 파라미터 끝에 써주면 된다.

```php
password=asdfasdf -> password[]=asdfasdf
```

그렇게 되면 위에서 설명한 바와 같이 `strcmp`를 우회할 수 있다.