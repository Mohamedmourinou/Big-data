from flask import Flask, request, jsonify
from flask_cors import CORS
from recommender_model import recommend_by_each_ingredient

# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)

@app.route('/recommend', methods=['POST'])
def handle_recommendation():
    try:
        # Récupération des données envoyées par le frontend
        request_payload = request.json

        # Traitement de la chaîne brute d'ingrédients
        ingredients_text = request_payload.get("ingredients", "")
        ingredient_list = [
            item.strip().strip('"\'') 
            for item in ingredients_text.split(',') 
            if item.strip()
        ]

        if not ingredient_list:
            return jsonify({"error": "Aucun ingrédient fourni."}), 400

        # Initialisation des filtres dynamiques
        filter_criteria = {}
        user_country = request_payload.get("country")
        user_nutriscore = request_payload.get("nutriscore")
        user_nova_group = request_payload.get("nova_group")

        if user_country and user_country.lower() != "pays":
            filter_criteria["countries_en"] = user_country
        if user_nutriscore and user_nutriscore.lower() != "nutriscore":
            filter_criteria["nutriscore_grade"] = user_nutriscore
        if user_nova_group and user_nova_group.lower() != "nova_group":
            filter_criteria["nova_group"] = user_nova_group

        # Nombre de résultats recommandés à retourner
        max_results = request_payload.get("top_k", 5)

        # Appel au système de recommandation
        recommended_items = recommend_by_each_ingredient(
            ingredient_list, filter_criteria, max_results
        )

        # Formatage des résultats pour l'API
        formatted_results = recommended_items[
            ["product_name", "matched_ingredient", "nutriscore_grade", "countries_en", "brands"]
        ].to_dict(orient="records")

        return jsonify({"recommendations": formatted_results})

    except Exception as error:
        print(f"[Erreur] Recommandation échouée : {error}")
        return jsonify({"error": str(error)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

