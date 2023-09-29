# anyrss
Turn web page to RSS.

## Ideas

1. Fetch HTML from url
2. Use Xpath (save to config) to extract info and build RSS feed
3. That's it!

## Build & run
Rename `config.py.sample` to `config.py`
```
docker build -t anyrss .
mkdir db
docker run -it --rm -p 5000:5000 -v $(pwd)/db:/app/instance anyrss
```

Remember to backup your DB

## Example
This is example config for URL: https://github.com/advisories?query=severity%3Acritical+type%3Aunreviewed

```yaml
base: 'body/div[1]/div[4]/main/div/div[2]/div[2]/div[2]/div'
link: './div/div/div/a/@href'
guid: './div/div/div/a/@href'
title: './div/div/div/a/text()'
description: './div/div/div/a/text()'
date: './div/div/div/div/relative-time/@datetime'
tag:  './div/div/div/span[1]'
link_prefix: 'https://github.com'
date_format: '%Y-%m-%dT%H:%M:%SZ'
```

With slug `gh-unreviewed-critical`, RSS feed can be access at: http://localhost/rss/gh-unreviewed-critical

## Screenshoots

![](https://i.imgur.com/b5WuKA0.png)
![](https://i.imgur.com/iX7zsIG.png)
![](https://i.imgur.com/l3LonZ6.png)

## Roadmap

- [ ] Support SPA pages by https://www.browserless.io/
- [ ] Filter entry to include, exclude by keywords