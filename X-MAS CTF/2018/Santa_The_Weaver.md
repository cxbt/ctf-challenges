# Santa The Weaver

## Challenge Description

50

Santa LOVES two things! Weaving and ...

Author: Vlad

## Solution

### flag.zip

![1](screenshots/Santa_The_Weaver_1.PNG)

The ZIP file contains `flag.png`. It's a picture of christmas tree and X-MAS CTF. Oh, and by the way, Merry Christmas to you all.

So basically it's just a picture. We need to find flag in this picture.

Basically, most of window iamge viewers render image within [Image Format](https://en.wikipedia.org/wiki/Image_file_formats). It simply ignores data in outbound of image format. So if we put any data after the end of image file format, it is unseen by normal image viewer but yet saved in the file.

### So how can we see it?

I frequently use Hex Editor to see internals of file, and my favorite one is HxD (There are link below). If we open `flag.png` with HxD and see the last part of the hex data, we can see flag-like string data below.

![2](screenshots/Santa_The_Weaver_2.PNG)

## Thanks to

- Maël Hörz, developer of [HxD](https://mh-nexus.de/en/hxd/).