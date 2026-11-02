import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import validate


def row(ip="10.0.0.1", model="Cisco-2960", fw="15.2"):
    return {"device": "sw1", "ip": ip, "model": model, "firmware": fw}


class TestInventory(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(validate(row()), [])

    def test_bad_ip(self):
        self.assertIn("invalid IP", validate(row(ip="999.1.1.1")))

    def test_old_firmware(self):
        self.assertTrue(any("below minimum" in p for p in validate(row(fw="12.2"))))

    def test_unknown_model(self):
        self.assertIn("unknown model", validate(row(model="Mystery-1")))
