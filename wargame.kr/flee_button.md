# flee button

## 문제

```
click the button!

i can't catch it!
```

## 풀이

문제에 들어가보면 `click me!` 란 버튼이 커서에 안닿게 도망간다.

굳이 버튼을 누를 필요는 없고 소스를 봐서 버튼을 눌렸을 때 이동하는 페이지를 직접 쳐서 들어가면 된다.

```html
<div id="esc" style="position: absolute; left: 701px; top: 206px;">
    <input type="button" onfocus="nokp();" onclick="window.location='?key=ee4b';" value="click me!">
</div>
```

여기선 버튼을 클릭하면 `?key=ee4b`로 이동하니 직접 쳐서 들어가면 된다. 