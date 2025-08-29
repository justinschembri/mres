"""Simplified scripts for applying known multi-hazard indexes to geojsons."""
# standard library
import pathlib
import os
from typing import Literal, Any
import csv
import json
# external
# internal
from .indicators import (
        FloodResilienceIndicators, 
        HeatResilienceIndicators, 
        ResilienceIndicator, 
        SeismicResilienceIndicators, 
        WindResilienceIndicators
        )

def find_geojson(path: pathlib.Path | None = None) -> pathlib.Path:
    """
    Return `Path` object of the exposure file in the current working directory.

    Args:
        path (pathlib.Path | None): Directory to search. Defaults to None, which
        searches the current working directory.

    Returns:
        pathlib.Path: Path to the found exposure file (`exposure.json` or 
        `exposure.geojson`).

    Raises:
        FileNotFoundError: If no exposure file is found.
        ValueError: If both `.json` and `.geojson` exposure files are found.
    """
    path = path or pathlib.Path(os.getcwd())
    potential_file = list(path.glob("exposure.json")) + list(path.glob("exposure.geojson"))
    if not potential_file:
        raise FileNotFoundError(
            f"Did not find exposure.json/geojson in {path}. " +
            f"Is this the correct directory?"
        )
    elif len(potential_file) > 1:
        raise ValueError(
            f"Found indicators as .json and .geojson in {path}, will not "
            f"proceed to avoid confusion."
        )
    return potential_file[0]

def find_indicators_csv(
        hazard: Literal["heat", "seismic", "wind", "flood"],
        path:pathlib.Path | None = None
        ) -> pathlib.Path:
    """
    Return `Path` object of indicator files in current working directory.

    Args:
        hazard (Literal["heat", "seismic", "wind", "flood"]): Hazard indicator 
        to search for, for example passing `heat` will find 
        `heat_indicators.csv`.
        path (pathlib.Path | None): Direct to search, defaults to None which
        searches through current working directory.

    Returns:
        `Path` object of `{hazard}_indicators.csv` found, None if nothing found.
    """
    path = path or pathlib.Path(os.getcwd())
    potential_file = list(path.glob(f"{hazard}_indicators.csv"))
    if not potential_file:
        raise ValueError(
                f"Did not find indicators.csv"
                )
    elif len(potential_file) > 1:
        raise ValueError(
                f"Found indicators as .json and .csv, in {path} will not " +
                f"proceed to avoid confusion."
                )
    return potential_file[0]

def parse_indicators(
        hazard: Literal["heat", "seismic", "wind", "flood"],
        path:pathlib.Path,
        ) -> list[ResilienceIndicator]:
    """Parse an indicator.csv file and return an array of indicators."""
    expected_indicators =  {
    "heat": ["id", "res_1", "res_2", "res_3", "rec_1", "e_f", "m_1", "m_2"],
    "seismic": ["id", "res_1", "res_2", "res_3", "res_4", "rec_1", "rec_2", "rec_3", "n_1", "n_2", "n_3", "n_4", "n_5", "n_6", "n_7", "m_1", "m_2"],
    "wind": ["id", "res_1", "res_2", "res_3", "res_4", "rec_1", "rec_2", "rec_3", "n_1", "n_2", "n_3", "n_4", "n_5", "n_6", "n_7", "m_1", "m_2"],
    "flood": ["id", "res_1", "res_2", "res_3", "res_4", "res_5", "rec_1", "rec_2", "rec_3", "rec_4", "n_1", "n_2", "n_3", "n_4", "n_5", "n_6", "n_7", "n_8", "n_9", "m_1", "m_2"]
        }
    class_map = {
            "heat":HeatResilienceIndicators,
            "seismic":SeismicResilienceIndicators,
            "wind":WindResilienceIndicators,
            "flood":FloodResilienceIndicators
            }

    with open(path, "r") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"No fields (headers) found in the provided .CSV: {path=}")
        headers = [h.strip() for h in reader.fieldnames if h]
        for expected_indicator in expected_indicators[hazard]:
            if expected_indicator not in headers:
                raise ValueError(f"Missing {expected_indicator=}.")
        result_indicators = []
        for row in reader:
            row = {k.strip(): float(v) if k.strip() != "id" else int(v) for k, v in row.items()}
            indicator = class_map[hazard](**row)
            result_indicators.append(indicator)
    
    return result_indicators

def calculate_rrl(
        indicator_array: list[ResilienceIndicator]
        ) -> dict[int, float]:
    """Iterate through an array of resilience indicators and calculate the RRL."""
    resilience_readiness_levels = {}
    for indicator in indicator_array:
        resilience_readiness_levels[str(indicator.id)] = indicator.calculate_rrl()

    return resilience_readiness_levels

def modify_geojson(
        path: pathlib.Path,
        rrl_type: Literal["heat", "seismic", "flood", "wind"],
        rrls: dict[Any, Any],
        ) -> int:
    """
    Update GeoJSON file at `path`, embedding RRLs into schema.

    Args:
        path (Path): Path to exposure.json file to modify.
        rrl_type (Literal): RRL type to add to json object.
        rrls: Dict object containing buildings and their respective RRLs.

    Returns:
        int: returns the number of modified buildings.
    """
    with open(path, "r") as f:
        geojson = json.load(f)
        if not geojson.get("features"):
            raise ValueError(f"No features found in GEOJSON at {path},")
        
        modified_buildings = 0
        for idx, feature in enumerate(geojson.get("features")):
            feature: dict[str, Any]
            id = feature.get("id")
            rrl = rrls.get(id)
            if not rrl:
                continue
            geojson["features"][idx]["properties"][f"{rrl_type}_rrl"] = rrl
            modified_buildings += 1

    with open(path, "w") as f:
        json.dump(geojson, f)
        return modified_buildings


def simple_rrl_calculator(path: pathlib.Path):
    """Take the available RRL indicator data in a directory and return an augmented GeoJSON File."""
    exposure_file = find_geojson(path) #for now this does nothing.
    indicator_files = []
    for hazard in ("heat", "seismic", "wind", "flood"):
        indicator_file = find_indicators_csv(hazard, path)
        indicators = parse_indicators(hazard, indicator_file)
        rrl = calculate_rrl(indicators)
         
