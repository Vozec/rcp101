# Examen RCP101

Le rapport est disponible [ici](./rapport.md)

## Examen Pratique – Module : Gestion des Données à Large Échelle & Bases NoSQL

**Durée :** 2h  
**Modalité :** Examen sur machine, accès internet autorisé  
**Outils à disposition :** MongoDB ou Cassandra, Spark, HDFS (ou S3), Python (ou Scala), NoSQL Workbench ou Compass

---

## 🎯 Objectifs de l’épreuve :

- Concevoir et manipuler un modèle de données dans une base NoSQL adaptée à la volumétrie
- Évaluer les choix de modélisation (clé primaire, partitionnement, indexation)
- Construire un pipeline de traitement distribué (ex : Spark → NoSQL → Analyse)
- Appliquer des requêtes analytiques à partir de données semi-structurées ou non-structurées

---

## 📂 Contexte du cas pratique :

Une plateforme e-commerce souhaite analyser le comportement de ses utilisateurs (navigation, recherches, achats) en quasi-temps réel.  
Les données sont collectées sous forme de documents JSON contenant :

- `user_id`, `timestamp`, `event_type` (search, click, purchase)
- `product_id`, `category`, `price` (si achat ou clic)
- `search_query` (si type = search)

---

## 🧪 Travail demandé :

### Étape 1 — Ingestion & Modélisation NoSQL (MongoDB ou Cassandra) (30 pts)

- Créer une base `ecommerce` adaptée aux lectures rapides par utilisateur et par type d’événement.
- Importer un jeu d’exemples fournis (10k documents JSON).
- Justifier les choix de modélisation : collections, clé primaire, index.
- Fournir 2 requêtes d’accès optimisées (par `user_id` et par `date`).

---

### Étape 2 — Analyse des données avec Spark (30 pts)

- Connecter Spark à la base NoSQL choisie
- Écrire un job Spark pour :
  - Compter le nombre moyen de clics avant achat
  - Identifier les catégories les plus recherchées par heure
  - Générer un top 10 des produits les plus consultés par région (fictive, injectée)

---

## ✅ Éléments attendus :

- Code commenté, lisible et versionné (dépôt Git ou archive propre)
- Rapport PDF ou Markdown synthétique (modélisation, pipeline, choix techniques)
- Screenshots ou export des résultats clés (visualisations, performances)
