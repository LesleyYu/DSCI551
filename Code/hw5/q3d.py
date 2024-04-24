from pyspark.sql import SparkSession

# Initialize SparkSession
spark = SparkSession.builder.appName("Film Dataset Analysis").getOrCreate()

# Load the datasets as DataFrames
actor_df = spark.read.csv('actor.csv', header=True, inferSchema=True)
film_actor_df = spark.read.csv('film_actor.csv', header=True, inferSchema=True)

# Convert DataFrames to RDDs
actor_rdd = actor_df.rdd
film_actor_rdd = film_actor_df.rdd


def query_d(actor_rdd, film_actor_rdd):
    """
    Select distinct first name and last name of actors who acted in films 1, 2, or 3.
    """
    # joined = actor_rdd.join(film_actor_rdd)
    # # print(joined.count())         # 5462 same as film_actor_rdd.count()
    # # print(joined.take(10))        # [(2, ('NICK', 3)), (2, ('NICK', 31))]

    # # actors_in_123 = joined.filter(lambda x: x[1][1] in [1, 2, 3])
    # # print(actors_in_123.count())  # 19
    # actors_id_in_123 = joined.filter(lambda x: x[1][1] in [1, 2, 3]).map(lambda x: x[0])
    # # print(actors_id_in_123.collect())   #[2, 10, 20, 24, 30, 40, 64, 90, 108, 160, 162, 188, 198, 1, 19, 19, 53, 85, 123]

    # actor_names = actor_rdd.filter(lambda x: x[1] in actors_id_in_123)
    # print(actor_names.take(2))
    # result = (actor_names
    #           .map(lambda row: (row.first_name, row.last_name))
    #           .distinct()
    #           .sortBy(lambda x: x[0])
    #           )

    # Join the actor and film_actor RDDs on actor_id
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



def main():
    print("Query D:")
    print(query_d(actor_rdd, film_actor_rdd).take(5))

if __name__ == "__main__":
    main()
