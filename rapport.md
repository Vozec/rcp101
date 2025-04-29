# Rapport Examen RCP101

L'ensemble du code est disponible [sur mon github](https://github.com/Vozec/rcp101)
*(Une archive zip est aussi fournie au cas-ou)*

## Etape 1:

### Installation MongoDB
```bash
sudo pacman -S mongodb
mkdir -p ~/data/db
mongod --dbpath ~/data/db
```

### Création de la bdd `ecommerce`

```bash
> use ecommerce
switched to db ecommerce
> db.createCollection("events")
{ "ok" : 1 }
```

### Importation des données JSON
```bash
$ mongoimport --db ecommerce --collection events --file ecommerce_events.json
2025-04-29T10:57:51.277+0200	connected to: mongodb://localhost/
2025-04-29T10:57:51.351+0200	10000 document(s) imported successfully. 0 document(s) failed to import.
```

### Création des index
```bash
> db.events.createIndex({ user_id: 1, event_type: 1 })
{
	"numIndexesBefore" : 1,
	"numIndexesAfter" : 2,
	"createdCollectionAutomatically" : true,
	"ok" : 1
}
> db.events.createIndex({ timestamp: 1 })
{
	"numIndexesBefore" : 2,
	"numIndexesAfter" : 3,
	"createdCollectionAutomatically" : false,
	"ok" : 1
}
>
```

### Justification des choix de modélisation:


#### Indexation

Deux index ont été créés pour optimiser les performances de lecture :
- Index *composite* : `{ user_id: 1, event_type: 1 }`
Ce choix permet d’accélérer les requêtes filtrant les événements d’un utilisateur donné. 

- Index *temporel* : `{ timestamp: 1 }`
Utile pour les analyses par période, cet index permet de faire l'étude temporelle des comportements (par heure, jour, semaine, etc.).

#### Clé primaire

Utilisation de *_id* généré automatiquement par MongoDB
Chaque document possède une clé unique ce qui garantit son intégrité sans avoir besoin de définir une clé primaire composite.

#### Collection principale : events

Tous les types d’événements (recherche, clic, achat) sont regroupés dans une seule collection pour faciliter les analyses 
globales et l'homogénéité des traitements.

### Requêtes optimisées

- Requête par *utilisateur*
```bash
> use ecommerce
switched to db ecommerce
> db.events.find({ user_id: "U2138" }).pretty()
{
	"_id" : ObjectId("6810948f0ee44c1fad99782e"),
	"user_id" : "U2138",
	"timestamp" : "2025-04-01T00:19:00",
	"event_type" : "search",
	"region" : "south",
	"search_query" : "python book"
}
>
```

