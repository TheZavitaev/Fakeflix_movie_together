* Запись 100 млн объектов в ClickHouse заняла: 0:04:46
* Запись 100 млн объектов в Vertica заняла: 0:10:33
___
* Чтение 100 тыс объектов по movie_id в ClickHouse занивает в среднем 1,3 сек
* Чтение 100 тыс объектов по movie_id в Vertica занивает в среднем 1,5 сек
___
Стоит отметить, что разница в скорости чтения не столь очевидна, как на запись. 
В тоже время, перед нами стоит задача собирать генерируемую пользователями информацию о поведении, которая имеет свойство расти:
- сегодня то, как пользователи смотрят фильмы
- завтра лайки
- послезавтра заходы на страницу другого пользователя
- далее данные о том, что человек прочитал описание к фильму и стал\не стал его смотреть
- и т.д.

Следовательно, запись будет приоритетнее со временем, а значит, выбор ClickHouse обоснован.
___
Примеры аналитических запросов для сравнения:
____
```
CH> SELECT
    user_id,
    sum(viewed_frame),
    max(viewed_frame)
    FROM analytics.regular_table
    GROUP by user_id
[2021-11-17 03:01:25] 500 rows retrieved starting from 1 in 620 ms (execution: 589 ms, fetching: 31 ms)
```
```
V> SELECT
    user_id,
    sum(viewed_frame),
    max(viewed_frame)
    FROM public.views
    GROUP by user_id
[2021-11-17 03:02:46] 500 rows retrieved starting from 1 in 1 s 144 ms (execution: 1 s 93 ms, fetching: 51 ms)
```
____
```
CH> SELECT avg(movies_watched)
    FROM (
    SELECT count(movie_id) as movies_watched
    FROM analytics.regular_table
    GROUP BY user_id
    ) AS movies_count
[2021-11-17 03:06:44] 1 row retrieved starting from 1 in 788 ms (execution: 757 ms, fetching: 31 ms)
```
```
V> SELECT avg(movies_watched)
    FROM (
    SELECT count(movie_id) as movies_watched
    FROM public.views
    GROUP BY user_id
    ) AS movies_count
[2021-11-17 03:07:56] 1 row retrieved starting from 1 in 719 ms (execution: 688 ms, fetching: 31 ms)
```
___
```
CH> SELECT avg(viewed_frame) FROM analytics.regular_table
[2021-11-17 03:09:35] 1 row retrieved starting from 1 in 114 ms (execution: 95 ms, fetching: 19 ms)
```
```
V> SELECT avg(viewed_frame) FROM public.views
[2021-11-17 03:10:13] 1 row retrieved starting from 1 in 438 ms (execution: 412 ms, fetching: 26 ms)
```
____
```
CH> SELECT user_id, sum(viewed_frame) AS view_time  
    FROM analytics.regular_table
    GROUP BY user_id 
    ORDER BY view_time DESC 
    LIMIT 10
[2021-11-17 03:11:25] 10 rows retrieved starting from 1 in 633 ms (execution: 606 ms, fetching: 27 ms)
```
```
V> SELECT user_id, sum(viewed_frame) AS view_time  
    FROM public.views
    GROUP BY user_id 
    ORDER BY view_time DESC 
    LIMIT 10
[2021-11-17 03:11:53] 10 rows retrieved starting from 1 in 683 ms (execution: 652 ms, fetching: 31 ms)
```
___
```
CH> SELECT movie_id, max(viewed_frame) AS view_time
    FROM analytics.regular_table
    GROUP BY movie_id
    ORDER BY view_time DESC
    LIMIT 50
[2021-11-17 03:13:55] 50 rows retrieved starting from 1 in 553 ms (execution: 533 ms, fetching: 20 ms)
```
```
V> SELECT movie_id, max(viewed_frame) AS view_time
    FROM views
    GROUP BY movie_id
    ORDER BY view_time DESC
    LIMIT 50
[2021-11-17 03:14:16] 50 rows retrieved starting from 1 in 971 ms (execution: 952 ms, fetching: 19 ms)
```
____

```
CH> SELECT count(DISTINCT movie_id) FROM analytics.regular_table
[2021-11-17 03:15:34] 1 row retrieved starting from 1 in 825 ms (execution: 781 ms, fetching: 44 ms)
```
```
V> SELECT count(DISTINCT movie_id) FROM public.views
[2021-11-17 03:15:54] 1 row retrieved starting from 1 in 824 ms (execution: 803 ms, fetching: 21 ms)
```
___
```
CH> SELECT count(DISTINCT user_id) FROM analytics.regular_table
[2021-11-17 03:16:21] 1 row retrieved starting from 1 in 806 ms (execution: 777 ms, fetching: 29 ms)
```
```
V> SELECT count(DISTINCT user_id) FROM views
[2021-11-17 03:16:31] 1 row retrieved starting from 1 in 606 ms (execution: 575 ms, fetching: 31 ms)
```
