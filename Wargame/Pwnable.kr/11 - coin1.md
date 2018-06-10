# coin1 - 6 pt

```text
Mommy, I wanna play a game!
(if your network response time is too slow, try nc 0 9007 inside pwnable.kr server)

Running at : nc pwnable.kr 9007
```

## 근데 대체 머하라는 거지

```text
        ---------------------------------------------------
        -              Shall we play a game?              -
        ---------------------------------------------------

        You have given some gold coins in your hand
        however, there is one counterfeit coin among them
        counterfeit coin looks exactly same as real coin
        however, its weight is different from real one
        real coin weighs 10, counterfeit coin weighes 9
        help me to find the counterfeit coin with a scale
        if you find 100 counterfeit coins, you will get reward :)
        FYI, you have 30 seconds.

        - How to play -
        1. you get a number of coins (N) and number of chances (C)
        2. then you specify a set of index numbers of coins to be weighed
        3. you get the weight information
        4. 2~3 repeats C time, then you give the answer

        - Example -
        [Server] N=4 C=2        # find counterfeit among 4 coins with 2 trial
        [Client] 0 1            # weigh first and second coin
        [Server] 20                     # scale result : 20
        [Client] 3                      # weigh fourth coin
        [Server] 10                     # scale result : 10
        [Client] 2                      # counterfeit coin is third!
        [Server] Correct!

        - Ready? starting in 3 sec... -
```


netcat으로 연결하면 게임을 할 수 있다. 게임을 이기려면 동전들 중에서 위조된 동전을 찾아내면 된다. 진짜 동전과 위조된 동전은 구별하는 방법은 무게로, 진짜 동전은 10의 무게를 가지고 있고 가짜 동전은 9의 무게를 가진다. 게임 플레이어는 무게를 측정하고 싶은 동전을 서버에 보내면 서버는 해당 동전들의 무게 합을 다시 보낸다. 이렇게 위조 동전을 찾는 걸 30초 내에 **100번** 하면 된다!

30초 안에 사람이 어떻게 할까. 코딩해야지

```python
import socket, time

t = ("pwnable.kr", 9007)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(t)

data_intro = s.recv(2000).decode("utf-8")
print(data_intro)
time.sleep(3)

while True:
    data_prob = s.recv(1000).decode("utf-8")
    print(data_prob)
    if "time expired!" in data_prob:
        exit(-1)

    N, C = [int(d.split('=')[1]) for d in data_prob.split()]
    deviant_range = [0, N-1]
    ans = None
    pv = None

    for i in range(C):
        selector = (deviant_range[0] + deviant_range[1]) // 2
        deviant_num = selector-deviant_range[0]
        if deviant_range[0] == selector:
            payload = "{}\n".format(deviant_range[0])
        else:
            payload = ' '.join([str(p) for p in range(deviant_range[0], selector)]) + '\n'
        payload = payload.encode('utf-8')
        s.send(payload)
        data_ans = int(s.recv(1000).decode("utf-8"),10)
        # print("{}th QUERY: {}~{} = {}".format(i+1, deviant_range[0], selector-1, data_ans))
        pv = deviant_range[0]
        if data_ans == 9:
            # print("ANSWER = {}".format(payload.decode('utf-8')), end='')
            ans = payload
        elif data_ans != deviant_num*10:
            deviant_range = [deviant_range[0], selector] 
        else:
            deviant_range = [selector, deviant_range[1]]

    if ans is not None:
        s.send(ans)
        print(s.recv(1000).decode('utf-8'))
    else:
        pv = pv + 1
        print("Eww.. pv is {} but...".format(pv))
        s.send("{}\n".format(pv).encode('utf-8'))
        print(s.recv(1000).decode('utf-8'))
```

간단하게 이진 탐색으로 위조 동전을 찾는 알고리즘을 구현한다. 참 쉽죠?

## 그래서

```text
N=605 C=10

Correct! (99)

Congrats! get your flag
b1NaRy_S34rch1nG_1s_3asy_p3asy
```