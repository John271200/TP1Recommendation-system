# Rapport de projet - TP1 Big Data

## Recommendation system: Collaborative Filtering item-item top-N avec Streamlit

**Nom et prenoms :** AGBESSI John Ulrich  
**Filiere :** Genie logiciel  
**Ecole :** IFRI-UAC  
**Depot GitHub :** https://github.com/John271200/TP1Recommendation-system.git  
**Application Streamlit :** https://tp1recommendation-system.streamlit.app/  

---

## Resume

Ce projet consiste a developper un systeme de recommandation base sur le filtrage collaboratif item-item. Le systeme analyse les notes donnees par plusieurs utilisateurs a differents films, calcule les similarites entre les films, puis propose a un utilisateur cible une liste de recommandations top-N.

Le projet comporte deux modes d'utilisation :

- une version console avec `recommender.py` ;
- une interface web interactive avec `Streamlit`, implementee dans `app.py`.

L'application finale est publiee sur GitHub et deployee sur Streamlit Community Cloud.

---

## 1. Introduction

Les systemes de recommandation sont utilises dans de nombreux services numeriques : plateformes de streaming, sites de commerce electronique, reseaux sociaux, bibliotheques numeriques ou plateformes educatives. Leur objectif est de proposer automatiquement des contenus pertinents a un utilisateur en fonction de son historique ou du comportement d'autres utilisateurs.

Dans ce TP, le systeme developpe repose sur le **filtrage collaboratif item-item**. Cette approche ne se base pas sur le contenu des films, mais sur les notes attribuees par les utilisateurs. Deux films sont consideres comme proches si les utilisateurs les notent de maniere similaire.

L'interet de cette methode est qu'elle est relativement simple a comprendre et interpretable. Elle permet d'expliquer pourquoi un item est recommande : il est proche d'autres items deja apprecies par l'utilisateur.

---

## 2. Objectifs du projet

Les objectifs du TP sont les suivants :

- lire et exploiter un dataset utilisateur-item ;
- construire les structures de donnees necessaires au filtrage collaboratif ;
- calculer la similarite entre les items ;
- predire les scores des items non notes ;
- retourner une liste top-N de recommandations ;
- proposer une interface web simple avec Streamlit ;
- publier le code source sur GitHub ;
- deployer l'application en ligne sur Streamlit Community Cloud.

---

## 3. Donnees utilisees

Le projet utilise deux fichiers CSV.

### 3.1 Fichier des notes

Le fichier `ratings.csv` contient les notes donnees par les utilisateurs :

```text
user_id,item_id,rating
U1,I1,5
U1,I2,4
U1,I3,1
```

Chaque ligne correspond a une note donnee par un utilisateur a un item.

### 3.2 Fichier des items

Le fichier `items.csv` associe chaque identifiant d'item a un titre de film :

```text
item_id,title
I1,Inception
I2,Interstellar
I3,The Matrix
```

Le dataset utilise dans ce TP contient :

- 8 utilisateurs ;
- 8 films ;
- 32 notes.

Le dataset est volontairement reduit afin de rendre le calcul plus lisible et de faciliter l'explication de l'algorithme.

---

## 4. Architecture du projet

Le projet est organise de la maniere suivante :

```text
TP1/
  app.py
  recommender.py
  ratings.csv
  items.csv
  requirements.txt
  README.md
  EXECUTION_SUMMARY.md
  SUBMISSION_LINKS.md
  RAPPORT_TP1_AGBESSI_John_Ulrich.pdf
```

Role des principaux fichiers :

- `recommender.py` contient la logique de recommandation ;
- `app.py` contient l'interface Streamlit ;
- `ratings.csv` contient les notes utilisateur-item ;
- `items.csv` contient les noms des films ;
- `requirements.txt` contient les dependances du projet ;
- `README.md` explique comment executer le projet ;
- `EXECUTION_SUMMARY.md` presente les resultats d'execution ;
- `SUBMISSION_LINKS.md` regroupe les liens utiles pour la soumission.

---

## 5. Methode de recommandation

### 5.1 Principe du filtrage collaboratif item-item

Le filtrage collaboratif item-item consiste a comparer les items entre eux. Contrairement au filtrage user-user, qui cherche des utilisateurs similaires, l'approche item-item cherche des items ayant des profils de notation proches.

Dans ce projet, si un utilisateur a bien note un film, le systeme cherche d'autres films similaires a ce film et les recommande si l'utilisateur ne les a pas encore notes.

### 5.2 Construction des structures de donnees

Le programme construit deux dictionnaires :

- `ratings_by_user` : pour retrouver rapidement les notes donnees par un utilisateur ;
- `ratings_by_item` : pour retrouver rapidement les notes recues par un item.

Ces deux structures permettent de calculer les similarites et les recommandations sans parcourir inutilement tout le dataset a chaque etape.

