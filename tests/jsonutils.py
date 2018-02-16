from unittest import TestCase

import json
from pytable.core import jsonutils


class JsonUtilsTest(TestCase):
    def setUp(self):
        # vide
        self.data1 = {}
        # présent avec une valeur
        self.data2 = {"pos": 5}
        # présent avec un vecteur
        self.data3 = {"pos": {"x": 1, "y": 2, "z": 3}}

    def test_check_key_not_present(self):
        jsonutils.check_key(self.data1, "pos", 1)
        self.assertTrue("pos" in self.data1, "key added")
        self.assertEqual(self.data1["pos"], 1, "added key has the right value")

    def test_check_key_present(self):
        jsonutils.check_key(self.data2, "pos", 1)
        self.assertTrue("pos" in self.data2, "key still here")
        self.assertEqual(self.data2["pos"], 5, "key not modified")

    def test_check_vector_key_not_present(self):
        jsonutils.check_vector_key(self.data2, "pos")
        self.assertTrue("pos" in self.data2, "key still here")

        self.assertTrue("x" in self.data2["pos"], "x is present")
        self.assertEqual(self.data2["pos"]["x"], 0)
        self.assertTrue("y" in self.data2["pos"], "y is present")
        self.assertEqual(self.data2["pos"]["y"], 0)
        self.assertTrue("z" in self.data2["pos"], "z is present")
        self.assertEqual(self.data2["pos"]["z"], 0)

    def test_check_vector_key_present(self):
        jsonutils.check_vector_key(self.data3, "pos")
        self.assertTrue("pos" in self.data3, "key still here")

        self.assertTrue("x" in self.data3["pos"], "x is present")
        self.assertEqual(self.data3["pos"]["x"], 1)
        self.assertTrue("y" in self.data3["pos"], "y is present")
        self.assertEqual(self.data3["pos"]["y"], 2)
        self.assertTrue("z" in self.data3["pos"], "z is present")
        self.assertEqual(self.data3["pos"]["z"], 3)
