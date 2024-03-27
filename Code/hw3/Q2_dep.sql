-- Use the CINEMA database
USE CINEMA;

-- Drop existing tables if they exist
DROP TABLE IF EXISTS DirectedBy, ActIn, Directors, Actors, Movies;


-- Please create the tables as per the structure given.
-- Remember to consider appropriate data types and primary/foreign key constraints.

-- Movies(id, title, year, length, language)
CREATE TABLE Movies (
  id        INT           AUTO_INCREMENT  PRIMARY KEY,
  title     VARCHAR(255)  NOT NULL,
  year      SMALLINT,
  length    SMALLINT,
  language  VARCHAR(50)   DEFAULT 'en',
  UNIQUE(title, year)
);
-- Insert data into Movies table
INSERT INTO Movies (title, year, length, language)
VALUES
  ('Inception', 2010, 148, 'en'),
  ('The Dark Knight', 2008, 148, 'en'),
  ('Pulp Fiction', 1994, 154, 'en'),
  ('The Shawshank Redemption', 1994, 142, 'en'),
  ('Forrest Gump', 1994, 142, 'en'),
  ('Titanic', 1997, 195, 'en'),
  ('The Matrix', 1999, 136, 'en'),
  ('Fight Club', 1999, 139, 'en'),
  ('The Lord of the Rings: The Fellowship of the Ring', 2001, 178, 'en'),
  ('Gladiator', 2000, 155, 'en'),
  ('Twilight Zone', 1983, 101, 'en'),
  ('Amélie', 2001, 122, 'fr'),
  ('La La Land', 2016, 128, 'en'),
  ('The Intouchables', 2011, 112, 'fr'),
  ('The Artist', 2011, 100, 'fr'),
  ('The English Patient', 1996, 162, 'en'),
  ('Bleu', 1993, 99, 'fr');

-- Actors(id, name, gender)
CREATE TABLE Actors (
  id      INT           AUTO_INCREMENT  PRIMARY KEY,
  name    VARCHAR(100)  NOT NULL,
  gender  CHAR,
  UNIQUE(name, gender)
);
-- Insert data into Actors table
INSERT INTO Actors (name, gender)
VALUES
  ('Leonardo DiCaprio', 'M'),
  ('Tom Hanks', 'M'),
  ('Brad Pitt', 'M'),
  ('Morgan Freeman', 'M'),
  ('Keanu Reeves', 'M'),
  ('Uma Thurman', 'F'),
  ('Charlize Theron', 'F'),
  ('Kate Winslet', 'F'),
  ('Lawrence Fishburne', 'M'),
  ('Edward Norton', 'M'),
  ('Dan Aykroyd', 'M'),
  ('Albert Brooks', 'M'),
  ('Audrey Tautou', 'F'),
  ('Omar Sy', 'M'),
  ('Jean Dujardin', 'M'),
  ('Marion Cotillard', 'F'),
  ('Juliette Binoche', 'F');

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
  id          INT           AUTO_INCREMENT  PRIMARY KEY,
  name        VARCHAR(100)  NOT NULL,
  nationality VARCHAR(100),
  UNIQUE(name, nationality)
);
-- Insert data into Directors table
INSERT INTO Directors (name, nationality)
VALUES
    ('Christopher Nolan', 'British'),
    ('Quentin Tarantino', 'American'),
    ('Frank Darabont', 'American'),
    ('James Cameron', 'Canadian'),
    ('Lana Wachowski', 'American'),
    ('David Fincher', 'American'),
    ('Peter Jackson', 'New Zealander'),
    ('Ridley Scott', 'British'),
    ('Steven Spielberg', 'American'),
    ('Martin Scorsese', 'American'),
    ('Krzysztof Kieślowski', 'Polish');

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

-- Please insert sample data into the tables created above.
-- Note: Testing will be conducted on a blind test set, so ensure your table creation and data insertion scripts are accurate and comprehensive.
