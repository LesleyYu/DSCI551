from pyspark.sql import SparkSession
import pyspark.sql.functions as fc

# Initialize SparkSession and load the datasets
spark = SparkSession.builder.appName("Film Dataset Analysis").getOrCreate()
film = spark.read.csv('film.csv', header=True, inferSchema=True)


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



def main():
    print("Query E:")
    query_e(film).show()

if __name__ == "__main__":
    main()