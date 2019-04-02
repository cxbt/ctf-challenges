# fly me to the moon

## 문제

```
javascript game.

can you clear with bypass prevent cheating system?
```

## 풀이

문제에 들어가면 비행기 게임이 있는데 플래그를 얻기 위해선 31337점을 채워야 할 것으로 보인다.

솔직히 언제 31337점 채우고 앉아있나, 클라이언트와 서버끼리 보내는 데이터를 잘 보면 죽을 때 클라이언트가 서버로 `high-scores.php`로 POST Request를 보내는 것을 확인할 수 있다. POST Request를 보내면서 폼 데이터로 `token`과 `score`를 보내는데, `score`값을 31337점으로 조작하면 서버가 진짜 그런줄 알고 플래그를 넘긴다.

참고로 `<script>` 태그 안에 있는 자바스크립트 코드를 보면 알 수 없도록 난독화 되어 있다. [`Unpacker`](https://www.strictly-software.com/unpack-javascript)나 [`Javascript Beautifier`](https://beautifier.io/)로 쉽게 난독화를 해제할 수 있다.