# TP1 Big Data - Resume d'execution Streamlit

Auteur : JOHN AGBESSI  
Formation : Genie logiciel

## 1. Objectif

Ce TP implemente un systeme de recommandation avec filtrage collaboratif item-item et une interface Streamlit.

Le programme lit un dataset de notes, calcule les similarites entre items, puis recommande les meilleurs items non encore notes par un utilisateur.

## 2. Environnement utilise

- Langage : Python
- Version testee : Python 3.11.9
- Bibliotheques : Streamlit et bibliotheque standard Python
- Execution : locale
- Systeme : Windows / PowerShell

## 3. Commandes executees

Depuis le dossier `TP1` :

```powershell
streamlit run app.py
```

La version console reste disponible :

```powershell
python recommender.py --user U1 --top-n 3 --show-similarities
```

## 4. Resultat obtenu

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

## 5. Interpretation

L'utilisateur `U1` a deja note :

- `I1` : Inception
- `I2` : Interstellar
- `I3` : The Matrix
- `I5` : The Martian

Le systeme exclut donc ces items et recommande uniquement des films non notes.

La recommandation `Gravity` obtient le meilleur score predit, car elle est proche des items bien notes par l'utilisateur selon les comportements des autres utilisateurs.

## 6. Methode utilisee

Le systeme suit les etapes suivantes :

1. lecture du fichier `ratings.csv`
2. creation des structures utilisateur-item et item-utilisateur
3. calcul des similarites cosinus entre items
4. prediction des scores pour les items non notes
5. tri des scores et affichage du top-N

## 7. Liens a remettre

Depot GitHub :

```text
https://github.com/John271200/TP1Recommendation-system.git
```

Application Streamlit :

```text
https://tp1recommendation-system.streamlit.app/
```

Professeur a ajouter au depot GitHub :

```text
johnaoga@gmail.com
```

## 8. Conclusion

Le programme produit correctement des recommandations top-N avec une approche collaborative item-item. L'interface Streamlit permet de tester le systeme facilement depuis un navigateur.
