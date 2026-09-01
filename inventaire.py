import json
from pathlib import Path


def load_products(file_path="inventaire.json"):
    path = Path(file_path)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []


def save_products(products, file_path="inventaire.json"):
    path = Path(file_path)
    with path.open("w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)


def add_product(products, nom, categorie, quantite, prix, seuil_alerte=0):
    nouveau = {
        "nom": nom.strip(),
        "categorie": categorie.strip(),
        "quantite": int(quantite),
        "prix": float(prix),
        "seuil_alerte": int(seuil_alerte),
    }
    products.append(nouveau)
    return products


def search_products(products, terme):
    terme = terme.lower().strip()
    if not terme:
        return products
    return [
        produit
        for produit in products
        if terme in produit["nom"].lower() or terme in produit["categorie"].lower()
    ]


def low_stock_products(products):
    return [
        produit
        for produit in products
        if produit["quantite"] <= produit["seuil_alerte"]
    ]


def update_quantity(products, nom, nouvelle_quantite):
    for produit in products:
        if produit["nom"].lower() == nom.lower():
            produit["quantite"] = int(nouvelle_quantite)
            return products
    return products


def afficher_produits(products):
    if not products:
        print("Aucun produit en stock.")
        return

    print("\nListe des produits :")
    for idx, produit in enumerate(products, start=1):
        print(
            f"{idx}. {produit['nom']} | "
            f"Catégorie: {produit['categorie']} | "
            f"Quantité: {produit['quantite']} | "
            f"Prix: {produit['prix']} € | "
            f"Seuil alerte: {produit['seuil_alerte']}"
        )


def menu():
    products = load_products()

    while True:
        print("\n=== GESTION D'INVENTAIRE ===")
        print("1. Ajouter un produit")
        print("2. Afficher les produits")
        print("3. Rechercher un produit")
        print("4. Mettre à jour la quantité")
        print("5. Produits en rupture / faible stock")
        print("6. Quitter")

        choix = input("Votre choix : ")

        if choix == "1":
            nom = input("Nom du produit : ")
            categorie = input("Catégorie : ")
            quantite = int(input("Quantité : "))
            prix = float(input("Prix : "))
            seuil = int(input("Seuil d'alerte : "))
            add_product(products, nom, categorie, quantite, prix, seuil)
            save_products(products)
            print("Produit ajouté.")

        elif choix == "2":
            afficher_produits(products)

        elif choix == "3":
            terme = input("Entrez un nom ou une catégorie : ")
            resultats = search_products(products, terme)
            if not resultats:
                print("Aucun résultat.")
            else:
                afficher_produits(resultats)

        elif choix == "4":
            nom = input("Nom du produit à mettre à jour : ")
            nouvelle_qte = int(input("Nouvelle quantité : "))
            update_quantity(products, nom, nouvelle_qte)
            save_products(products)
            print("Quantité mise à jour.")

        elif choix == "5":
            alertes = low_stock_products(products)
            if not alertes:
                print("Aucune alerte de stock.")
            else:
                afficher_produits(alertes)

        elif choix == "6":
            print("Au revoir !")
            break

        else:
            print("Choix invalide.")


if __name__ == "__main__":
    menu()
