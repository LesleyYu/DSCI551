# IMPORT LIBRARIES
import sys
from sqlalchemy import create_engine
import pymysql
import pandas as pd

# NOTE: DO NOT modify any variable or function names given in the template!

# Choose EITHER SQLAlchemy OR PyMySQL:

# OPTION 1: SQLAlchemy
pymysql.install_as_MySQLdb()
DATABASE_URI = 'mysql+mysqldb://dsci551:Dsci-551@localhost/CINEMA'

# OPTION 2: PyMySQL
# Replace the placeholders with the actual database connection details
# DATABASE_CONNECTION_PARAMS = {

# }


def get_movies_by_actor(actor_name):
    """
    Fetches titles of movies that the specified actor has acted in.
    INPUT: actor_name (str) - The name of the actor
    RETURN: A list of movie titles (list)
    
    Sample Terminal Command:python3 search.py "John Doe"
    Expected Sample Output: Movies featuring John Doe: ['The Great Adventure', 'Dreams of Space']
    """

    # Placeholder for the result list:
    movies = []

    ## Your code goes here
    my_conn = create_engine(DATABASE_URI)

    with my_conn.connect() as conn:
        # Get the actor_id by querying the Actors table
        actor_id_query = f"SELECT id FROM Actors WHERE name = '{actor_name}'"
        actor_id = conn.execute(actor_id_query).scalar()

        if actor_id is None:
            return []

        # Get the list of movie_ids that the actor has acted in
        movie_ids_query = f"SELECT movie_id FROM ActIn WHERE actor_id = {actor_id}"
        movie_ids = [row[0] for row in conn.execute(movie_ids_query)]

        # Get the movie titles from the Movies table
        movie_titles_query = f"SELECT title FROM Movies WHERE id IN ({','.join(str(mid) for mid in movie_ids)})"
        movies = [row[0] for row in conn.execute(movie_titles_query)]

    return movies


# Use the below main method to test your code
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python search.py '<actor_name>'")
        sys.exit(1)
    actor_name = sys.argv[1]
    movies = get_movies_by_actor(actor_name)
    if movies:
        print(f"Movies featuring {actor_name}: {movies}")
    else:
        print(f"No movies found for actor {actor_name}.")
