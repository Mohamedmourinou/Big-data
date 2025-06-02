import pandas as pd


def recommend_products(ingredients_list, country=None, nutriscore=None, nova_group=None, top_k=5):


    df = MOCK_DATABASE.copy()

    # Filtrage par pays
    if country and country.lower() != "pays":
        df = df[df["countries_en"].str.lower() == country.lower()]

    # Filtrage par nutriscore
    if nutriscore and nutriscore.lower() != "nutriscore":
        df = df[df["nutriscore_grade"].str.lower() == nutriscore.lower()]

    # Filtrage par nova group
    if nova_group and str(nova_group).lower() != "nova_group":
        df = df[df["nova_group"] == int(nova_group)]

    # Calcul du score : nombre d'ingrédients correspondants
    def match_score(row):
        matches = set(ingredients_list) & set(row["ingredients"])
        return len(matches), list(matches)  # renvoie le nombre + liste des ingrédients trouvés

    df["match_count"], df["matched_ingredient"] = zip(*df.apply(match_score, axis=1))

    # Garder uniquement les produits avec au moins un ingrédient correspondant
    df = df[df["match_count"] > 0]

    # Trier par nombre d’ingrédients correspondants
    df_sorted = df.sort_values(by="match_count", ascending=False)

    return df_sorted.head(top_k)

