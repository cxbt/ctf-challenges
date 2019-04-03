# DB is really GOOD

## 문제

```
What kind of this Database?

you have to find correlation between user name and database.
```

## 풀이

어떤 아이디를 입력하면 `Hello, blahblah` 와 함께 메모장 같은 웹페이지가 나온다.

아이디를 `admin`으로 치고 들어가면 `dont access with 'admin'`이라고 뜨고 페이지가 넘어가지 않는다. 이는 사실 클라이언트 단에서 JS로 막는 것이기 때문에 상관없이 들어갈 수 있다. 문제는 `admin`의 메모장 파일이 뭔지 알아야 한다.

아이디 입력란에 `./`를 입력하면 다음과 같이 에러가 뜬다.

```
Fatal error: Uncaught exception 'Exception' with message 'Unable to open database: unable to open database file' in /var/www/html/db_is_really_good/sqlite3.php:7 Stack trace: #0 /var/www/html/db_is_really_good/sqlite3.php(7): SQLite3->open('./db/wkrm__/.db') #1 /var/www/html/db_is_really_good/memo.php(14): MyDB->__construct('./db/wkrm__/.db') #2 {main} thrown in /var/www/html/db_is_really_good/sqlite3.php on line 7
```

이 디렉토리 안에 `db`란 이름의 디렉토리가 있다. 주소창에 `db` 치고 들어가면 디렉토리가 나열되어 있는 것을 볼 수 있다. 여기서 `admin`의 DB 파일을 찾아 열어보면 플래그를 확인할 수 있는 링크를 볼 수 있다.