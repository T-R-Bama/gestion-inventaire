import json
from pathlib import Path


def read_non_empty_text(value):
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("Le texte ne peut pas être vide.")
    return cleaned


def parse_positive_int(value):
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("La valeur doit être un nombre entier valide.") from exc
    if number < 0:
        raise ValueError("La valeur doit être supérieure ou égale à 0.")
    return number


def parse_positive_float(value):
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("La valeur doit être un nombre valide.") from exc
    if number < 0:
        raise ValueError("La valeur doit être supérieure ou égale à 0.")
    return number


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


def delete_product(products, nom):
    for produit in products:
        if produit["nom"].lower() == nom.lower():
            products.remove(produit)
            return True
    return False


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
        print("5. Supprimer un produit")
        print("6. Produits en rupture / faible stock")
        print("7. Quitter")

        choix = input("Votre choix : ")

        if choix == "1":
            try:
                nom = read_non_empty_text(input("Nom du produit : "))
                categorie = read_non_empty_text(input("Catégorie : "))
                quantite = parse_positive_int(input("Quantité : "))
                prix = parse_positive_float(input("Prix : "))
                seuil = parse_positive_int(input("Seuil d'alerte : "))
                add_product(products, nom, categorie, quantite, prix, seuil)
                save_products(products)
                print("Produit ajouté.")
            except ValueError as exc:
                print(f"Erreur : {exc}")

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
            try:
                nom = read_non_empty_text(input("Nom du produit à mettre à jour : "))
                nouvelle_qte = parse_positive_int(input("Nouvelle quantité : "))
                update_quantity(products, nom, nouvelle_qte)
                save_products(products)
                print("Quantité mise à jour.")
            except ValueError as exc:
                print(f"Erreur : {exc}")

        elif choix == "5":
            try:
                nom = read_non_empty_text(input("Nom du produit à supprimer : "))
                if delete_product(products, nom):
                    save_products(products)
                    print("Produit supprimé.")
                else:
                    print("Produit introuvable.")
            except ValueError as exc:
                print(f"Erreur : {exc}")

        elif choix == "6":
            alertes = low_stock_products(products)
            if not alertes:
                print("Aucune alerte de stock.")
            else:
                afficher_produits(alertes)

        elif choix == "7":
            print("Au revoir !")
            break

        else:
            print("Choix invalide.")


if __name__ == "__main__":
    menu()