\
from __future__ import annotations

from scripts.validation.preflight_sys76_err10619300 import (
    _check_fastq,
    _launch_command,
)


def test_missing_fastq_is_reported(tmp_path) -> None:
    record = _check_fastq(str(tmp_path / "missing.fastq.gz"))
    assert record["exists"] is False
    assert record["size_bytes"] is None


def test_existing_fastq_is_reported(tmp_path) -> None:
    path = tmp_path / "reads.fastq.gz"
    path.write_bytes(b"fixture")
    record = _check_fastq(str(path))
    assert record["exists"] is True
    assert record["size_bytes"] == 7


def test_launch_command_is_tmux_detached() -> None:
    command = _launch_command(
        "config/execution_provenance/config.sys76.err10619300.execution_provenance.yaml"
    )
    assert command.startswith("tmux new-session -d")
    assert "vap_err10619300_sys76" in command
    assert "run_pipeline.py --config" in command
    assert "TMPDIR=/mnt/storage/vap_tmp/ERR10619300" in command
