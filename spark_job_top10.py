from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, row_number
from pyspark.sql.window import Window

# Création de la session Spark
spark = SparkSession.builder \
    .appName("Top10ProductsByRegion") \
    .config("spark.mongodb.read.connection.uri", "mongodb://127.0.0.1/ecommerce.events") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.3.0") \
    .getOrCreate()

# Chargement des données
df = spark.read.format("mongodb").load()

# Filtrer les événements de type 'click' avec des régions et des produits définis
clicks = df.filter(
    (col("event_type") == "click") &
    (col("region").isNotNull()) &
    (col("product_id").isNotNull())
)

# Compter les clics par région et produit
click_counts = clicks.groupBy("region", "product_id") \
    .agg(count("*").alias("nb_clicks"))

# Définir une fenêtre partitionnée par région, triée par nombre de clics décroissant
windowSpec = Window.partitionBy("region").orderBy(col("nb_clicks").desc())

# Attribuer un rang à chaque produit dans sa région
ranked = click_counts.withColumn("rank", row_number().over(windowSpec))

# Garder uniquement les top 10 par région
top_10_per_region = ranked.filter(col("rank") <= 10)

# Afficher le résultat
top_10_per_region.orderBy("region", "rank").show(100, truncate=False)

spark.stop()
