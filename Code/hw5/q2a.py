from pyspark.sql import SparkSession
import pyspark.sql.functions as fc

# Initialize SparkSession and load the datasets
spark = SparkSession.builder.appName("Film Dataset Analysis").getOrCreate()
film = spark.read.csv('film.csv', header=True, inferSchema=True)


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


def main():
    print("Query A:")
    query_a(film).show()

if __name__ == "__main__":
    main()