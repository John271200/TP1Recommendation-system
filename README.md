# TP1 Big Data - Recommendation system avec Collaborative Filtering et Streamlit

Auteur : JOHN AGBESSI  
Formation : Genie logiciel

## 1. Objectif du TP

Ce TP implemente un systeme de recommandation base sur le filtrage collaboratif item-item avec une interface Streamlit.

Le but est de recommander les `N` meilleurs items a un utilisateur cible, a partir des notes donnees par les autres utilisateurs. L'approche utilisee est :

- construction d'une matrice utilisateur-item
- calcul de la similarite entre les items
- prediction des scores des items non notes par l'utilisateur
- selection des meilleures recommandations top-N

## 2. Fichiers fournis

```text
TP1/
  recommender.py
  app.py
  ratings.csv
  items.csv
  output.txt
  requirements.txt
  README.md
  EXECUTION_SUMMARY.md
  SUBMISSION_LINKS.md
```

## 3. Dataset

Le fichier `ratings.csv` contient les notes sous la forme :

```text
user_id,item_id,rating
U1,I1,5
U1,I2,4
```

Le fichier `items.csv` contient les noms des items :

```text
item_id,title
I1,Inception
I2,Interstellar
```

## 4. Installation

Installer les dependances depuis le dossier `TP1` :

```powershell
python -m pip install -r requirements.txt
```

## 5. Lancer l'application Streamlit

Depuis le dossier `TP1` :

```powershell
streamlit run app.py
```

L'application permet de :

- choisir un utilisateur
- choisir le nombre de recommandations top-N
- afficher les notes deja donnees par l'utilisateur
- afficher les recommandations
- afficher les meilleures similarites item-item

## 6. Executer aussi la version console

Depuis le dossier `TP1` :

```powershell
python recommender.py
```

## 7. Executer une recommandation top-N

Commande par defaut :

```powershell
python recommender.py
```

Cette commande genere les 3 meilleures recommandations pour l'utilisateur `U1`.

Pour choisir un autre utilisateur et un autre nombre de recommandations :

```powershell
python recommender.py --user U4 --top-n 3
```

Pour afficher aussi les similarites item-item les plus fortes :

```powershell
python recommender.py --user U1 --top-n 3 --show-similarities
```

## 8. Principe de l'algorithme

### 8.1 Similarite item-item

Pour chaque paire d'items, le programme construit deux vecteurs de notes sur l'ensemble des utilisateurs. Une note manquante est consideree comme `0`, puis le programme calcule une similarite cosinus :

```text
similarite(A, B) = produit_scalaire(A, B) / (norme(A) * norme(B))
```

Une similarite proche de `1` indique que les deux items sont apprecies de maniere similaire par les utilisateurs.

### 8.2 Prediction du score

Pour un utilisateur cible, le programme regarde les items qu'il a deja notes. Pour chaque item non note, il calcule un score predit avec une moyenne ponderee :

```text
score(item) = somme(similarite(item, item_note) * note) / somme(abs(similarite))
```

Les items deja notes par l'utilisateur sont exclus des recommandations.

### 8.3 Top-N

Les items candidats sont tries par score predit decroissant. Les `N` meilleurs sont retournes comme recommandations.

## 9. Exemple de sortie console

```text
Recommandations top-3 pour U1
1. Gravity (I7) - score predit : 4.27
2. Blade Runner 2049 (I8) - score predit : 2.69
3. John Wick (I4) - score predit : 1.94
```

## 10. Liens a remettre

Depot GitHub :

```text
https://github.com/John271200/TP1Recommendation-system.git
```

Application Streamlit :

```text
A COMPLETER : coller ici le lien Streamlit Community Cloud
```

Professeur a ajouter au depot GitHub :

```text
johnaoga@gmail.com
```

Sur GitHub, il faut ajouter ce mail comme collaborateur ou partager le depot avec ce compte. Sur Streamlit Community Cloud, il faut deployer `TP1/app.py` depuis le depot GitHub.

## 11. Conclusion

Ce TP montre le fonctionnement d'un systeme de recommandation collaboratif item-item. L'approche est simple, interpretable et adaptee aux recommandations top-N lorsque l'on dispose d'un historique de notes utilisateur-item.
