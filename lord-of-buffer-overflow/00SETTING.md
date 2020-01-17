# Setting LOB

## Root 계정
```
ID : root
PW : hacherschoolbof 
```

## Switching shell 'bash' to 'bash2'

LOB 모든 계정은 `bash`가 기본 쉘로 되어 있는데 `\xff`와 같은 바이트가 `null`, `\x00`으로 인식되어서 되지도 않는 곳에서 무한 삽질을 할 수 있다.

`/etc/passwd`에서 모든 사용자에 대해 기본 쉘을 `bash2`로 바꾸자! 바꾸려면 당연히 루트 계정으로 들어가야 한다;

```sh
vi /etc/passwd

root:x:0:0:root:/root:/bin/bash2
bin:x:1:1:bin:/bin:
daemon:x:2:2:daemon:/sbin:
adm:x:3:4:adm:/var/adm:
lp:x:4:7:lp:/var/spool/lpd:
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/spool/mail:
news:x:9:13:news:/var/spool/news:
uucp:x:10:14:uucp:/var/spool/uucp:
operator:x:11:0:operator:/root:
games:x:12:100:games:/usr/games:
gopher:x:13:30:gopher:/usr/lib/gopher-data:
nobody:x:99:99:Nobody:/:
xfs:x:43:43:X Font Server:/etc/X11/fs:/bin/false
named:x:25:25:Named:/var/named:/bin/false
postgres:x:26:26:PostgreSQL Server:/var/lib/pgsql:/bin/bash2
gate:x:500:500::/home/gate:/bin/bash2
gremlin:x:501:501::/home/gremlin:/bin/bash2
cobolt:x:502:502::/home/cobolt:/bin/bash2
goblin:x:503:503::/home/goblin:/bin/bash2
orc:x:504:504::/home/orc:/bin/bash2
wolfman:x:505:505::/home/wolfman:/bin/bash2
darkelf:x:506:506::/home/darkelf:/bin/bash2
orge:x:507:507::/home/orge:/bin/bash2
troll:x:508:508::/home/troll:/bin/bash2
vampire:x:509:509::/home/vampire:/bin/bash2
skeleton:x:510:510::/home/skeleton:/bin/bash2
golem:x:511:511::/home/golem:/bin/bash2
darkknight:x:512:512::/home/darkknight:/bin/bash2
bugbear:x:513:513::/home/bugbear:/bin/bash2
giant:x:514:514::/home/giant:/bin/bash2
assassin:x:515:515::/home/assassin:/bin/bash2
zombie_assassin:x:516:516::/home/zombie_assassin:/bin/bash2
succubus:x:517:517::/home/succubus:/bin/bash2
nightmare:x:518:518::/home/nightmare:/bin/bash2
xavius:x:519:519::/home/xavius:/bin/bash2
death_knight:x:520:520::/home/death_knight:/bin/bash2
:%s/bash/bash2/
```

## 참고 사이트
- [오늘도 걷는다 :: [BOF원정대] LEVEL1 (gate -> gremlin)](http://ddubucker.tistory.com/entry/BOF%EC%9B%90%EC%A0%95%EB%8C%80-LEVEL1-gate-gremlin-simple-bof)
- [BOF 원정대 간단풀이](https://docs.google.com/document/d/1DaTxDdOsvZk39LLdO6qLoywEbiNAHU32nKajpdxX_Wg/edit)