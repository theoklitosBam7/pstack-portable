"""Regression tests for harness-specific model config checks."""

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("verify", Path(__file__).with_name("verify.py"))
verify = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verify)


class ModelConfigTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        config_patch = patch.object(verify, "CONFIG_ROOT", self.root)
        config_patch.start()
        self.addCleanup(config_patch.stop)

    def write_config(self, harness, content):
        config = self.root / harness / "models"
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text(content)
        return config

    def validate(self):
        failures, warnings, notes = [], [], []
        verify.validate_model_configs(failures, warnings, notes)
        return failures, warnings, notes

    def test_each_adapter_names_its_own_config(self):
        adapters = verify.REPO / "skills" / "harness" / "references"
        for adapter in adapters.glob("*.md"):
            with self.subTest(harness=adapter.stem):
                expected = f"Model config: `~/.config/pstack/{adapter.stem}/models`."
                self.assertIn(expected, adapter.read_text())

    def test_missing_configs_use_harness_defaults(self):
        failures, warnings, notes = self.validate()
        self.assertEqual(failures, [])
        self.assertEqual(warnings, [])
        self.assertTrue(any("pi/models absent" in note for note in notes))
        self.assertTrue(any("codex/models absent" in note for note in notes))

    def test_legacy_shared_config_is_ignored_and_preserved(self):
        legacy = self.root / "models"
        legacy.write_text("invalid shared config\n")
        failures, warnings, notes = self.validate()
        self.assertEqual(failures, [])
        self.assertEqual(warnings, [])
        self.assertTrue(any("pi/models absent" in note for note in notes))
        self.assertEqual(legacy.read_text(), "invalid shared config\n")

    def test_distinct_harness_configs_are_validated_without_changes(self):
        pi = self.write_config("pi", "# Budget: medium\ncode: openai/pi-model\n")
        codex = self.write_config("codex", "code: openai/codex-model\n")
        failures, warnings, _ = self.validate()
        self.assertEqual(failures, [])
        self.assertEqual(warnings, [])
        self.assertEqual(pi.read_text(), "# Budget: medium\ncode: openai/pi-model\n")
        self.assertEqual(codex.read_text(), "code: openai/codex-model\n")

    def test_invalid_config_identifies_harness_path_and_line(self):
        self.write_config("pi", "code: auto\n")
        codex = self.write_config("codex", "# comment\ninvalid\n")
        failures, _, _ = self.validate()
        self.assertEqual(len(failures), 1)
        self.assertIn(f"{codex}:2", failures[0])

    def test_unknown_roles_and_empty_panel_entries_fail(self):
        self.write_config("pi", "unknown: auto\narena runners: auto, , inherit-parent\n")
        failures, _, _ = self.validate()
        self.assertEqual(len(failures), 2)
        self.assertIn("unknown role", failures[0])
        self.assertIn("empty list entry", failures[1])

    def test_aliases_and_panels_are_valid(self):
        self.write_config("pi", "code: auto\nfast: inherit-parent\narena runners: auto, openai/model\n")
        failures, warnings, _ = self.validate()
        self.assertEqual(failures, [])
        self.assertEqual(warnings, [])

    def test_model_without_provider_produces_path_specific_warning(self):
        config = self.write_config("pi", "code: model-slug\n")
        failures, warnings, _ = self.validate()
        self.assertEqual(failures, [])
        self.assertEqual(len(warnings), 1)
        self.assertIn(f"{config}:1", warnings[0])


if __name__ == "__main__":
    unittest.main()
