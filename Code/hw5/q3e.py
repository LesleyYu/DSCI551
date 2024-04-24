from pyspark.sql import SparkSession

# Initialize SparkSession
spark = SparkSession.builder.appName("Film Dataset Analysis").getOrCreate()

# Load the datasets as DataFrames
film_df = spark.read.csv('film.csv', header=True, inferSchema=True)

# Convert DataFrames to RDDs
film_rdd = film_df.rdd


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


    # a = film_rdd.map(lambda row: (row["rental_duration"], row["rating"], row["length"]))
    # print('\n\n\n\na', a.take(5))   # [(6, 'PG', 86), (3, 'G', 48), (7, 'NC-17', 50), (5, 'G', 117), (6, 'G', 130)]
    # key_value_pairs = a.map(lambda x: ((x[0], x[1]), x[2]))
    
    # # b = a.groupBy(lambda x: (x[0], x[1]))
    # b = key_value_pairs.groupByKey()
    # print('\n\n\n\nb', b.count(), '\n\n', b.take(3))    # 25
    #     # [((6, 'PG'), <pyspark.resultiterable.ResultIterable object at 0x7f5a8fc094c0>), 
    #     # ((3, 'G'), <pyspark.resultiterable.ResultIterable object at 0x7f5a8fc092b0>), 
    #     # ((7, 'NC-17'), <pyspark.resultiterable.ResultIterable object at 0x7f5a8fc09760>)]
    # list(b.collect()[1][1])
    #     # [(3, 'G', 48), (3, 'G', 74), (3, 'G', 86), (3, 'G', 108), (3, 'G', 182), (3, 'G', 71), (3, 'G', 89), (3, 'G', 179), (3, 'G', 164), (3, 'G', 113)...]
    
    # sum_count_b = b.mapValues(lambda values: (sum(values), len(values)))

    # avg = b.mapValues(lambda values: (min(values), max(values), sum(values) / len(values), len(values)))

    # return b

# %query_e output:
# [(7, 'NC-17', 48, 179, 118.7, 40), (7, 'PG-13', 48, 185, 118.27272727272727, 44), (7, 'PG', 46, 182, 111.95555555555555, 45), (7, 'G', 49, 185, 116.34482758620689, 29), (7, 'R', 59, 185, 131.27272727272728, 33), (6, 'PG', 49, 182, 104.82051282051282, 39), (6, 'G', 57, 183, 128.0, 39), (6, 'PG-13', 46, 185, 118.52, 50), (6, 'R', 54, 181, 127.18518518518519, 27), (6, 'NC-17', 48, 184, 111.78947368421052, 57)]


def main():
    print("Query E:")
    print(query_e(film_rdd).take(10))

if __name__ == "__main__":
    main()
