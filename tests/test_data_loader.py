import unittest
import sys

from dataLoader import DataLoader

sys.path.append("src")


class TestDataLoader(unittest.TestCase):

    def test_nodes(self):
        data_loader = DataLoader("janos-us-ca.xml")
        self.assertEqual(data_loader.get_nodes()[0], "Vancouver")

    def test_links(self):
        data_loader = DataLoader("janos-us-ca.xml")
        self.assertEqual(
            str(data_loader.get_links()[0]), "Vancouver - Calgary"
        )

    def test_demands(self):
        data_loader = DataLoader("janos-us-ca.xml")
        self.assertEqual(
            str(data_loader.get_demands()[0]),
            "Vancouver - LosAngeles - 1770.0"
        )


if __name__ == '__main__':
    unittest.main()
