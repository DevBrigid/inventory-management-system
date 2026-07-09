import subprocess
import unittest
from pathlib import Path


class CliCommandTests(unittest.TestCase):
    def test_root_cli_script_lists_inventory(self):
        repo_root = Path(__file__).resolve().parents[1]
        script_path = repo_root / "cli.py"

        self.assertTrue(script_path.exists(), "CLI entrypoint should exist")

        result = subprocess.run(
            ["python3", str(script_path), "list"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("Apples", result.stdout)


if __name__ == "__main__":
    unittest.main()
