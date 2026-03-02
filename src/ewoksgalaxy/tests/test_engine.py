import json
import subprocess
import sys
from pathlib import Path


def test_convert_to_gxwf(ewoks_workflow: dict, tmpdir: Path):
    input_path = tmpdir / "workflow.json"
    with open(input_path, "w") as f:
        json.dump(ewoks_workflow, f)

    output_path = tmpdir / "workflow.yaml"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "ewoks",
            "convert",
            str(input_path),
            str(output_path),
            "--dst-format",
            "gxwf",
        ],
        check=True,
    )
    assert output_path.exists()

    subprocess.run(
        [sys.executable, "-m", "gxformat2.lint", str(output_path)],
        check=True,
    )


def test_convert_from_gxwf(iris_workflow_path: Path, tmpdir: Path):
    output_path = tmpdir / "iris.json"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "ewoks",
            "convert",
            str(iris_workflow_path),
            str(output_path),
        ],
        check=True,
    )
    assert output_path.exists()
