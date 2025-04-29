# Rapport Examen RCP101

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
