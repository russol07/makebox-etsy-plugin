import importlib.util
import json
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("listing_qa", ROOT / "scripts/check-listing.py")
qa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qa)


class ListingQA(unittest.TestCase):
    def setUp(self):
        self.packet = json.loads((ROOT / "examples/physical-desk-sign.json").read_text())

    def test_complete_example(self):
        self.assertTrue(qa.check(self.packet)["structural_valid"])

    def test_missing_tags(self):
        self.packet["tags"] = self.packet["tags"][:10]
        self.assertFalse(qa.check(self.packet)["structural_valid"])
        self.assertTrue(qa.check(self.packet, "native")["structural_valid"])

    def test_case_whitespace_unicode_duplicate(self):
        self.packet["tags"][1] = "  CUSTOM DESK SIGN "
        self.packet["tags"][0] = "custom desk sign"
        self.assertTrue(any("duplicate" in e for e in qa.check(self.packet)["errors"]))

    def test_limits_and_placeholder(self):
        self.packet["title"] = "x" * 141
        self.packet["description"] = "Made of [MATERIAL]"
        self.packet["tags"][0] = "a phrase longer than twenty"
        self.assertEqual(len(qa.check(self.packet)["errors"]), 3)

    def test_native_single_word(self):
        self.packet["tags"] = ["acrylic"]
        self.assertTrue(qa.check(self.packet, "native")["structural_valid"])
        self.assertFalse(qa.check(self.packet)["structural_valid"])

    def test_non_space_delimited_language(self):
        self.packet["tags"] = [f"名前看板{i}" for i in range(13)]
        self.packet["space_delimited_language"] = False
        self.assertTrue(qa.check(self.packet)["structural_valid"])

    def test_digital_physical_conflict(self):
        self.packet["type"] = "download"
        self.packet["variants"] = [{"color": "red"}]
        self.packet["shipping"] = {"profile": 12}
        self.assertEqual(len(qa.check(self.packet)["errors"]), 2)

    def test_partial_units_and_invalid_numbers(self):
        self.packet["package"] = {"length": 2, "weight": 1}
        self.packet["price"] = float("nan")
        self.packet["quantity"] = True
        self.assertEqual(len(qa.check(self.packet)["errors"]), 4)

    def test_long_description_not_truncated(self):
        self.packet["description"] = "Specifications and order instructions. " * 300
        original = deepcopy(self.packet)
        self.assertTrue(qa.check(self.packet)["structural_valid"])
        self.assertEqual(original, self.packet)

    def test_blockers_warn_not_false_publication(self):
        self.packet["blockers"] = ["shipping unknown"]
        self.packet["facts"] = [{"name": "material", "status": "conflicting"}]
        result = qa.check(self.packet)
        self.assertTrue(result["structural_valid"])
        self.assertTrue(any("blockers" in w for w in result["warnings"]))
        self.assertNotIn("ready_to_publish", result)

    def test_direct_and_local_personalization_limits(self):
        self.packet["personalization"][0]["max_allowed_characters"] = 1000
        self.assertTrue(qa.check(self.packet)["structural_valid"])
        self.packet["personalization_route"] = "local"
        self.assertFalse(qa.check(self.packet)["structural_valid"])

    def test_dropdown_option_shape(self):
        self.packet["personalization"] = [{"question_text": "Font", "question_type": "dropdown",
                                           "required": True, "options": [{"value": "Serif"}]}]
        self.assertFalse(qa.check(self.packet)["structural_valid"])
        self.packet["personalization"][0]["options"] = [{"label": "Serif"}]
        self.assertTrue(qa.check(self.packet)["structural_valid"])

    def test_title_symbols(self):
        self.packet["title"] = "Desk Sign ✨"
        self.assertFalse(qa.check(self.packet)["structural_valid"])
        self.packet["title"] = "Desk & Name & Sign"
        self.assertFalse(qa.check(self.packet)["structural_valid"])


if __name__ == "__main__":
    unittest.main()
