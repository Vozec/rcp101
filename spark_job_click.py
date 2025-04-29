from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum as sum_, when
from pyspark.sql import Window

# Création de la session Spark
spark = SparkSession.builder \
    .appName("MeanClicksBeforePurchase") \
    .config("spark.mongodb.read.connection.uri", "mongodb://127.0.0.1/ecommerce.events") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.1.1") \
    .getOrCreate()

# Charger les événements
df = spark.read.format("mongodb").load()

# Filtrer les événements intéressants (click et purchase uniquement)
events = df.filter(col("event_type").isin(["click", "purchase"]))

# Créer une fenêtre d'analyse ordonnée par timestamp pour chaque utilisateur
windowSpec = Window.partitionBy("user_id").orderBy("timestamp")

# Ajouter une colonne pour compter les événements par utilisateur
events = events.withColumn("click_before_purchase", 
    when(col("event_type") == "click", 1)
    .when(col("event_type") == "purchase", 0)
    .otherwise(None)
)

# Cumul du nombre de clics avant chaque achat
# On va cumuler le nombre de clics jusqu'au moment où un achat est réalisé
from pyspark.sql.functions import sum as _sum

# Calcul des clics cumulés par utilisateur
events_with_cumsum = events.withColumn(
    "cumulative_clicks", 
    _sum("click_before_purchase").over(windowSpec)
)

# Garder seulement les lignes de type 'purchase'
purchases = events_with_cumsum.filter(col("event_type") == "purchase")

# Maintenant, on a pour chaque achat le nombre de clics cumulés
# Calculer la moyenne
result = purchases.agg({"cumulative_clicks": "avg"}).withColumnRenamed("avg(cumulative_clicks)", "mean_clicks_before_purchase")

# Afficher le résultat
result.show()

spark.stop()
