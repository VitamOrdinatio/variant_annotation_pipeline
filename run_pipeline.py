"""
CLI entrypoint for variant_annotation_pipeline v1.0.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.config_loader import load_config, validate_config
from src.pipeline_runner import run_pipeline


def initialize_logger(log_path: str, level: str = "INFO"):
    """
    Initialize console + file logger.

    Parameters
    ----------
    log_path : str
        Path to log file.
    level : str
        Logging level.

    Returns
    -------
    logging.Logger
        Configured logger.
    """
    import logging

    logger = logging.getLogger("variant_annotation_pipeline")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.propagate = False
    return logger


def parse_args() -> argparse.Namespace:
    """
    Parse CLI arguments.

    Returns
    -------
    argparse.Namespace
        Parsed CLI namespace.
    """
    parser = argparse.ArgumentParser(
        description="Run variant_annotation_pipeline v1.0"
    )
    parser.add_argument(
        "--config",
        required=True,
        help="Path to config/config.yaml",
    )
    return parser.parse_args()


def bootstrap_log_path(config: dict) -> str:
    """
    Create an early deterministic bootstrap log path before run_id creation.

    Parameters
    ----------
    config : dict
        Parsed config.

    Returns
    -------
    str
        Bootstrap log path.
    """
    base_results_dir = Path(config["output"]["base_results_dir"])
    bootstrap_dir = base_results_dir / "bootstrap_logs"
    bootstrap_dir.mkdir(parents=True, exist_ok=True)
    return str(bootstrap_dir / config["logging"]["log_filename"])


def main() -> int:
    """
    Main CLI entrypoint.

    Returns
    -------
    int
        Process exit code.
    """
    args = parse_args()

    try:
        config = load_config(args.config)
        validate_config(config)

        bootstrap_log = bootstrap_log_path(config)
        logger = initialize_logger(
            log_path=bootstrap_log,
            level=config["logging"]["level"],
        )

        logger.info("Config loaded successfully.")
        logger.info(f"Using config: {args.config}")
        logger.info(f"Execution mode: {config['mode']['execution_mode']}")
        logger.info(f"Sample ID: {config['input']['sample_id']}")
        logger.info(f"SRA accession: {config['input']['sra_accession']}")

        state, run_paths = run_pipeline(
            config=config,
            config_path=args.config,
            logger=logger,
        )

        print("Pipeline execution complete.")
        print(f"Run status: {state['run']['status']}")
        print(f"Run ID: {state['run']['run_id']}")
        print(f"Run directory: {run_paths['run_dir']}")

        return 0 if state["run"]["status"] == "completed" else 1

    except Exception as exc:
        print(f"Pipeline bootstrap failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())