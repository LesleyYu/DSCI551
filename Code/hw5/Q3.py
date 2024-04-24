from pyspark.sql import SparkSession

# Initialize SparkSession
spark = SparkSession.builder.appName("Film Dataset Analysis").getOrCreate()

# Load the datasets as DataFrames
film_df = spark.read.csv('film.csv', header=True, inferSchema=True)
actor_df = spark.read.csv('actor.csv', header=True, inferSchema=True)
film_actor_df = spark.read.csv('film_actor.csv', header=True, inferSchema=True)

# Convert DataFrames to RDDs
film_rdd = film_df.rdd
actor_rdd = actor_df.rdd
film_actor_rdd = film_actor_df.rdd

"""
Select title and description from the film dataset where the rating is 'PG'.
"""
def query_a(film_rdd):
    # Filter the RDD to get films with rating 'PG'
    pg_films = film_rdd.filter(lambda row: row.rating == "PG")
    # Select the title and description columns
    result = pg_films.map(lambda row: (row.title, row.description))
    return result

# %query_a output:
# [('ACADEMY DINOSAUR', 'A Epic Drama of a Feminist And a Mad Scientist who must Battle a Teacher in The Canadian Rockies'), ('AGENT TRUMAN', 'A Intrepid Panorama of a Robot And a Boy who must Escape a Sumo Wrestler in Ancient China'), ('ALASKA PHANTOM', 'A Fanciful Saga of a Hunter And a Pastry Chef who must Vanquish a Boy in Australia'), ('ALI FOREVER', 'A Action-Packed Drama of a Dentist And a Crocodile who must Battle a Feminist in The Canadian Rockies'), ('AMADEUS HOLY', 'A Emotional Display of a Pioneer And a Technical Writer who must Battle a Man in A Baloon')]


def query_b(film_rdd):
    """
    Select the average replacement cost grouped by rating for films longer than 60 minutes,
    having at least 160 films per rating.
    """
    # Filter the RDD to get films with length >= 60
    long_films = film_rdd.filter(lambda row: row.length >= 60) 
    # print(long_films.count())   # 904

    # Group the RDD by rating and calculating the average replacement_cost, then filter for count >= 160
    result = (long_films
              .map(lambda row: (row.rating, row.replacement_cost))
              .groupByKey()
              .filter(lambda x: len(list(x[1])) >= 160)
              .mapValues(lambda values: sum(values) / len(values))
              )
    
    return result

# %query_b output:
# [('PG', 18.84465116279062), ('PG-13', 20.579108910890984), ('NC-17', 20.265132275132174), ('R', 20.294347826086863)]


def query_c(film_actor_rdd):
    """
    Select actor IDs that appear in both film ID 1 and film ID 23.
    """
    actors_1 = film_actor_rdd.filter(lambda row: row.film_id == 1).map(lambda row: row.actor_id)
    actors_23 = film_actor_rdd.filter(lambda row: row.film_id == 23).map(lambda row: row.actor_id)
    result = actors_1.intersection(actors_23)
    return result

# %query_c output:
# [1]


def query_d(actor_rdd, film_actor_rdd):
    """
    Select distinct first name and last name of actors who acted in films 1, 2, or 3.
    """
    actor_ids = film_actor_rdd.filter(lambda x: x[1] in [1, 2, 3]).map(lambda x: x[0]).distinct().collect()

    # Filter the actor_rdd to get the actors who appeared in films 1, 2, or 3
    actors_in_films = actor_rdd.filter(lambda x: x[0] in actor_ids)

    # Select the distinct first_name and last_name, order by first_name, and limit to 5 rows
    result = (
        actors_in_films
        .map(lambda x: (x[1], x[2]))
        .distinct()
        .sortBy(lambda x: x[0])
    )

    return result

# %query_d output:
# [('BOB', 'FAWCETT'), ('CAMERON', 'STREEP'), ('CHRIS', 'DEPP'), ('CHRISTIAN', 'GABLE'), ('JOHNNY', 'CAGE')]


def query_e(film_rdd):
    """
    Select rental duration, rating, minimum, maximum, and average length, and count of films,
    grouped by rental duration and rating, ordered by rental duration descending.
    """
    result = (film_rdd
                .map(lambda row: ((row["rental_duration"], row["rating"]), row["length"]))
                .groupByKey()
                .mapValues(lambda values: (min(values), max(values), sum(values) / len(values), len(values)))
                .sortBy(lambda x: x[0][0], ascending=False)
                .map(lambda x: (x[0][0], x[0][1], x[1][0], x[1][1], x[1][2], x[1][3]))
    )
    return result

# %query_e output:
# [(7, 'NC-17', 48, 179, 118.7, 40), (7, 'PG-13', 48, 185, 118.27272727272727, 44), (7, 'PG', 46, 182, 111.95555555555555, 45), (7, 'G', 49, 185, 116.34482758620689, 29), (7, 'R', 59, 185, 131.27272727272728, 33), (6, 'PG', 49, 182, 104.82051282051282, 39), (6, 'G', 57, 183, 128.0, 39), (6, 'PG-13', 46, 185, 118.52, 50), (6, 'R', 54, 181, 127.18518518518519, 27), (6, 'NC-17', 48, 184, 111.78947368421052, 57)]

def main():
    print("Query A:")
    print(query_a(film_rdd).take(5))

    print("Query B:")
    print(query_b(film_rdd).collect())

    print("Query C:")
    print(query_c(film_actor_rdd).collect())

    print("Query D:")
    print(query_d(actor_rdd, film_actor_rdd).take(5))

    print("Query E:")
    print(query_e(film_rdd).take(10))

if __name__ == "__main__":
    main()
