import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("⚠️ Clé API YouTube manquante ! Vérifie ton fichier .env")

YOUTUBE_TRENDING_URL = "https://www.googleapis.com/youtube/v3/videos"

params = {
    "part": "snippet,statistics",
    "chart": "mostPopular",
    "regionCode": "FR",
    "maxResults": 10,
    "key": API_KEY,
}

response = requests.get(YOUTUBE_TRENDING_URL, params=params)

if response.status_code == 200:
    data = response.json()
    print("✅ Données récupérées avec succès !")
else:
    print(f"❌ Erreur API : {response.status_code} - {response.text}")


import json

print(json.dumps(data, indent=2)[:500])


##### 2. Vérification de la structure des données
# Vérifier les clés disponibles dans le JSON
for item in data.get("items", []):
    print(item.keys())
    break


# Exemple avec la première vidéo
video = data["items"][0]

# Affichage des infos principales
print("📺 Titre :", video["snippet"]["title"])
print("📆 Date de publication :", video["snippet"]["publishedAt"])
print("🎭 Catégorie ID :", video["snippet"]["categoryId"])
print("👀 Nombre de vues :", video["statistics"].get("viewCount", "N/A"))
print("👍 Nombre de likes :", video["statistics"].get("likeCount", "N/A"))


##### 3. Vérification des valeurs manquantes / anomalies
import pandas as pd

df = pd.DataFrame(
    [
        {
            "titre": video["snippet"]["title"],
            "categorie_id": video["snippet"]["categoryId"],
            "views": video["statistics"].get("viewCount", 0),
            "likes": video["statistics"].get("likeCount", 0),
            "comments": video["statistics"].get("commentCount", 0),
            "publishedAt": item["snippet"]["publishedAt"],
        }
        for video in data.get("items", [])
    ]
)

print("📌 Nombre de valeurs nulles par colonne :\n", df.isnull().sum())


############# 🚀 Étape Suivante : Analyse Exploratoire des Données (EDA)

##  1. Vérifier la répartition des vidéos par catégorie
# Mapping des IDs vers noms de catégories
categories_dict = {
    "1": "Film & Animation",
    "2": "Autos & Vehicles",
    "10": "Music",
    "15": "Pets & Animals",
    "17": "Sports",
    "18": "Short Movies",
    "19": "Travel & Events",
    "20": "Gaming",
    "22": "People & Blogs",
    "23": "Comedy",
    "24": "Entertainment",
    "25": "News & Politics",
    "26": "How-to & Style",
    "27": "Education",
    "28": "Science & Technology",
}

df["categorie"] = df["categorie_id"].map(categories_dict)

print(df.head())


### 2. Graphique : Répartition des vidéos par catégorie
import matplotlib.pyplot as plt

category_counts = df["categorie"].value_counts()

plt.figure(figsize=(10, 5))
category_counts.plot(kind="bar", color="skyblue")
plt.title("Nombre de vidéos tendances par catégorie")
plt.xlabel("Catégorie")
plt.ylabel("Nombre de vidéos")
plt.xticks(rotation=45)
plt.show()


### 📈 3. Graphique : Corrélation entre vues et likes
import seaborn as sns

plt.figure(figsize=(8, 6))
sns.scatterplot(x=df["views"], y=df["likes"], alpha=0.7)

plt.title("Corrélation entre vues et likes sur YouTube")
plt.xlabel("Nombre de vues")
plt.ylabel("Nombre de likes")
plt.show()


################## 🔥 Identifier la vidéo la plus populaire
top_video = df.loc[df["views"].idxmax()]

print(f"📢 La vidéo la plus populaire est : {top_video['titre']}")
print(f"👀 Nombre de vues : {top_video['views']}")
print(f"👍 Nombre de likes : {top_video['likes']}")
print(f"🎭 Catégorie : {top_video['categorie']}")


#### DataFrame pour PowerBI
df.to_csv("youtube_trending_data.csv", index=False, encoding="utf-8")
print("✅ Fichier CSV exporté avec succès !")