- Requête par *période*
```bash
> db.events.find({ 
...     "timestamp": { 
...         $gte: "2025-02-01T00:00:00", 
...         $lte: "2025-05-01T23:59:59"
...     }
... }).sort({ "timestamp": 1 })
{ "_id" : ObjectId("6810948f0ee44c1fad998f0e"), "user_id" : "U1255", "timestamp" : "2025-04-01T00:00:00", "event_type" : "purchase", "region" : "north", "product_id" : "P0036", "category" : "home", "price" : 292.89 }
{ "_id" : ObjectId("6810948f0ee44c1fad998af3"), "user_id" : "U6142", "timestamp" : "2025-04-01T00:00:00", "event_type" : "search", "region" : "south", "search_query" : "headphones" }
{ "_id" : ObjectId("6810948f0ee44c1fad997e57"), "user_id" : "U3181", "timestamp" : "2025-04-01T00:00:00", "event_type" : "click", "region" : "north", "product_id" : "P0020", "category" : "books", "price" : 62.19 }
{ "_id" : ObjectId("6810948f0ee44c1fad998dce"), "user_id" : "U1082", "timestamp" : "2025-04-01T00:01:00", "event_type" : "search", "region" : "east", "search_query" : "headphones" }
{ "_id" : ObjectId("6810948f0ee44c1fad997d15"), "user_id" : "U4970", "timestamp" : "2025-04-01T00:02:00", "event_type" : "search", "region" : "west", "search_query" : "laptop" }
{ "_id" : ObjectId("6810948f0ee44c1fad998c55"), "user_id" : "U4804", "timestamp" : "2025-04-01T00:04:00", "event_type" : "search", "region" : "south", "search_query" : "lego" }
{ "_id" : ObjectId("6810948f0ee44c1fad999476"), "user_id" : "U3694", "timestamp" : "2025-04-01T00:04:00", "event_type" : "search", "region" : "north", "search_query" : "python book" }
{ "_id" : ObjectId("6810948f0ee44c1fad9999e1"), "user_id" : "U8059", "timestamp" : "2025-04-01T00:10:00", "event_type" : "click", "region" : "west", "product_id" : "P0069", "category" : "books", "price" : 204.83 }
{ "_id" : ObjectId("6810948f0ee44c1fad998169"), "user_id" : "U8920", "timestamp" : "2025-04-01T00:11:00", "event_type" : "click", "region" : "south", "product_id" : "P0035", "category" : "books", "price" : 38.89 }
{ "_id" : ObjectId("6810948f0ee44c1fad99780e"), "user_id" : "U7563", "timestamp" : "2025-04-01T00:12:00", "event_type" : "search", "region" : "west", "search_query" : "python book" }
{ "_id" : ObjectId("6810948f0ee44c1fad9984db"), "user_id" : "U6040", "timestamp" : "2025-04-01T00:13:00", "event_type" : "search", "region" : "south", "search_query" : "laptop" }
{ "_id" : ObjectId("6810948f0ee44c1fad99782e"), "user_id" : "U2138", "timestamp" : "2025-04-01T00:19:00", "event_type" : "search", "region" : "south", "search_query" : "python book" }
{ "_id" : ObjectId("6810948f0ee44c1fad998465"), "user_id" : "U4275", "timestamp" : "2025-04-01T00:26:00", "event_type" : "purchase", "region" : "north", "product_id" : "P0063", "category" : "sports", "price" : 219.27 }
{ "_id" : ObjectId("6810948f0ee44c1fad997ea7"), "user_id" : "U2275", "timestamp" : "2025-04-01T00:27:00", "event_type" : "search", "region" : "south", "search_query" : "lego" }
{ "_id" : ObjectId("6810948f0ee44c1fad999bc2"), "user_id" : "U1090", "timestamp" : "2025-04-01T00:27:00", "event_type" : "click", "region" : "north", "product_id" : "P0006", "category" : "electronics", "price" : 217.73 }
{ "_id" : ObjectId("6810948f0ee44c1fad998cf5"), "user_id" : "U7637", "timestamp" : "2025-04-01T00:28:00", "event_type" : "search", "region" : "north", "search_query" : "lego" }
{ "_id" : ObjectId("6810948f0ee44c1fad999a12"), "user_id" : "U9308", "timestamp" : "2025-04-01T00:30:00", "event_type" : "click", "region" : "east", "product_id" : "P0088", "category" : "home", "price" : 90.5 }
{ "_id" : ObjectId("6810948f0ee44c1fad998a9c"), "user_id" : "U2232", "timestamp" : "2025-04-01T00:30:00", "event_type" : "click", "region" : "west", "product_id" : "P0085", "category" : "sports", "price" : 42.52 }
{ "_id" : ObjectId("6810948f0ee44c1fad997af0"), "user_id" : "U8614", "timestamp" : "2025-04-01T00:30:00", "event_type" : "purchase", "region" : "north", "product_id" : "P0052", "category" : "toys", "price" : 290.53 }
{ "_id" : ObjectId("6810948f0ee44c1fad999127"), "user_id" : "U8665", "timestamp" : "2025-04-01T00:31:00", "event_type" : "purchase", "region" : "east", "product_id" : "P0030", "category" : "home", "price" : 71.91 }
Type "it" for more
```


## Etape 2:

### Installation de spark

```bash
pip install pyspark
pip install pymongo[srv]
```

### Connection de Spark à la DB NoSQL:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("EcommerceMongoAnalysis") \
    .config("spark.mongodb.read.connection.uri", "mongodb://127.0.0.1/ecommerce.events") \
    .config("spark.mongodb.write.connection.uri", "mongodb://127.0.0.1/ecommerce.results") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.2.1") \
    .getOrCreate()
