from __future__ import annotations

import shutil
import tempfile
import venv
from pathlib import Path


class WindowsFriendlyEnvBuilder(venv.EnvBuilder):
    def setup_scripts(self, context: object) -> None:
        source = Path(venv.__file__).parent / "scripts"

        def ignore_powershell_scripts(
            directory: str, names: list[str]
        ) -> set[str]:
            return {name for name in names if name.lower().endswith(".ps1")}

        with tempfile.TemporaryDirectory() as temp_dir:
            shutil.copytree(
                source,
                temp_dir,
                dirs_exist_ok=True,
                ignore=ignore_powershell_scripts,
            )
            self.install_scripts(context, temp_dir)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        raise SystemExit("Usage: create_venv.py <environment-directory>")

    WindowsFriendlyEnvBuilder(with_pip=True).create(sys.argv[1])