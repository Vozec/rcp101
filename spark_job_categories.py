from pyspark.sql import SparkSession
from pyspark.sql.functions import col, hour, count, row_number
from pyspark.sql.window import Window

spark = SparkSession.builder \
    .appName("TopCategoryPerHour") \
    .config("spark.mongodb.read.connection.uri", "mongodb://127.0.0.1/ecommerce.events") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.3.0") \
    .getOrCreate()

df = spark.read.format("mongodb").load()

# On part des clics avec des catégories valides
clicks = df.filter((col("event_type") == "click") & (col("category").isNotNull()))

# Extraire l'heure
clicks = clicks.withColumn("hour", hour(col("timestamp")))

# Compter le nombre de clics par heure et catégorie
click_counts = clicks.groupBy("hour", "category").agg(count("*").alias("nb_clicks"))

# Définir une fenêtre pour extraire le top 1 par heure
windowSpec = Window.partitionBy("hour").orderBy(col("nb_clicks").desc())

# Appliquer le classement et filtrer le premier par heure
top_category_per_hour = click_counts.withColumn("rank", row_number().over(windowSpec)) \
    .filter(col("rank") == 1) \
    .select("hour", "category", "nb_clicks")

# Afficher le résultat final
top_category_per_hour.orderBy("hour").show(24, truncate=False)

spark.stop()
