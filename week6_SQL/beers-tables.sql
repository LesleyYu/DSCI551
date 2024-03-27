
-- foreign key must be defined as an element to be enforced in MySQL


drop table if exists Sells;
drop table if exists Likes;
drop table if exists Frequents;

drop table if exists Beers;
create table Beers(name varchar(100) primary key, manf varchar(100));

insert into Beers values('Bud', 'Anheuser-Busch');
insert into Beers values('Bud Lite', 'Anheuser-Busch');
insert into Beers values('Michelob', 'Anheuser-Busch');
insert into Beers values('Summerbrew', 'Pete''s');
insert into Beers values('Budweiser', 'Heineken');

drop table if exists Bars;
create table Bars(name varchar(100) primary key, addr varchar(100));

insert into Bars values('Joe''s bar', 'Maple St.');
insert into Bars values('Bob''s bar', 'Maple St.');
insert into Bars values('Mary''s bar', 'Sunny Dr.');


drop table if exists Drinkers;
create table Drinkers(name varchar(100) primary key, addr varchar(100),
	phone varchar(20));

insert into Drinkers values('Steve', 'Vermont St.', '213-555-1234');
insert into Drinkers values('Bill', 'Jefferson St.', '213-555-0101');
insert into Drinkers values('Jennifer', 'Maple St.', '626-552-1234');
insert into Drinkers values('David', 'Vermont Ave.', '310-384-3829');

drop table if exists Sells;
create table Sells(bar varchar(100), 
	beer varchar(100), 
	price real, 
	primary key(bar, beer), 
	foreign key (bar) references Bars(name),
	foreign key (beer) references Beers(name));

insert into Sells values('Joe''s bar', 'Bud', 3);
insert into Sells values('Joe''s bar', 'Bud Lite', 3);
insert into Sells values('Joe''s bar', 'Summerbrew', 4);
insert into Sells values('Joe''s bar', 'Michelob', 3);
insert into Sells values('Bob''s bar', 'Bud', 3);
insert into Sells values('Bob''s bar', 'Summerbrew', 3);
insert into Sells values('Mary''s bar', 'Bud', null);
insert into Sells values('Mary''s bar', 'Bud Lite', 3);
insert into Sells values('Mary''s bar', 'Budweiser', 2);


drop table if exists Likes;
create table Likes(drinker varchar(100),
	beer varchar(100),
	primary key (drinker, beer),
	foreign key (drinker) references Drinkers(name),
	foreign key (beer) references Beers(name));


insert into Likes values('Steve', 'Bud');
insert into Likes values('Steve', 'Bud Lite');
insert into Likes values('Steve', 'Michelob');
insert into Likes values('Steve', 'Summerbrew');
insert into Likes values('Bill', 'Bud');
insert into Likes values('Jennifer', 'Bud');


drop table if exists Frequents;
create table Frequents(drinker varchar(100),
	bar varchar(100),
	primary key (drinker, bar),
	foreign key (drinker) references Drinkers(name), 
	foreign key (bar) references Bars(name));

insert into Frequents values('Steve', 'Joe''s bar');
insert into Frequents values('Steve', 'Bob''s bar');
insert into Frequents values('Bill', 'Mary''s bar');
insert into Frequents values('Jennifer', 'Joe''s bar');
insert into Frequents values('David', 'Joe''s bar');


