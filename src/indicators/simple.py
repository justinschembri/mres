"""Simplified scripts for applying known multi-hazard indexes to geojsons."""
#stdlib
import pathlib
import os
from typing import Literal
#external

def find_geojson(path:pathlib.Path | None = None) -> pathlib.Path:
    """Walk the current working directory find the exposure.json file."""
    path = path or pathlib.Path(os.getcwd())
    potential_file = list(path.glob("exposure.json")) + list(path.glob("exposure.geojson"))
    if not potential_file:
        raise FileNotFoundError(
                f"Did not find exposure.json/geojson in {path}"
                )
    elif len(potential_file) > 1:
        raise ValueError(
                f"Found indicators as .json and .geojson, in {path} will not " +
                f"proceed to avoid confusion."
                )
    return potential_file[0]

def find_indicators(
        hazard: Literal["heat", "seismic", "wind", "flood"],
        path:pathlib.Path | None = None
        ) -> pathlib.Path:
    """Walk the current working directory find the indicators.csv file."""
    path = path or pathlib.Path(os.getcwd())
    potential_file = list(path.glob(f"{hazard}_indicators.csv"))
    if not potential_file:
        raise FileNotFoundError(
                f"Did not find exposure.json/geojson in {path}"
                )
    elif len(potential_file) > 1:
        raise ValueError(
                f"Found indicators as .json and .csv, in {path} will not " +
                f"proceed to avoid confusion."
                )
    return potential_file[0]

def parse_indicatores(
        hazard: Literal["heat", "seismic", "wind", "flood"],
        path:pathlib.Path | None = None
        ) -> pathlib.Path:
    expected_indicators = {
            "heat": [id, res_1, res_2, res_3, rec_1, e_f],
            "seismic": [id, res_1, res_2, res_3, res_4, rec_1, rec_2, rec_3, n_1, n_2, n_3, n_4, n_5, n_6, n_7, m_1, m_2]
            }
