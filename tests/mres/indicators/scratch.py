from pathlib import Path
from mres.indicators.simple import (
        find_indicators_csv,
        parse_indicators,
        calculate_rrl,
        modify_geojson
        )
from mres.config import TEST_DIR

data_path = TEST_DIR / "mres" / "data"
exposure_path = data_path / "exposure.json"

if __name__ == "__main__":
    for hazard in ("heat", "seismic", "flood", "wind"):
        csv_file = find_indicators_csv(
                hazard, data_path
                )
        indicators = parse_indicators(hazard, csv_file)
        rrls = calculate_rrl(indicators)
        geojson = modify_geojson(exposure_path, hazard, rrls)