```

### Lire les données
```python
df = spark.read.format("mongodb").load()
```

### Premier JOB: 

- *"Compter le nombre moyen de clicks avant achat"*

Voici la méthode utilisé: 
    - On ne prend que les événements de type click et purchase
    - On numérote chaque clic comme 1 et chaque achat comme 0
    - On cumule les clics successifs par utilisateur dans l'ordre du temps
    - À chaque achat, on sait combien de clics ont précédé
    - On calcule la moyenne sur tous les achats.

Le code python est disponible [ici](./spark_job_click.py)

Lancement de spark avec le premier Job
```bash
spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.12:10.2.1 spark_job_click.py
...
+---------------------------+
|mean_clicks_before_purchase|
+---------------------------+
|        0.16407425990968388|
+---------------------------+
...
```

L'ensemble de la trace d'execution est disponible [ici](./logs/job1.log)

### Second JOB:

- *"Identifier les catégories les plus recherchées par heure"*

Voici la méthode utilisée :
- On ne garde que les événements de type `click` avec une catégorie définie.
- On utilise la fonction `hour()` pour extraire l'heure à partir de la colonne `timestamp`.
- On compte le nombre de clics par heure et par catégorie, en considérant ces clics comme des indicateurs des recherches effectuées.
- On applique une fenêtre (`Window`) partitionnée par heure et triée par nombre de clics décroissant.
- On sélectionne la première ligne de chaque partition pour identifier la catégorie la plus cliquée (et donc la plus recherchée) par heure.
- On trie le résultat final par heure croissante.

Le code python est disponible [ici](./spark_job_categories.py)

```bash
spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.12:10.3.0 spark_job_categories.py 
...
+----+-----------+---------+
|hour|category   |nb_clicks|
+----+-----------+---------+
|0   |clothing   |21       |
|1   |books      |22       |
|2   |home       |24       |
|3   |home       |29       |
|4   |electronics|26       |
|5   |books      |28       |
|6   |clothing   |31       |
|7   |home       |30       |
|8   |home       |26       |
|9   |clothing   |23       |
|10  |books      |25       |
|11  |toys       |22       |
|12  |electronics|26       |
|13  |toys       |28       |
|14  |electronics|26       |
|15  |electronics|24       |
|16  |electronics|26       |
|17  |home       |24       |
|18  |toys       |29       |
|19  |books      |28       |
|20  |books      |26       |
|21  |home       |25       |
|22  |electronics|30       |
|23  |toys       |28       |
+----+-----------+---------+
...
```

L'ensemble de la trace d'execution est disponible [ici](./logs/job2.log)

### Troisième JOB:

- *"Générer un top 10 des produits les plus consultés par région (fictive, injectée)"*

Le code python est disponible [ici](./spark_job_top10.py)


```bash
spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.12:10.3.0 spark_job_top10.py 
...
+------+----------+---------+----+
|region|product_id|nb_clicks|rank|
+------+----------+---------+----+
|east  |P0075     |14       |1   |
|east  |P0051     |14       |2   |
|east  |P0069     |13       |3   |
|east  |P0042     |13       |4   |
|east  |P0054     |12       |5   |
|east  |P0083     |12       |6   |
|east  |P0086     |11       |7   |
|east  |P0023     |11       |8   |
|east  |P0048     |11       |9   |
|east  |P0034     |11       |10  |
|north |P0043     |16       |1   |
|north |P0079     |13       |2   |
|north |P0037     |13       |3   |
|north |P0080     |13       |4   |
|north |P0099     |12       |5   |
|north |P0014     |12       |6   |
|north |P0064     |12       |7   |
|north |P0069     |12       |8   |
|north |P0004     |11       |9   |
|north |P0008     |11       |10  |
|south |P0059     |13       |1   |
|south |P0094     |13       |2   |
|south |P0095     |13       |3   |
|south |P0032     |13       |4   |
|south |P0026     |12       |5   |
|south |P0085     |11       |6   |
|south |P0053     |11       |7   |
|south |P0062     |11       |8   |
|south |P0028     |11       |9   |
|south |P0009     |11       |10  |
|west  |P0032     |18       |1   |
|west  |P0055     |15       |2   |
|west  |P0047     |15       |3   |
|west  |P0039     |13       |4   |
|west  |P0095     |13       |5   |
|west  |P0001     |13       |6   |
|west  |P0016     |12       |7   |
|west  |P0024     |12       |8   |
|west  |P0022     |11       |9   |
|west  |P0084     |11       |10  |
+------+----------+---------+----+
...
```

L'ensemble de la trace d'execution est disponible [ici](./logs/job3.log)