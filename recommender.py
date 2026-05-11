import argparse
import csv
import math
from collections import defaultdict


def load_ratings(path):
    ratings_by_user = defaultdict(dict)
    ratings_by_item = defaultdict(dict)

    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_id = row["user_id"]
            item_id = row["item_id"]
            rating = float(row["rating"])
            ratings_by_user[user_id][item_id] = rating
            ratings_by_item[item_id][user_id] = rating

    return dict(ratings_by_user), dict(ratings_by_item)


def load_items(path):
    items = {}
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            items[row["item_id"]] = row["title"]
    return items


def cosine_similarity(item_a_ratings, item_b_ratings):
    users = set(item_a_ratings) | set(item_b_ratings)
    if not users:
        return 0.0

    numerator = sum(item_a_ratings.get(user, 0.0) * item_b_ratings.get(user, 0.0) for user in users)
    norm_a = math.sqrt(sum(item_a_ratings.get(user, 0.0) ** 2 for user in users))
    norm_b = math.sqrt(sum(item_b_ratings.get(user, 0.0) ** 2 for user in users))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return numerator / (norm_a * norm_b)


def build_item_similarities(ratings_by_item):
    similarities = defaultdict(dict)
    item_ids = sorted(ratings_by_item)

    for index, item_a in enumerate(item_ids):
        for item_b in item_ids[index + 1:]:
            similarity = cosine_similarity(ratings_by_item[item_a], ratings_by_item[item_b])
            similarities[item_a][item_b] = similarity
            similarities[item_b][item_a] = similarity

    return dict(similarities)


def recommend_for_user(user_id, ratings_by_user, similarities, top_n=3):
    if user_id not in ratings_by_user:
        raise ValueError(f"Utilisateur inconnu : {user_id}")

    user_ratings = ratings_by_user[user_id]
    scores = defaultdict(float)
    similarity_sums = defaultdict(float)

    for rated_item, rating in user_ratings.items():
        for candidate_item, similarity in similarities.get(rated_item, {}).items():
            if candidate_item in user_ratings or similarity <= 0:
                continue
            scores[candidate_item] += similarity * rating
            similarity_sums[candidate_item] += abs(similarity)

    predictions = []
    for item_id, score in scores.items():
        if similarity_sums[item_id] == 0:
            continue
        predicted_rating = score / similarity_sums[item_id]
        predictions.append((item_id, predicted_rating))

    predictions.sort(key=lambda item: (-item[1], item[0]))
    return predictions[:top_n]


def print_similarity_matrix(similarities, items, limit=5):
    pairs = []
    for item_a, related_items in similarities.items():
        for item_b, similarity in related_items.items():
            if item_a < item_b:
                pairs.append((item_a, item_b, similarity))

    pairs.sort(key=lambda pair: (-pair[2], pair[0], pair[1]))

    print("Top similarites item-item")
    for item_a, item_b, similarity in pairs[:limit]:
        print(f"{items.get(item_a, item_a)} <-> {items.get(item_b, item_b)} : {similarity:.3f}")


def main():
    parser = argparse.ArgumentParser(
        description="Systeme de recommandation item-item top-N avec filtrage collaboratif."
    )
    parser.add_argument("--ratings", default="ratings.csv", help="Chemin du fichier ratings.csv")
    parser.add_argument("--items", default="items.csv", help="Chemin du fichier items.csv")
    parser.add_argument("--user", default="U1", help="Utilisateur cible")
    parser.add_argument("--top-n", type=int, default=3, help="Nombre de recommandations")
    parser.add_argument("--show-similarities", action="store_true", help="Afficher les meilleures similarites")
    args = parser.parse_args()

    ratings_by_user, ratings_by_item = load_ratings(args.ratings)
    items = load_items(args.items)
    similarities = build_item_similarities(ratings_by_item)

    if args.show_similarities:
        print_similarity_matrix(similarities, items)
        print()

    recommendations = recommend_for_user(args.user, ratings_by_user, similarities, args.top_n)

    print(f"Recommandations top-{args.top_n} pour {args.user}")
    if not recommendations:
        print("Aucune recommandation disponible.")
        return

    for rank, (item_id, predicted_rating) in enumerate(recommendations, start=1):
        title = items.get(item_id, item_id)
        print(f"{rank}. {title} ({item_id}) - score predit : {predicted_rating:.2f}")


if __name__ == "__main__":
    main()
