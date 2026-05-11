from pathlib import Path

import streamlit as st

from recommender import build_item_similarities, load_items, load_ratings, recommend_for_user


BASE_DIR = Path(__file__).parent
RATINGS_PATH = BASE_DIR / "ratings.csv"
ITEMS_PATH = BASE_DIR / "items.csv"


@st.cache_data
def load_data():
    ratings_by_user, ratings_by_item = load_ratings(RATINGS_PATH)
    items = load_items(ITEMS_PATH)
    similarities = build_item_similarities(ratings_by_item)
    return ratings_by_user, ratings_by_item, items, similarities


def get_top_similarities(similarities, items, limit=10):
    rows = []
    for item_a, related_items in similarities.items():
        for item_b, similarity in related_items.items():
            if item_a < item_b:
                rows.append(
                    {
                        "Item A": items.get(item_a, item_a),
                        "Item B": items.get(item_b, item_b),
                        "Similarite": round(similarity, 3),
                    }
                )

    rows.sort(key=lambda row: (-row["Similarite"], row["Item A"], row["Item B"]))
    return rows[:limit]


def get_user_ratings(user_id, ratings_by_user, items):
    rows = []
    for item_id, rating in sorted(ratings_by_user[user_id].items()):
        rows.append(
            {
                "Item": items.get(item_id, item_id),
                "Note": rating,
            }
        )
    return rows


def get_recommendation_rows(recommendations, items):
    rows = []
    for rank, (item_id, score) in enumerate(recommendations, start=1):
        rows.append(
            {
                "Rang": rank,
                "Item recommande": items.get(item_id, item_id),
                "Score predit": round(score, 2),
            }
        )
    return rows


def main():
    st.set_page_config(
        page_title="TP1 - Recommendation system",
        layout="wide",
    )

    ratings_by_user, ratings_by_item, items, similarities = load_data()

    st.title("TP1 - Recommendation system")
    st.caption("Collaborative Filtering item-item top-N")

    with st.sidebar:
        st.header("Parametres")
        user_id = st.selectbox("Utilisateur", sorted(ratings_by_user))
        top_n = st.slider("Nombre de recommandations", 1, len(items), 3)
        show_similarities = st.checkbox("Afficher les similarites item-item", value=True)

    recommendations = recommend_for_user(user_id, ratings_by_user, similarities, top_n)

    metric_cols = st.columns(3)
    metric_cols[0].metric("Utilisateurs", len(ratings_by_user))
    metric_cols[1].metric("Items", len(ratings_by_item))
    metric_cols[2].metric("Notes", sum(len(ratings) for ratings in ratings_by_user.values()))

    left_col, right_col = st.columns([1, 2])

    with left_col:
        st.subheader(f"Notes de {user_id}")
        st.dataframe(get_user_ratings(user_id, ratings_by_user, items), use_container_width=True)

    with right_col:
        st.subheader(f"Top-{top_n} recommandations")
        recommendation_rows = get_recommendation_rows(recommendations, items)
        if recommendation_rows:
            st.dataframe(recommendation_rows, use_container_width=True, hide_index=True)
        else:
            st.info("Aucune recommandation disponible pour cet utilisateur.")

    if show_similarities:
        st.subheader("Meilleures similarites item-item")
        st.dataframe(get_top_similarities(similarities, items), use_container_width=True, hide_index=True)

    with st.expander("Principe de calcul"):
        st.write(
            "Le programme calcule la similarite cosinus entre les items, puis predit les scores "
            "des items non notes par l'utilisateur avec une moyenne ponderee par les similarites."
        )


if __name__ == "__main__":
    main()
