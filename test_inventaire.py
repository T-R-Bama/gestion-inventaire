import json
from pathlib import Path

from inventaire import (
    add_product,
    load_products,
    save_products,
    search_products,
    low_stock_products,
    update_quantity,
)


def test_add_product():
    products = []
    result = add_product(products, "Laptop", "Electronique", 4, 899.99, 2)
    assert result[0]["nom"] == "Laptop"
    assert result[0]["quantite"] == 4
    assert result[0]["prix"] == 899.99


def test_search_products():
    products = [
        {"nom": "Laptop", "categorie": "Electronique", "quantite": 4, "prix": 899.99, "seuil_alerte": 2},
        {"nom": "Souris", "categorie": "Accessoire", "quantite": 12, "prix": 19.5, "seuil_alerte": 5},
    ]
    matches = search_products(products, "laptop")
    assert len(matches) == 1
    assert matches[0]["categorie"] == "Electronique"


def test_low_stock_products():
    products = [
        {"nom": "Laptop", "categorie": "Electronique", "quantite": 1, "prix": 899.99, "seuil_alerte": 2},
        {"nom": "Souris", "categorie": "Accessoire", "quantite": 12, "prix": 19.5, "seuil_alerte": 5},
    ]
    low = low_stock_products(products)
    assert [p["nom"] for p in low] == ["Laptop"]


def test_update_quantity():
    products = [{"nom": "Laptop", "categorie": "Electronique", "quantite": 4, "prix": 899.99, "seuil_alerte": 2}]
    updated = update_quantity(products, "Laptop", 10)
    assert updated[0]["quantite"] == 10


def test_save_and_load_products(tmp_path):
    file_path = tmp_path / "inventaire.json"
    products = [{"nom": "Clavier", "categorie": "Accessoire", "quantite": 7, "prix": 39.99, "seuil_alerte": 3}]
    save_products(products, file_path)
    loaded = load_products(file_path)
    assert loaded == products
