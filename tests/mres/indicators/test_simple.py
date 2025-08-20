"""Test simple.py."""

# standard
# external
import pytest
# internal
from mres.indicators.simple import (
        find_indicators_csv,
        parse_indicators,
        calculate_rrl,
        ResilienceIndicator
        )
from mres.config import TEST_DIR


# Pytest fixtures

@pytest.fixture
def test_datapath():
    yield TEST_DIR / "mres" / "data"

@pytest.fixture
def rrl_mock():
    """Known values for calculated RRLs."""
    yield {
            "heat" : ...,
            "seismic" : ...,
            "flood" : ..., 
            "wind" : ...
            }

def test_find_indicators_csv(test_datapath) -> None:
    for hazard in ("heat", "seismic", "flood", "wind"):
        csv_file = find_indicators_csv(hazard, test_datapath)
        assert csv_file == TEST_DIR / "mres" / "data" / f"{hazard}_indicators.csv"
    
def test_parse_indicators(test_datapath) -> None:
    for hazard in ("heat", "seismic", "flood", "wind"):
        csv_file = find_indicators_csv(hazard, test_datapath)
        indicators = parse_indicators(hazard, csv_file)
        assert isinstance(indicators, list)
        assert len(indicators) == 100
        assert isinstance(indicators[0], ResilienceIndicator)

def test_calculate_rrl(test_datapath) -> None:
    for hazard in ("heat", "seismic", "flood", "wind"):
        csv_file = find_indicators_csv(hazard, test_datapath)
        indicators = parse_indicators(hazard, csv_file)
        rrls = calculate_rrl(indicators)

