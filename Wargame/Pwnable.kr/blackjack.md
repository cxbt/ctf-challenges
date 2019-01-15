# blackjack - 1 pt

```text
Hey! check out this C implementation of blackjack game!
I found it online
* http://cboard.cprogramming.com/c-programming/114023-simple-blackjack-program.html

I like to give my flags to millionares.
how much money you got?


Running at : nc pwnable.kr 9009
```

연결하면 블랙잭을 할 수 있다. ...뭐 그거 말곤 다른거 없는듯

## 중요한 부분만 짚고 넘어가자

```c
// Line 721
int betting() //Asks user amount to bet
{
 printf("\n\nEnter Bet: $");
 scanf("%d", &bet);
 
 if (bet > cash) //If player tries to bet more money than player has
 {
        printf("\nYou cannot bet more money than you have.");
        printf("\nEnter Bet: ");
        scanf("%d", &bet);
        return bet;
 }
 else return bet;
} // End Function
```

문제에서 제공된 블랙잭 소스를 살펴보면 많은 부분이 하드코딩 된걸 확인 할 수 있다. 우리가 돈을 부풀리기 위해 사용할 부분의 위의 코드이다. 일단 베팅할 돈을 입력 받고 만약 베팅한 돈이 소유하고 있는 돈보다 많으면 다시 잡아서 베팅할 돈을 입력 받는다. 그런데 웃긴점은 2번째로 입력값에 대한 유효성 검사를 하지 않는 다는 것이다. 여기서 우리는 말도 안되는 금액을 베팅할 수 있게 된다ㅋ

## 그래서

```text
Cash: $500
-------
|D    |
|  6  |
|    D|
-------

Your Total is 6

The Dealer Has a Total of 6

Enter Bet: $1000

You cannot bet more money than you have.
Enter Bet: 1000000


Would You Like to Hit or Stay?
Please Enter H to Hit or S to Stay.
H
-------
|S    |
|  Q  |
|    S|
-------

Your Total is 16

The Dealer Has a Total of 13

Would You Like to Hit or Stay?
Please Enter H to Hit or S to Stay.
H
-------
|H    |
|  7  |
|    H|
-------

Your Total is 23

The Dealer Has a Total of 23
Dealer Has Went Over!. You Win!

You have 1 Wins and 0 Losses. Awesome!

Would You Like To Play Again?
Please Enter Y for Yes or N for No
Y
YaY_I_AM_A_MILLIONARE_LOL


Cash: $1000500
-------
|C    |
|  1  |
|    C|
-------

Your Total is 1

The Dealer Has a Total of 7
```