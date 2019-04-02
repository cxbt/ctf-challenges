# QR CODE PUZZLE

## 문제

```
javascript puzzle challenge

just enjoy!
```

## 풀이

문제에 들어가보면 아마 QR코드 그림이었을 것 같은 슬라이드 퍼즐이 보인다.

이걸 맞추면 될거 같긴한데 귀찮으니까 소스를 봐서 원본 그림을 찾자.

```html
<div class="jqp-piece" style="width: 81px; height: 81px; background-image: url(&quot;./img/qr.png&quot;); border-width: 0px; margin: 0px; padding: 0px; position: absolute; overflow: hidden; display: block; visibility: inherit; cursor: default; left: 415px; top: 83px; background-position: 0px -83px;" current="11">
    <span style="display: none;">7</span>
</div>
```

퍼즐 한 조각을 보면 `background-image` 속성이 보인다. 저 속성 값 URL로 들어가면 원본 QR코드 그림이 나오고, 원본 QR 코드 그림을 인식하면 된다.