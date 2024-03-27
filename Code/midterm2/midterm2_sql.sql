



-- MySQL比较运算符一览表（带解析） https://c.biancheng.net/view/7191.html
-- MySQL HAVING：过滤分组   https://c.biancheng.net/view/7416.html 讲了having 和 where 的使用区别




-- 2017 fall morning 

-- -- 1. 

-- -- 2. 
-- -- -- b.

-- -- -- c.



-- 2017 fall morning 2

-- -- 2.
-- -- -- a.
select a.color, b.manf from Ales a natural Join Beers b
where a.beer_name in (
  select beer_name from Ales
);
-- -- -- -- 答案：
select a.color, b.manf from Ales a natural Join Beers b
where a.beer_name = b.beer_name

-- -- -- b.
select d.drinker_name from Drinker d natural join Likes l
where l.beer_name in (
  select a.beer_name from Ales a
)
-- -- -- -- 答案：
select d.drinker_name from Drinker d, Likes l
where d.drinker_name = l.drinker_name   -- 区别在这里！不用natural join
and l.beer_name in (
  select a.beer_name from Ales a
)

-- -- -- c. 
select distinct b1.manf from Beers b1, Beers b2 
where (
  b1.beer_name <> b2.beer_name and b1.manf = b2.manf
)



-- 2017 fall afternoon

-- -- 2.
-- -- -- a.
select d.name from Drinker d, Beers b 
where d.LikedBeers = d.name
and
d.name = 'Steve'
-- -- -- -- 答案：好傻 不用用俩表啊.而且还返回错了。不是人名是酒名
select LikedBeers as BeerLikedBySteve
from Drinker
where name = 'Steve'

-- -- -- b.
select distinct d.name from Drinker d, Ales a
where d.LikedBeers = a.name;
-- -- -- -- 答案：
select d.name from Drinker d
where d.LikedBeers in (
  select name from Ales
);

-- -- -- c.
select b1.name, b2.name from Beers b1, Beers b2
where b1.name <> b2.name and b1.manf = b2.manf 
order by b1.name, b2.name
-- -- -- -- 答案：
select b1.name, b2.name from Beers b1, Beers b2
where b1.name < b2.name and b1.manf = b2.manf
-- -- -- -- 审题错误啦




-- 2017 fall afternoon 2
-- -- 1.
-- -- -- a.
select b.name from Beers b
where b.name not in (
  select s.beer from Sells s
)
-- -- -- b.
select b.name from Beers b 
left outer join Sells s
on b.name = s.beer
where s.bar is null
-- -- -- c.
select b.name from Beers b
where b.name not exists (
  ...
)
-- -- -- -- 答案：
select b.name from Beers b
where not exists (
  select s.beer from Sells s
  where s.beer = b.name
)

-- -- 2.
-- a) insert into Sells table
-- b) delete from Beers table
-- c) update Beers table or Sells table
-- 对咯！




-- 2018 spring
-- -- 1. Find bars frequented by drinkers who live in LA.
select distinct f.bar from Frequents f
left outer join Drinkers d
on f.drinker = d.name
where d.city = 'Los Angeles'
-- -- -- 错误！不能用left outer join
-- -- -- Claude: If we used a LEFT OUTER JOIN, it would include bars that are not frequented by any drinkers living in Los Angeles because a LEFT OUTER JOIN returns all rows from the left table (in this case, the Frequents table) and matches them with rows from the right table (in this case, the Bars table) if a match exists, or returns NULL values for the columns from the right table if a match does not exist.
select distinct f.bar from Frequents f
inner join Drinkers d 
on f.drinker = d.name
where d.city = 'Los Angeles'
-- -- -- 或者 答案：
select distinct f.bar from Frequents f, Drinker d
where f.drinker = d.name
and d.city = 'Los Angeles'

-- -- 2. Find name of bars which sell at least two different beers.
select distinct s1.bar from Sells s1, Sells s2
where s1.beer <> s2.beer and s1.bar = s2.bar

-- -- 3. Find the most expensive beers sold at bars. Note that price may be null.
select beer from Sells 
where price = (
  select max(price) from Sells
)
and price is not null
-- -- -- 错误！会返回 Empty Set！ 因为
-- -- -- select max(price) from Sells 会返回NULL
-- -- -- Then, in the main query, the condition price = (subquery) would never be true for any row because no price can be equal to NULL. 
-- -- -- 所以正确写法是：
SELECT beer
FROM Sells
WHERE price = (
    SELECT MAX(price)
    FROM Sells
    WHERE price IS NOT NULL
);
-- -- -- 或者 答案：
select beer from Sells 
where price >= ALL (
  select price from Sells
  where price is not null
)
-- -- -- 无论如何 `price is not null` 都要写在subquery里面

-- -- 4. Find drinkers who like beers but do not frequent any bars. You are required to use outer join.
select distinct l.drinker from Likes l 
outer left join Frequents f
on f.drinker = l.drinker
where f.bar is null

-- -- 5. Find drinkers who frequent some bars but do not like any beers. You are required to use subqueries.
select distinct f.drinker from Frequents f
where f.drinker is not in (
  select l.drinker from Likes l
)
-- -- -- 正确。或者 答案：
SELECT drinker FROM Frequents WHERE NOT EXISTS (
SELECT *
FROM Likes
WHERE Likes.drinker = Frequents.drinker
);




