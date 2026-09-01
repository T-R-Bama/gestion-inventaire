import unittest
from pathlib import Path

from gestion_inventaire.inventaire import (
    add_product,
    delete_product,
    load_products,
    parse_positive_float,
    parse_positive_int,
    read_non_empty_text,
    save_products,
    search_products,
    low_stock_products,
    update_quantity,
)


class TestInventory(unittest.TestCase):
    def test_add_product(self):
        products = []
        result = add_product(products, "Laptop", "Electronique", 4, 899.99, 2)
        self.assertEqual(result[0]["nom"], "Laptop")
        self.assertEqual(result[0]["quantite"], 4)
        self.assertEqual(result[0]["prix"], 899.99)

    def test_search_products(self):
        products = [
            {"nom": "Laptop", "categorie": "Electronique", "quantite": 4, "prix": 899.99, "seuil_alerte": 2},
            {"nom": "Souris", "categorie": "Accessoire", "quantite": 12, "prix": 19.5, "seuil_alerte": 5},
        ]
        matches = search_products(products, "laptop")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["categorie"], "Electronique")

    def test_low_stock_products(self):
        products = [
            {"nom": "Laptop", "categorie": "Electronique", "quantite": 1, "prix": 899.99, "seuil_alerte": 2},
            {"nom": "Souris", "categorie": "Accessoire", "quantite": 12, "prix": 19.5, "seuil_alerte": 5},
        ]
        low = low_stock_products(products)
        self.assertEqual([p["nom"] for p in low], ["Laptop"])

    def test_update_quantity(self):
        products = [{"nom": "Laptop", "categorie": "Electronique", "quantite": 4, "prix": 899.99, "seuil_alerte": 2}]
        updated = update_quantity(products, "Laptop", 10)
        self.assertEqual(updated[0]["quantite"], 10)

    def test_delete_product(self):
        products = [
            {"nom": "Laptop", "categorie": "Electronique", "quantite": 4, "prix": 899.99, "seuil_alerte": 2},
            {"nom": "Souris", "categorie": "Accessoire", "quantite": 12, "prix": 19.5, "seuil_alerte": 5},
        ]
        deleted = delete_product(products, "Laptop")
        self.assertTrue(deleted)
        self.assertEqual([p["nom"] for p in products], ["Souris"])

    def test_read_non_empty_text(self):
        self.assertEqual(read_non_empty_text("  Ordinateur  "), "Ordinateur")
        with self.assertRaises(ValueError):
            read_non_empty_text("   ")

    def test_parse_positive_int(self):
        self.assertEqual(parse_positive_int("5"), 5)
        with self.assertRaises(ValueError):
            parse_positive_int("-1")
        with self.assertRaises(ValueError):
            parse_positive_int("abc")

    def test_parse_positive_float(self):
        self.assertEqual(parse_positive_float("99.99"), 99.99)
        with self.assertRaises(ValueError):
            parse_positive_float("-1")
        with self.assertRaises(ValueError):
            parse_positive_float("abc")

    def test_save_and_load_products(self):
        file_path = Path("/tmp/inventaire-test.json")
        products = [{"nom": "Clavier", "categorie": "Accessoire", "quantite": 7, "prix": 39.99, "seuil_alerte": 3}]
        save_products(products, file_path)
        loaded = load_products(file_path)
        self.assertEqual(loaded, products)


if __name__ == "__main__":
    unittest.main()


