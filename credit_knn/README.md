Classification du risque crédit — KNN
Modèle de classification supervisée basé sur l'algorithme K-Nearest Neighbors (KNN) appliqué au dataset German Credit. L'objectif est de prédire si un client présente un risque crédit good ou bad à partir de ses caractéristiques socio-financières.

Dataset

Source : https://github.com/selva86/datasets/blob/master/GermanCredit.csv
Taille : 1 000 observations, 21 variables
Cible : credit_risk — deux classes : good / bad
Déséquilibre : environ 70% good / 30% bad

Séparation des variables numériques et catégorielles

Etude de l'influence du choix de k et de la normalisation sur la précision du modèle

Méthodes de validation croisée

Evaluation de l'overfitting en fonction de k
