USE CINEMA;

-- 1) Find titles of the longest movies. Note that there might be more than such movie.
select title from Movies where length = (select max(length) from Movies);

-- 2) Find out titles of movies that contain "Twilight" and are directed by "Steven Spielberg".
select title from Movies 
  where 
  title like '%Twilight%' and
  id in (
      select movie_id from DirectedBy left outer join Directors d
        on director_id=d.id
          where d.name = "Steven Spielberg"
  );


-- 3) Find out how many movies "Tom Hanks" has acted in.
select name, count(*)
  from ActIn ai join Actors a
  on a.id = ai.actor_id
  where name = 'Tom Hanks';

-- 4) Find out which director directed only a single movie.
select name from Directors where id in (
  select director_id from DirectedBy group by director_id having count(*) = 1
);

-- 5) Find titles of movies which have the largest number of actors. Note that there may be multiple such movies.
select title from Movies m join ActIn on movie_id = id group by m.id having count(*) = (
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

-- 7) Find names of directors who only directed English movies.
select d.name from Directors d
join DirectedBy db on d.id = db.director_id
join Movies m on db.movie_id = m.id
group by d.id
having count(distinct m.language) = 1;