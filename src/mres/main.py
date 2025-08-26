"""MRES main script and CLI functionality."""

# standard
from pathlib import Path
from typing import Literal, Union, List
# external
import typer
# internal
from mres.indicators.simple import (
        find_geojson,
        find_indicators_csv,
        parse_indicators,
        calculate_rrl,
        modify_geojson
    )
# Typer setup
cli = typer.Typer()

@cli.command()
def merge(
        path: Path | None = typer.Option(
            None,
            "--path",
            "-p",
            help="Path to scan for <hazard>_indicators.csv and exposure.json."
            )
        ) -> None:

    for hazard in ("heat", "seismic", "flood", "wind"):
        indicators_csv = find_indicators_csv(hazard, path)
        exposure_csv = find_geojson(path)
        if not indicators_csv:
            typer.echo(f"No {hazard} indicators CSV found at {path}.")
            continue
        indicators = parse_indicators(hazard, indicators_csv)
        rrls = calculate_rrl(indicators)
        total_modified = modify_geojson(
                exposure_csv, 
                hazard, 
                rrls,
                )
        typer.echo(f"Added {hazard} RRLs to {total_modified} buildings.")

    return None

@cli.command()
def template(
        path: Path | None = typer.Option(None, "--path", "-p"),
        hazard: List[str] | None = typer.Option(
                None,
                "--hazard",
                "-h",
                help="Hazards to create templates for."
            )
        ):
    ...

