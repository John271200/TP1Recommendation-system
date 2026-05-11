# Rapport TP1 - Recommendation system

## Informations etudiant

Nom et prenoms : AGBESSI John Ulrich  
Filiere : Genie logiciel  
Ecole : IFRI-UAC  
Depot GitHub : https://github.com/John271200/TP1Recommendation-system.git  
Application Streamlit : https://tp1recommendation-system.streamlit.app/  

## 1. Introduction

Ce projet porte sur la realisation d'un systeme de recommandation base sur le filtrage collaboratif item-item. L'objectif est de proposer a un utilisateur une liste top-N d'items qu'il n'a pas encore notes, en utilisant les notes donnees par l'ensemble des utilisateurs.

Le projet contient aussi une interface Streamlit permettant de tester facilement le systeme depuis un navigateur.

## 2. Objectif du projet

L'objectif principal est de construire une application capable de :

- lire un fichier de notes utilisateur-item ;
- calculer les similarites entre les items ;
- predire les scores des items non notes par un utilisateur ;
- afficher les meilleures recommandations top-N ;
- rendre le systeme accessible via une application Streamlit.

## 3. Donnees utilisees

Le projet utilise deux fichiers CSV.

Le fichier `ratings.csv` contient les notes donnees par les utilisateurs :

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

Dans ce TP, les items representent des films. Le dataset est volontairement simple afin de bien montrer le fonctionnement de l'algorithme.

## 4. Methode utilisee

La methode utilisee est le filtrage collaboratif item-item. Elle consiste a comparer les items entre eux a partir des notes donnees par les utilisateurs.

### 4.1 Construction des matrices

Le programme commence par lire les notes et construit deux structures :

- une structure utilisateur-item, pour connaitre les notes de chaque utilisateur ;
- une structure item-utilisateur, pour connaitre les utilisateurs ayant note chaque item.

### 4.2 Calcul de la similarite

Pour chaque paire d'items, le programme construit deux vecteurs de notes. Une note manquante est consideree comme `0`.

La similarite utilisee est la similarite cosinus :

```text
similarite(A, B) = produit_scalaire(A, B) / (norme(A) * norme(B))
```

Une valeur proche de `1` signifie que les deux items ont des profils de notes proches.

### 4.3 Prediction des scores

Pour un utilisateur cible, le programme ignore les items deja notes. Pour chaque item candidat, il calcule un score predit avec une moyenne ponderee :

```text
score(item) = somme(similarite(item, item_note) * note) / somme(abs(similarite))
```

Les items sont ensuite tries par score decroissant pour obtenir le top-N.

## 5. Implementation

Le projet contient les principaux fichiers suivants :

- `recommender.py` : implementation de l'algorithme de recommandation ;
- `app.py` : interface Streamlit ;
- `ratings.csv` : notes des utilisateurs ;
- `items.csv` : noms des items ;
- `requirements.txt` : dependance Streamlit ;
- `README.md` : documentation du projet ;
- `EXECUTION_SUMMARY.md` : resume d'execution.

L'application Streamlit permet de choisir un utilisateur, de choisir le nombre de recommandations et d'afficher les similarites item-item.

## 6. Resultats obtenus

Commande console testee :

```powershell
python recommender.py --user U1 --top-n 3 --show-similarities
```

Sortie obtenue :

```text
Top similarites item-item
John Wick <-> Mad Max Fury Road : 0.986
The Matrix <-> Mad Max Fury Road : 0.977
The Matrix <-> John Wick : 0.962
Inception <-> The Martian : 0.898
Interstellar <-> The Martian : 0.828

Recommandations top-3 pour U1
1. Gravity (I7) - score predit : 4.27
2. Blade Runner 2049 (I8) - score predit : 2.69
3. John Wick (I4) - score predit : 1.94
```

Pour l'utilisateur `U1`, les films deja notes sont exclus des recommandations. Le systeme propose donc seulement des items non notes par cet utilisateur.

## 7. Deploiement

Le projet est disponible sur GitHub :

```text
https://github.com/John271200/TP1Recommendation-system.git
```

L'application Streamlit est disponible au lien suivant :

```text
https://tp1recommendation-system.streamlit.app/
```

Le professeur peut acceder au depot GitHub avec l'adresse :

```text
johnaoga@gmail.com
```

## 8. Conclusion

Ce TP a permis de mettre en place un systeme de recommandation top-N avec filtrage collaboratif item-item. L'approche est simple, interpretable et efficace pour comprendre les bases des systemes de recommandation.

L'ajout de Streamlit rend le projet plus accessible, car l'utilisateur peut tester les recommandations directement dans une interface web.
