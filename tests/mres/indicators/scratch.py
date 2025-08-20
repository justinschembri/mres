from pathlib import Path
from mres.indicators.simple import (
        find_indicators_csv,
        parse_indicators,
        calculate_rrl
        )
from mres.config import TEST_DIR

data_path = TEST_DIR / "mres" / "data"

if __name__ == "__main__":
    for hazard in ("heat", "seismic", "flood", "wind"):
        csv_file = find_indicators_csv(
                hazard, data_path
                )
        indicators = parse_indicators(hazard, csv_file)
        rrls = calculate_rrl(indicators)
        print(rrls)

