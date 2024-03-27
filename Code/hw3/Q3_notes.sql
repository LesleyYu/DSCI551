USE CINEMA;

-- 1) 
-- Find titles of the longest movies. Note that there might be more than such movie.
select title from Movies where length = (select max(length) from Movies);



-- 2) 
-- Find out titles of movies that contain "Twilight" and are directed by "Steven Spielberg".
  -- method 1:
select title from Movies 
  where 
  title like '%Twilight%' and
  id in (
      select movie_id from DirectedBy left outer join Directors d
        on director_id=d.id
          where d.name = "Steven Spielberg"
  );

  -- method 2:
  -- select title from Movies 
  --   where 
  --   title like '%Twilight%' and
  --   id in (
  --     select movie_id from DirectedBy where 
  --       director_id = (
  --         select id from Directors where name = "Steven Spielberg"
  --       )
  --   );




-- 3) 
-- Find out how many movies "Tom Hanks" has acted in.
select name, count(*) as movies_count 
  from ActIn left outer join Actors 
  on id = actor_id
  where name = 'Tom Hanks';




-- 4) 
-- Find out which director directed only a single movie.
  -- method 1:
-- 分析：
-- 表：1）Directors， 2）DirectedBy
-- 从 DirectedBy 获取只导一个电影的导演后， 拿到它对应的name，选中它的name进行返回
-- 这两个方法的区别是：
-- 不用 having 就不能直接拿到 count(*) 的值， 必须得在select 里面写出来，这就造成：
-- 不能直接用 id in (subquery) 这个句子，因为 in 前后的值对不上
-- 所以我们必须要先join两个table之后才能拿到name，拿到之后还带有 count(*)，还得再在外面写一层，就很麻烦。
select name from (
  select name, count(*) as movies_count from 
  Directors right outer join DirectedBy on director_id = id
  group by name
) as d 
where d.movies_count = 1;

  -- method 2:
-- 从 DirectedBy 获取只导一个电影的导演后， 拿到它对应的id，选中它在 Directors 对应的name进行返回
select name from Directors where id in (
  select director_id from DirectedBy group by director_id having count(*) = 1
);




-- 5) 
-- Find titles of movies which have the largest number of actors. Note that there may be multiple such movies.

    -- method 1:
    -- 分析：需要从ActIn和Movies这两个表中获取信息，其中ActIn要先获取那个最大的演员数量，
    -- 得到那个数量后再通过ActIn来获得movies_id，
    -- 再从Movies对应的id获得title。
      -- 这里我们用 >= all (subquery) 来获得最大的演员数量.
      -- 在对应到 group by 过的subquery里，找到对应的movies_id
  select title from Movies where id in (
    select movie_id from (
      select movie_id, count(*) as actors_count from ActIn group by movie_id
    ) as x1 where
      actors_count >= all (
        select count(*) from ActIn group by movie_id
      )
  );

  -- method 2:
select title from Movies where id in (
  select movie_id from ActIn group by movie_id having count(*) = (
    select max(actors_count) from (
      select count(*) as actors_count from ActIn group by movie_id
    ) as counts
  )
);

  -- method 3:
  -- 这里我们从subquery获取数量，再通过join两个表来获得title
  -- 这个方法逻辑最清晰
select title from Movies join ActIn on movie_id = id group by title having count(*) = (
  select count(*) from ActIn group by movie_id order by count(*) desc limit 1
);




-- 6) Find names of actors who played in both English (language = "en") and French ("fr") movies.

select name from Actors a 
join ActIn ai on a.id = ai.actor_id 
join Movies m on ai.movie_id = m.id where 
  language = 'fr' and actor_id in (
    select ai.actor_id from ActIn ai join Movies m on ai.movie_id = m.id where
      language = 'en'
  );

select name from Actors a
join ActIn ai on a.id = ai.actor_id
join Movies m on ai.movie_id = m.id where
language in ('en', 'fr')
group by a.name
having count(distinct language) = 2;



-- 7) Find names of directors who only directed English movies.
select d.name from Directors d 
join DirectedBy db on d.id = db.director_id
join Movies m on db.movie_id = m.id
group by d.id
having count(distinct m.language) = 1;