from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_DIR = Path(__file__).resolve().parent.parent
LAUNCHER = REPO_DIR / "scripts" / "generar_newsletter_quincenal.sh"


class NewsletterLauncherTest(unittest.TestCase):
    def setUp(self) -> None:
        self.git_status_before = self._repo_status()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_dir = Path(self.temp_dir.name) / "project"
        self.scripts_dir = self.project_dir / "scripts"
        self.scripts_dir.mkdir(parents=True)
        shutil.copy2(LAUNCHER, self.scripts_dir / LAUNCHER.name)

        python_link = self.project_dir / ".venv" / "bin" / "python"
        python_link.parent.mkdir(parents=True)
        python_link.symlink_to(sys.executable)
        (self.project_dir / ".env").write_text("TEST_ONLY=1\n", encoding="utf-8")

        fake_bin = self.project_dir / "fake-bin"
        fake_bin.mkdir()
        self._write_executable(
            fake_bin / "git",
            """\
            #!/usr/bin/env sh
            if [ "$1" = "status" ]; then
                exit 0
            fi
            exit 99
            """,
        )
        self.fake_bin = fake_bin
        self._write_executable(
            self.project_dir / "generar_newsletter.py",
            """\
            #!/usr/bin/env python3
            import argparse
            import json
            import os
            from pathlib import Path

            parser = argparse.ArgumentParser()
            parser.add_argument("--periodicidad")
            parser.add_argument("--output-dir", required=True)
            parser.add_argument("--metadata-file", required=True)
            args = parser.parse_args()

            output_dir = Path(args.output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            (output_dir / "parcial.tmp").write_text("parcial", encoding="utf-8")
            failure = int(os.environ.get("FAKE_NEWSLETTER_EXIT", "0"))
            if failure:
                raise SystemExit(failure)

            (output_dir / "parcial.tmp").unlink()
            names = [
                "newsletter-2026-07-Q2.md",
                "newsletter-2026-07-Q2.html",
                "index.html",
            ]
            for name in names:
                (output_dir / name).write_text(name, encoding="utf-8")
            metadata = {
                "fecha_generacion": "2026-07-24T20:27:50+02:00",
                "periodo": "Quincena 2 de 07/2026",
                "estado": "PENDIENTE",
                "archivos": names,
                "codigo_salida": 0,
            }
            Path(args.metadata_file).write_text(
                json.dumps(metadata),
                encoding="utf-8",
            )
            """,
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()
        self.assertEqual(self.git_status_before, self._repo_status())

    def _repo_status(self) -> str:
        return subprocess.check_output(
            ["git", "status", "--porcelain", "--untracked-files=normal"],
            cwd=REPO_DIR,
            text=True,
        )

    def _write_executable(self, path: Path, content: str) -> None:
        path.write_text(textwrap.dedent(content), encoding="utf-8")
        path.chmod(path.stat().st_mode | stat.S_IXUSR)

    def _run(self, *, failure: int = 0) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["PATH"] = f"{self.fake_bin}:{env['PATH']}"
        env["FAKE_NEWSLETTER_EXIT"] = str(failure)
        return subprocess.run(
            [str(self.scripts_dir / LAUNCHER.name)],
            cwd=self.project_dir,
            env=env,
            text=True,
            capture_output=True,
            timeout=20,
        )

    def _temporary_dirs(self) -> list[Path]:
        private_dir = self.project_dir / "data" / "private"
        return list(private_dir.glob(".newsletter_pendiente.tmp.*"))

    def test_success_promotes_validated_draft(self) -> None:
        result = self._run()
        pending = self.project_dir / "data" / "private" / "newsletter_pendiente"

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertTrue((pending / "metadata.json").is_file())
        self.assertEqual(
            {
                "index.html",
                "newsletter-2026-07-Q2.html",
                "newsletter-2026-07-Q2.md",
            },
            {path.name for path in (pending / "archivos").iterdir()},
        )
        self.assertEqual([], self._temporary_dirs())

    def test_failure_preserves_exit_and_removes_temporary_state(self) -> None:
        result = self._run(failure=42)
        pending = self.project_dir / "data" / "private" / "newsletter_pendiente"

        self.assertEqual(42, result.returncode, result.stdout + result.stderr)
        self.assertFalse(pending.exists())
        self.assertEqual([], self._temporary_dirs())

    def test_existing_pending_returns_76_without_changes(self) -> None:
        pending = self.project_dir / "data" / "private" / "newsletter_pendiente"
        pending.mkdir(parents=True)
        marker = pending / "metadata.json"
        original = b'{"estado":"PENDIENTE","marca":"intacta"}'
        marker.write_bytes(original)

        result = self._run()

        self.assertEqual(76, result.returncode, result.stdout + result.stderr)
        self.assertEqual(original, marker.read_bytes())
        self.assertEqual([], self._temporary_dirs())


if __name__ == "__main__":
    unittest.main()
