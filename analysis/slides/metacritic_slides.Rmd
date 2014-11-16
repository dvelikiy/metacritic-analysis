---
title       : Описательный анализ данных Metacritic
subtitle    : 
author      : Великий Дмитрий Павлович
job         : Университет ИТМО
framework   : io2012        # {io2012, html5slides, shower, dzslides, ...}
#highlighter : highlight.js  # {highlight.js, prettify, highlight}
#hitheme     : tomorrow      # 
widgets     : []            # {mathjax, quiz, bootstrap}
mode        : selfcontained # {standalone, draft, selfcontained}
---

<style>
.title-slide {
  background-color: #FFFFFF; /* #EDE0CF; ; #CA9F9D*/
}
</style>

<!-- Limit image width and height -->
<style type='text/css'>
img {
    max-height: 560px;
    max-width: 964px;
}
</style>

<!-- Center image on slide -->
<script src="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-1.7.min.js"></script>
<script type='text/javascript'>
$(function() {
    $("p:has(img)").addClass('centered');
});
</script>

## О Metacritic 


![](http://www.metacritic.com/images/modules/about_metascores.png)

---
## Система агрегирования оценок
- Оценка пользователей (user score) = среднее арифметическое
- Оценка критиков (metascore) = взвешенное среднее

---
## Гипотезы
1. ОП и ОК значительно расходятся в большинстве случаев
2. В среднем, чем раньше выпущена игра, тем выше её оценка

--- #custbg 
<style>
#custbg {
  background-image:url(http://i.imgur.com/pt9kPjz.png); 
  background-repeat: no-repeat;
  background-position: center center;
  background-size: contain;
  text-shadow: 2px 0 0 #fff, -2px 0 0 #fff, 0 2px 0 #fff, 0 -2px 0 #fff, 1px 1px #fff, -1px -1px 0 #fff, 1px -1px 0 #fff, -1px 1px 0 #fff;
}
</style>
## Сбор данных
