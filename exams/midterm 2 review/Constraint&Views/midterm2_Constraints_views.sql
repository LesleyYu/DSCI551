
-- review Constraints
-- -- 1. primary key :
create table Sells (
    bar VARCHAR(100) references Bars(name),
    beer VARCHAR(100) references Beers(name),
    price real,
    primary key(bar, beer)
);

-- -- 2. foreign key:
create table Beers (
  name CHAR(20) PRIMARY KEY,
  manf CHAR(20)
);

create table Sells (
  bar CHAR(20),
  beer CHAR(20) references Beers(name),
  price REAL
);

-- -- -- or:
create table Sells (
  bar CHAR(20),
  beer CHAR(20),
  price REAL,
  foreign key(beer) references Beers(name)
)
-- -- -- 注意要写括号 (beer)

-- -- foreign key with unique attribs:
create table R (a int primary key); -- or `int unique`
Insert into R values (1),
select * from R;

create table S (b int, foreign key (b) references R(a));
Insert into S values (1);
Insert into S values (null); -- this works even though 'a' is primary key in R
select * from S;

-- if there is a foreign-key constraint from attributes of relation S to the primary key of relation R, two violations are possible:
-- 1. an insertion ot update to S introduces values not found in R.
-- 2. a deletion or update to R causes some tuples of S to 'dangle'

-- actions taken to enforce foreign-key constraints
create table Sells (
  bar CHAR(20),
  beer CHAR(20),
  price real,
  foreign key(beer) references Beers(name) 
    on delete set null,
    on update cascade
);

-- -- 3. value-based constraints
create table Sells (
  bar CHAR(20),
  beer CHAR(20) check (beer IN (
    select name from Beers
  )),
  price real check ( price <= 5.0 )
)

-- -- 4. tuple-based constraints
create table Sells (
  bar CHAR(20),
  beer CHAR(20),
  price REAL,
  check (bar = 'Joe' or price <= 5.00)
);

insert into sells values('Joe', 'bud', 8); -- okay
update sells set bar = 'joe1';    -- error


-- -- 5. assertions
create assertion FewBar check (
  (select count(*) from Bars) <= 
  (select count(*) from Drinkers)
);

-- review Views
-- -- example (ETL: extract, transform, load)
insert into W(time, tweet, stock);
select T.time, tweet_content, stock * 200
from ds1.T join ds2.S on T.time = S.timestamp

create materialized view W(time, tweet, stock) 
As 
select T.time, tweet_content, stock * 200
  from ds1 T join ds2 S on T.time = S.timestamp
  <refreshing policy>

-- -- view definition
create view CanDrink as 
select distinct drinker, beer
from Frequents, Sells
where Frequents.bar = Sells.bar;
-- -- what happens when a view is used?
-- -- -- relational algebra. 
-- -- -- view expansion!!
-- -- -- view expansion: 1. push selections(where clause) down the tree
-- -- -- view expansion: 2. Eliminate unnecessary projections (select clause)




-- 2019 spring

-- -- 1. 
create table W (
  Name VARCHAR(20) primary key,
  Weight int(5),    -- default null
  foreign key (Name) references D(name)
  on update cascade
  on delete cascade
);

create table H (
  Name VARCHAR(20) primary key,
  Height int(5),    -- default null
  foreign key (name) references D(name)
  on update cascade
  on delete cascade
);

-- -- 2. 
-- -- -- Try understand 'SET NULL' in DBMS

-- -- 3.
create view WHD as
select D.name, W.weight, H.Height from W, H, D
where D.Name = W.Name and D.Name = H.Name and 
D.age >= 25 and D.gender = 'M';

-- -- 4.
select WHD.Name, WHD.Weight from WHD 
left outer join D
on WHD.Name = D.Name 
where D.Age <= 30;
-- -- -- 不太对。Claude分析： https://claude.ai/chat/153deec2-28e5-47c2-a77b-1951e8747bdb
SELECT WHD.Name, WHD.Weight
FROM WHD
INNER JOIN D ON WHD.Name = D.Name AND D.Age BETWEEN 25 AND 30;
-- -- -- 或者
SELECT Name, Weight
FROM WHD
WHERE EXISTS (
    SELECT 1
    FROM D
    WHERE D.Name = WHD.Name AND D.Age BETWEEN 25 AND 30
);



-- 2019 fall

-- -- 1. 
BuyerName references Person(Name),
SellerName references Person(Name), 
StoreID references Store(ID), 
SerialNo references Product(SerialNo)

-- -- 2.
-- insert: no
-- delete: yes   Purchase should be checked
-- update: yes   Purchase should be checked
-- no. it's part of pk in Purchase. cannot be null

-- -- 3.
create view BrandModelView as(
  select p.Brand, p.Model, count(*) as total
  from Purchase pcs
  inner join Product p
  on pcs.SerialNo = p.SerialNo
  group by p.Brand, p.Model
);

-- -- 4.
select sum(total)
from BrandModelView
group by Brand;



-- 2018 spring afternoon
-- -- 1.
create table Likes (
  drinker VARCHAR(100),
  beer VARCHAR(100),
  primary key (drinker, beer),
  foreign key (drinker) references Drinker(name) on delete cascade on update cascade,
  foreign key (beer) references Beers(name) on delete cascade on update cascade
);

-- -- 2.
-- -- 3.
create view SellsView as(
  select b.city, max(s.price) 
  from Sells s
  inner join Bars b on b.name = s.bar
  group by b.city;
);

-- -- 5. 
db.Sells.find(
  {
    beer: "Bud",
    price: { $gt: 3 }
  },
  {
    _id: 0, bar: 1
  }
);

-- 2018 fall
-- -- 1.
select distinct R.A, R.B, S.C from R
left outer join S
on R.A = S.A
union
select distinct R.A, R.B, S.C from R
right outer join S
on R.A = S.A;




-- 2017 spring
-- -- 1. [2 points] Write a SQL query to “find brands such that at least five laptops for each brand have been sold.”
select p.Brand from Product p
inner join Purchase pu
on p.SerialNo = pu.SerialNo
group by p.Brand
having count(distinct p.SerialNo) >= 5;

-- -- 4. 
create view BrandStoreView as (
  select count(*) as total from Purchase pu
  inner join Product p
  on pu.SerialNo = p.SerialNo
  inner join Store s
  on s.ID = pu.StoreID
  group by p.Brand, s.City
);
-- -- -- correct

-- -- 5.
select Brand, sum(total) from BrandStoreView
group by Brand;