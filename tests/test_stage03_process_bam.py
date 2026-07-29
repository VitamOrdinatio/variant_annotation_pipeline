# tests/test_stage03_process_bam.py

from __future__ import annotations

from pathlib import Path
from unittest.mock import Mock

from pipeline.stage_03_process_bam import _record_samtools_version


def test_record_samtools_version_accepts_non_utf8_build_metadata(
    tmp_path: Path,
) -> None:
    """
    Stage 03 must record the samtools version when auxiliary build
    metadata contains bytes that are not valid UTF-8.
    """
    samtools = tmp_path / "samtools"
    samtools.write_bytes(
        b"#!/usr/bin/env python3\n"
        b"import sys\n"
        b"sys.stdout.buffer.write("
        b"b'samtools 1.16.1\\n"
        b"Using htslib 1.16\\n"
        b"CFLAGS: -ffile-prefix-map="
        b"\\xabBUILDPATH\\xbb=.\\n')\n"
    )
    samtools.chmod(0o755)

    config = {
        "tools": {
            "samtools": {
                "executable": str(samtools),
            }
        }
    }
    state = {
        "run": {},
        "warnings": [],
    }
    logger = Mock()

    _record_samtools_version(
        config,
        state,
        logger,
    )

    assert state["warnings"] == []
    assert state["run"]["tool_versions"] == {
        "samtools": "samtools 1.16.1",
    }
    logger.info.assert_called_once_with(
        "Recorded samtools version: samtools 1.16.1"
    )
    logger.warning.assert_not_called()


def test_record_samtools_version_warns_when_version_is_unparseable(
    tmp_path: Path,
) -> None:
    samtools = tmp_path / "samtools"
    samtools.write_text(
        "#!/usr/bin/env bash\n"
        'echo "unknown tool output"\n',
        encoding="utf-8",
    )
    samtools.chmod(0o755)

    config = {
        "tools": {
            "samtools": {
                "executable": str(samtools),
            }
        }
    }
    state = {
        "run": {},
        "warnings": [],
    }
    logger = Mock()

    _record_samtools_version(
        config,
        state,
        logger,
    )

    assert "tool_versions" not in state["run"]
    assert len(state["warnings"]) == 1
    assert state["warnings"][0].startswith(
        "Unable to record samtools version:"
    )
    logger.warning.assert_called_once()