### 5.3 Similarite cosinus

Pour comparer deux items, le programme utilise la similarite cosinus. Chaque item est represente par un vecteur de notes. Une note manquante est consideree comme `0`.

Formule :

```text
similarite(A, B) = (A . B) / (||A|| * ||B||)
```

Avec :

- `A . B` : produit scalaire des deux vecteurs ;
- `||A||` : norme du vecteur A ;
- `||B||` : norme du vecteur B.

Une similarite proche de `1` indique que les deux items sont notes de facon proche. Une similarite proche de `0` indique qu'ils sont peu lies selon les notes disponibles.

### 5.4 Prediction du score

Pour un utilisateur cible, le systeme parcourt les items deja notes. Pour chaque item non note, il calcule un score predit en utilisant une moyenne ponderee par les similarites.

Formule :

```text
score(item) = somme(similarite(item, item_note) * note) / somme(abs(similarite))
```

Les items deja notes par l'utilisateur sont exclus afin de ne recommander que de nouveaux films.

### 5.5 Generation du top-N

Apres le calcul des scores predits, les items candidats sont tries par score decroissant. Le programme retourne ensuite les `N` meilleurs items. Dans les tests, la valeur par defaut est `N = 3`.

---

## 6. Interface Streamlit

L'interface Streamlit permet d'utiliser le systeme sans passer par la ligne de commande. Elle offre les fonctionnalites suivantes :

- selection de l'utilisateur cible ;
- choix du nombre de recommandations ;
- affichage des notes deja donnees par l'utilisateur ;
- affichage du top-N des recommandations ;
- affichage des meilleures similarites item-item ;
- visualisation simple des donnees principales du projet.

Cette interface rend le projet plus accessible, car elle permet de tester les recommandations directement depuis un navigateur web.

---

## 7. Execution du projet

### 7.1 Installation

Depuis le dossier du projet :

```powershell
python -m pip install -r requirements.txt
```

### 7.2 Lancement de l'application Streamlit

```powershell
streamlit run app.py
```

### 7.3 Execution en mode console

```powershell
python recommender.py --user U1 --top-n 3 --show-similarities
```

---

## 8. Resultats obtenus

Pour l'utilisateur `U1`, la commande console donne les resultats suivants :

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

Interpretation :

- `U1` a deja note plusieurs films, dont `Inception`, `Interstellar`, `The Matrix` et `The Martian` ;
- ces films sont exclus des recommandations ;
- `Gravity` obtient le meilleur score predit ;
- le top-N final contient uniquement des films non encore notes par l'utilisateur.

---

## 9. Deploiement et soumission

Le depot GitHub du projet est disponible ici :

```text
https://github.com/John271200/TP1Recommendation-system.git
```

L'application Streamlit deployee est disponible ici :

```text
https://tp1recommendation-system.streamlit.app/
```

Le professeur doit etre ajoute au depot GitHub avec l'adresse suivante :

```text
johnaoga@gmail.com
```

---

## 10. Limites du projet

Le projet fonctionne correctement pour illustrer le principe du filtrage collaboratif item-item. Cependant, certaines limites existent :

- le dataset utilise est petit ;
- les notes manquantes sont remplacees par `0`, ce qui simplifie le calcul ;
- il n'y a pas encore de gestion avancee du probleme de cold start ;
- l'evaluation du modele n'inclut pas de metriques comme RMSE, precision ou recall ;
- le systeme ne combine pas encore les donnees collaboratives avec des caracteristiques de contenu.

Ces limites sont normales dans le cadre d'un TP introductif. Elles ouvrent des pistes d'amelioration pour une version plus avancee.

---

## 11. Perspectives d'amelioration

Pour ameliorer le projet, il serait possible de :

- utiliser un dataset plus grand, par exemple MovieLens ;
- ajouter une separation train/test ;
- evaluer la qualite des recommandations avec des metriques ;
- comparer item-item avec user-user ;
- ajouter une matrice de similarite visualisable dans l'interface ;
- permettre l'import d'un fichier CSV depuis Streamlit ;
- ajouter une base de donnees pour stocker les notes ;
- ameliorer le design de l'application Streamlit.

---

## 12. Conclusion

Ce TP a permis de construire un systeme de recommandation top-N base sur le filtrage collaboratif item-item. Le projet montre toutes les etapes essentielles : lecture des donnees, construction des matrices, calcul de similarite, prediction des scores et affichage des recommandations.

L'utilisation de Streamlit apporte une interface simple et pratique pour tester le systeme. Le deploiement en ligne permet aussi de rendre le projet accessible au professeur et a toute personne disposant du lien.

Ce travail constitue donc une base solide pour comprendre le fonctionnement des systemes de recommandation et pour aller vers des approches plus avancees.
