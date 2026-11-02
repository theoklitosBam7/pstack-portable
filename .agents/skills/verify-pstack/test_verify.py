"""Regression tests for harness-specific model config checks."""

import contextlib
import importlib.util
import io
import json
import shutil
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

    def test_model_without_provider_is_accepted(self):
        self.write_config("codex", "code: model-slug\n")
        failures, warnings, _ = self.validate()
        self.assertEqual(failures, [])
        self.assertEqual(warnings, [])


class InstallTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.repo = (self.root / "repo").resolve()
        self.install = self.root / "install"
        self.lock = self.root / "lock.json"
        self.install.mkdir()
        (self.repo / "agents").mkdir(parents=True)
        for name in ("alpha", "beta"):
            skill = self.repo / "skills" / name
            (skill / "nested").mkdir(parents=True)
            (skill / "SKILL.md").write_text(name)
            (skill / "nested" / "data").write_text("data")
            (skill / "nested" / "link").symlink_to("data")
        for key, value in (("REPO", self.repo), ("INSTALL", self.install),
                           ("LOCK", self.lock), ("CONFIG_ROOT", self.root / "config")):
            patcher = patch.object(verify, key, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def copy(self, name):
        shutil.copytree(self.repo / "skills" / name, self.install / name, symlinks=True)

    def write_lock(self, names):
        self.lock.write_text(json.dumps({"skills": {
            name: {"source": verify.PSTACK_SOURCE, "skillPath": f"skills/{name}/SKILL.md"}
            for name in names
        }}))

    def doctor(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            try:
                verify.cmd_doctor()
            except SystemExit as exc:
                return exc.code, output.getvalue()
        return 0, output.getvalue()

    def test_exact_copies_and_nested_symlinks_pass_without_changes(self):
        self.copy("alpha")
        self.copy("beta")
        self.assertEqual(self.doctor()[0], 0)
        self.assertEqual((self.install / "alpha" / "nested" / "link").readlink(), Path("data"))

    def test_copy_drift_extra_missing_and_symlink_differences_fail(self):
        for change in ("content", "extra", "missing", "symlink"):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as tmp:
                source = Path(tmp) / "source"
                installed = Path(tmp) / "installed"
                shutil.copytree(self.repo / "skills" / "alpha", source, symlinks=True)
                shutil.copytree(source, installed, symlinks=True)
                if change == "content":
                    (installed / "nested" / "data").write_text("different")
                elif change == "extra":
                    (installed / "extra").write_text("extra")
                elif change == "missing":
                    (installed / "nested" / "data").unlink()
                else:
                    (installed / "nested" / "link").unlink()
                    (installed / "nested" / "link").symlink_to("other")
                self.assertIsNotNone(verify.compare_skill_copy(source, installed))

    def test_mixed_copy_and_checkout_symlink_pass(self):
        self.copy("alpha")
        (self.install / "beta").symlink_to(self.repo / "skills" / "beta")
        self.assertEqual(self.doctor()[0], 0)

    def test_partial_lock_warns_for_proven_manual_install(self):
        self.copy("alpha")
        self.copy("beta")
        self.write_lock(["alpha"])
        code, output = self.doctor()
        self.assertEqual(code, 0)
        self.assertIn("warning: lock drift:", output)
        self.assertNotIn("lock: " + str(self.lock) + " covers", output)

    def test_partial_lock_and_drift_fail(self):
        self.copy("alpha")
        self.copy("beta")
        self.write_lock(["alpha"])
        (self.install / "beta" / "SKILL.md").write_text("stale")
        code, output = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("differs", output)
        self.assertIn("FAIL: lock:", output)

    def test_valid_cli_lock_preserves_existing_directory_behavior(self):
        for name in ("alpha", "beta"):
            (self.install / name).mkdir()
            (self.install / name / "SKILL.md").write_text("CLI version")
        self.write_lock(["alpha", "beta"])
        code, output = self.doctor()
        self.assertEqual(code, 0)
        self.assertIn("covers 2 checkout skill(s)", output)
        (self.install / "beta" / "SKILL.md").unlink()
        self.assertEqual(self.doctor()[0], 1)

    def test_external_symlink_fails(self):
        self.copy("alpha")
        (self.install / "beta").symlink_to(self.root)
        self.assertEqual(self.doctor()[0], 1)


if __name__ == "__main__":
    unittest.main()
