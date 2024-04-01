-- Use the CINEMA database
USE CINEMA;

-- Drop existing tables if they exist
DROP TABLE IF EXISTS DirectedBy, ActIn, Directors, Actors, Movies;

-- Please create the tables as per the structure given.
-- Remember to consider appropriate data types and primary/foreign key constraints.

-- Movies(id, title, year, length, language)
CREATE TABLE Movies (
  id        INT           PRIMARY KEY,
  title     VARCHAR(255)  NOT NULL,
  year      SMALLINT,
  length    SMALLINT,
  language  VARCHAR(50)   DEFAULT 'en',
  UNIQUE(title, year)
);

-- Insert data into Movies table
INSERT INTO Movies (id, title, year, length, language)
VALUES
  (1, 'Inception', 2010, 148, 'en'),
  (2, 'The Dark Knight', 2008, 148, 'en'),
  (3, 'Pulp Fiction', 1994, 154, 'en'),
  (4, 'The Shawshank Redemption', 1994, 142, 'en'),
  (5, 'Forrest Gump', 1994, 142, 'en'),
  (6, 'Titanic', 1997, 195, 'en'),
  (7, 'The Matrix', 1999, 136, 'en'),
  (8, 'Fight Club', 1999, 139, 'en'),
  (9, 'The Lord of the Rings: The Fellowship of the Ring', 2001, 178, 'en'),
  (10, 'Gladiator', 2000, 155, 'en'),
  (11, 'Twilight Zone', 1983, 101, 'en'),
  (12, 'Amélie', 2001, 122, 'fr'),
  (13, 'La La Land', 2016, 128, 'en'),
  (14, 'The Intouchables', 2011, 112, 'fr'),
  (15, 'The Artist', 2011, 100, 'fr'),
  (16, 'The English Patient', 1996, 162, 'en'),
  (17, 'Bleu', 1993, 99, 'fr');

-- Actors(id, name, gender)
CREATE TABLE Actors (
  id      INT           PRIMARY KEY,
  name    VARCHAR(100)  NOT NULL,
  gender  CHAR,
  UNIQUE(name, gender)
);

-- Insert data into Actors table
INSERT INTO Actors (id, name, gender)
VALUES
  (1, 'Leonardo DiCaprio', 'M'),
  (2, 'Tom Hanks', 'M'),
  (3, 'Brad Pitt', 'M'),
  (4, 'Morgan Freeman', 'M'),
  (5, 'Keanu Reeves', 'M'),
  (6, 'Uma Thurman', 'F'),
  (7, 'Charlize Theron', 'F'),
  (8, 'Kate Winslet', 'F'),
  (9, 'Lawrence Fishburne', 'M'),
  (10, 'Edward Norton', 'M'),
  (11, 'Dan Aykroyd', 'M'),
  (12, 'Albert Brooks', 'M'),
  (13, 'Audrey Tautou', 'F'),
  (14, 'Omar Sy', 'M'),
  (15, 'Jean Dujardin', 'M'),
  (16, 'Marion Cotillard', 'F'),
  (17, 'Juliette Binoche', 'F');

-- ActIn(actor_id, movie_id)
CREATE TABLE ActIn (
  actor_id INT,
  movie_id INT,
  PRIMARY KEY (actor_id, movie_id),
  FOREIGN KEY (actor_id) REFERENCES Actors(id),
  FOREIGN KEY (movie_id) REFERENCES Movies(id)
);

-- Insert data into ActIn table
INSERT INTO ActIn (actor_id, movie_id)
VALUES
    (1, 1),
    (1, 2),
    (1, 5),
    (2, 4),
    (2, 5),
    (2, 10),
    (3, 3),
    (3, 7),
    (3, 8),
    (3, 10),
    (4, 4),
    (4, 6),
    (5, 7),
    (5, 8),
    (6, 3),
    (7, 3),
    (8, 6),
    (9, 7),
    (9, 9),
    (10, 8),
    (10, 9),
    (11, 11),
    (12, 11),
    (13, 12),
    (14, 14),
    (15, 15),
    (16, 13),
    (17, 16),
    (17, 17);

-- Directors(id, name, nationality)
CREATE TABLE Directors (
  id          INT           PRIMARY KEY,
  name        VARCHAR(100)  NOT NULL,
  nationality VARCHAR(100),
  UNIQUE(name, nationality)
);

-- Insert data into Directors table
INSERT INTO Directors (id, name, nationality)
VALUES
    (1, 'Christopher Nolan', 'British'),
    (2, 'Quentin Tarantino', 'American'),
    (3, 'Frank Darabont', 'American'),
    (4, 'James Cameron', 'Canadian'),
    (5, 'Lana Wachowski', 'American'),
    (6, 'David Fincher', 'American'),
    (7, 'Peter Jackson', 'New Zealander'),
    (8, 'Ridley Scott', 'British'),
    (9, 'Steven Spielberg', 'American'),
    (10, 'Martin Scorsese', 'American'),
    (11, 'Krzysztof Kieślowski', 'Polish');

-- DirectedBy(movie_id, director_id)
CREATE TABLE DirectedBy (
  movie_id INT,
  director_id INT,
  PRIMARY KEY (movie_id, director_id),
  FOREIGN KEY (movie_id) REFERENCES Movies(id),
  FOREIGN KEY (director_id) REFERENCES Directors(id)
);

-- Insert data into DirectedBy table
INSERT INTO DirectedBy (movie_id, director_id)
VALUES
    (1, 1),
    (2, 1),
    (3, 2),
    (4, 3),
    (5, 3),
    (6, 4),
    (7, 5),
    (8, 6),
    (9, 7),
    (10, 8),
    (11, 9),
    (17, 11);
