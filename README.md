# Gestion d'inventaire

Petit projet Python pour gérer un stock de produits.

## Fonctionnalités

- ajouter un produit
- afficher les produits
- rechercher un produit
- mettre à jour une quantité
- supprimer un produit
- afficher les alertes de stock

## Prérequis

- Python 3

## Installer le projet

```bash
git clone https://github.com/T-R-Bama/gestion-inventaire.git
cd gestion-inventaire
```

## Lancer le projet

```bash
python3 inventaire.py
```

## Lancer les tests

Depuis le dossier parent du projet :

```bash
cd ..
python3 -m unittest discover -s gestion_inventaire -p "test_*.py" -v
```

Les tests vérifient l'ajout, la recherche, la modification et la suppression
de produits, ainsi que la validation des données et la sauvegarde JSON.

Le fichier `inventaire.json` est créé automatiquement pendant l'utilisation de
l'application. Il reste local et n'est pas envoyé sur GitHub.
