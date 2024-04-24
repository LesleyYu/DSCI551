from pyspark.sql import SparkSession
import pyspark.sql.functions as fc

# Initialize SparkSession and load the datasets
spark = SparkSession.builder.appName("Film Dataset Analysis").getOrCreate()
film = spark.read.csv('film.csv', header=True, inferSchema=True)
actor = spark.read.csv('actor.csv', header=True, inferSchema=True)
film_actor = spark.read.csv('film_actor.csv', header=True, inferSchema=True)

def query_a(film_df):
    """
    Question: Select title and description from the film dataset where the rating is 'PG'.
    """
    # Filter the RDD to get films with rating 'PG'
    pg_films = film.where(fc.col('rating') >= 'PG')

    # Select the title and description columns
    result = pg_films.select('title', 'description').limit(5)
    
    # Limit the output to 5 rows
    return result

#  query_a Output:
# +----------------+--------------------+
# |           title|         description|
# +----------------+--------------------+
# |ACADEMY DINOSAUR|A Epic Drama of a...|
# |    AGENT TRUMAN|A Intrepid Panora...|
# | AIRPLANE SIERRA|A Touching Saga o...|
# | AIRPORT POLLOCK|A Epic Tale of a ...|
# |   ALABAMA DEVIL|A Thoughtful Pano...|
# +----------------+--------------------+





def query_b(film_df):
    """
    Question: Select the average replacement cost grouped by rating for films longer than 60 minutes,
              having at least 160 films per rating.
    """
    result = film\
            .where(fc.col('length') >= 60)\
            .groupBy('rating')\
            .agg(fc.avg('replacement_cost').alias('avg_replacement_cost'), fc.count('*').alias('count'))\
            .where(fc.col('count') >= 160)\
            .select('rating', 'avg_replacement_cost')
    return result

# query_b Output:
# +------+--------------------+
# |rating|avg_replacement_cost|
# +------+--------------------+
# |    PG|   18.84465116279062|
# | NC-17|  20.265132275132174|
# |     R|  20.294347826086863|
# | PG-13|  20.579108910890984|
# +------+--------------------+



def query_c(film_actor_df):
    """
    Question: Select actor IDs that appear in both film ID 1 and film ID 23.
    """
    # Get the actor_ids that appear in both film 1 and film 23
    mutual_actors = (film_actor.where(fc.col('film_id') == 1)
                        .select('actor_id')
                        .intersect(film_actor.where(fc.col('film_id') == 23)
                                .select('actor_id')))
    return mutual_actors

# query_c Output:
# +--------+
# |actor_id|
# +--------+
# |       1|
# +--------+




def query_d(actor_df, film_actor_df):
    """
    Question: Select distinct first name and last name of actors who acted in films 1, 2, or 3.
              Order the result by first name.
    """
    actor_film = actor.join(film_actor, actor.actor_id == film_actor.actor_id, 'inner')
    result = (actor_film\
              .where(fc.col('film_id').isin([1, 2, 3]))\
              .select('first_name', 'last_name')\
              .distinct()\
              .orderBy(fc.asc('first_name'))\
              .limit(5)
              )
    return result
    
# query_d Output:
# +----------+---------+
# |first_name|last_name|
# +----------+---------+
# |       BOB|  FAWCETT|
# |   CAMERON|   STREEP|
# |     CHRIS|     DEPP|
# | CHRISTIAN|    GABLE|
# |    JOHNNY|     CAGE|
# +----------+---------+



def query_e(film_df):
    """
    Question: Select rental duration, rating, minimum, maximum, and average length, and count of films,
                grouped by rental duration and rating, ordered by rental duration descending.
    """
    result = (film
          .groupBy('rental_duration', 'rating')
          .agg(fc.min('length'),
               fc.max('length'),
               fc.avg('length'),
               fc.count('length'))
          .orderBy(fc.col('rental_duration').desc())
          .limit(10))
    return result

# query_e Output:
# +---------------+------+-----------+-----------+------------------+-------------+
# |rental_duration|rating|min(length)|max(length)|       avg(length)|count(length)|
# +---------------+------+-----------+-----------+------------------+-------------+
# |              7|     R|         59|        185|131.27272727272728|           33|
# |              7| NC-17|         48|        179|             118.7|           40|
# |              7|    PG|         46|        182|111.95555555555555|           45|
# |              7|     G|         49|        185|116.34482758620689|           29|
# |              7| PG-13|         48|        185|118.27272727272727|           44|
# |              6| NC-17|         48|        184|111.78947368421052|           57|
# |              6| PG-13|         46|        185|            118.52|           50|
# |              6|     G|         57|        183|             128.0|           39|
# |              6|     R|         54|        181|127.18518518518519|           27|
# |              6|    PG|         49|        182|104.82051282051282|           39|
# +---------------+------+-----------+-----------+------------------+-------------+

def main():
    print("Query A:")
    query_a(film).show()

    print("Query B:")
    query_b(film).show()

    print("Query C:")
    query_c(film_actor).show()

    print("Query D:")
    query_d(actor, film_actor).show()

    print("Query E:")
    query_e(film).show()

if __name__ == "__main__":
    main()