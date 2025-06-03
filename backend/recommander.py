import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient

# Créer le client Mongodb
client = MongoClient("mongodb://admin:admin@localhost:27007/")

# Accéder à la base et à la collection
db = client["product"]
collection = db["product"]

# Charger les documents MongoDB dans un DataFrame pandas
data = list(collection.find())  # retourne une liste de dictionnaires
df = pd.DataFrame(data)

# Supprimer l'_id automatique si nécessaire
if '_id' in df.columns:
    df = df.drop(columns=['_id'])

# Nettoyer les données : on garde les lignes non nulles
df = df.dropna(subset=['product_name', 'ingredients_text', 'countries_tags'])

# Préparation du texte
df['ingredients_text'] = df['ingredients_text'].astype(str).str.lower()
df['countries_tags'] = df['countries_tags'].astype(str).str.lower()

# Fonction de recommandation prenant en compte le pays
def recommend_recipes(user_ingredients, country='maroc', top_n=5):
    country = country.lower()
    filtered_df = df[df['countries_tags'] == country]
    if filtered_df.empty:
        # Si aucun produit pour ce pays, on retourne les meilleurs produits tous pays confondus
        filtered_df = df

    # Recalcule le TF-IDF pour le sous-ensemble filtré
    vectorizer = TfidfVectorizer(stop_words='english')
    filtered_tfidf_matrix = vectorizer.fit_transform(filtered_df['ingredients_text'])
    user_input = ' '.join(user_ingredients).lower()
    user_vector = vectorizer.transform([user_input])
    similarities = cosine_similarity(user_vector, filtered_tfidf_matrix).flatten()
    top_indices = similarities.argsort()[-top_n:][::-1]

    recommendations = filtered_df.iloc[top_indices][['product_name', 'ingredients_text', 'countries_tags']]
    recommendations['similarity'] = similarities[top_indices]
    return recommendations

def nettoyer_ingredients(texte):
    texte = texte.replace(";", ",").replace(".", ",")
    tokens = [t.strip().lower() for t in texte.split(",") if t.strip()]
    uniques = list(dict.fromkeys(tokens))
    return ", ".join(uniques)
