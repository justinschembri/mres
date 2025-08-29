"""Functions for deriving Resilience Indicators from Archetypes."""

# standard library
from abc import ABC, abstractmethod
from enum import Enum
from typing import List
from pathlib import Path
import csv
from collections import defaultdict
import json

from mres.indicators.simple import find_geojson, find_indicators_csv
# external libraries
# internal imports
from .indicators.indicators import HazardType

class Archetype(Enum):
    """Supported archetypes."""
    _TEST_CLASS = "_test_class"
    RESIDENTIAL = "residential"
    COMMERICIAL = "commercial"
    ...

class ArchetypeFunction(ABC):
    """ABC which calculates an Archetypes' Resilience Indicator."""

    def __init__(self, indicators_csv: Path):
        self.indicators_csv = indicators_csv
        self.archetype: Archetype
        self.hazard: HazardType
        self.indicator: str
        self.relevant_properties: List[str] = [] 
        self.results: dict[str, float] = defaultdict(lambda:999)

    def _validate(self, building_entity:dict) -> bool:
        if not self.relevant_properties:
            return True
        else:
            for i in self.relevant_properties:
                if not building_entity.get(i):
                    return False

        return True

    def modify_csv(self) -> None:
        with open(self.indicators_csv, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            fieldnames = reader.fieldnames
            if not fieldnames:
                raise ValueError(f"No headers in this file.")
            for row in rows:
                row[self.indicator] = self.results[row["id"]]
        
        with open(self.indicators_csv, "w") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    @abstractmethod
    def compute_indicator(self, building:dict):
        pass

class TestFunction(ArchetypeFunction):
    """Use exclusively for testing."""

    def __init__(self, indicators_csv: Path):
        super().__init__(indicators_csv)
        self.archetype = Archetype("_test_class")
        self.hazard = HazardType("heat")
        self.indicator = "e_f"
        self.relevant_properties = ["has_cooling", "year_of_construction"]

    def compute_indicator(self, building:dict):
        id = building["id"]
        if not self._validate(building):
            self.results[id] = 999
            return None
        if building["has_cooling"] == False:
            self.results[id] = 1
        elif (1960 < int(building["year_of_construction"]) <= 1970):
            self.results[id] = 0.1
        elif (1970 < int(building["year_of_construction"]) <= 1980):
            self.results[id] = 0.2
        elif (1980 < int(building["year_of_construction"]) <= 1990):
            self.results[id] = 0.3
        elif (1990 < int(building["year_of_construction"]) <= 2000):
            self.results[id] = 0.4
        elif (2000 < int(building["year_of_construction"]) <= 2010):
            self.results[id] = 0.5
        elif (2010 < int(building["year_of_construction"]) <= 2020):
            self.results[id] = 0.6
        else:
            self.results[id] = 0.7
        

def apply_archetype_functions(
        hazard: str,
        path: Path | None
        ) -> list[ArchetypeFunction]:

    indicators_file = find_indicators_csv(hazard, path) #type: ignore
    exposure_file = find_geojson(path)
    results: list[ArchetypeFunction] = []

    with open(exposure_file, "r") as f:
        for feature in json.load(f).get("features"):
            id = feature.get("id")
            feature_properties = feature.get("properties")
            archetype = feature_properties.get("archetype")
            try:
                archetype_enum = Archetype(archetype)
                archetype_functions = ARCHETYPE_FUNCTIONS[archetype_enum]
            except ValueError or KeyError:
                print(f"No archetype funciton available for {archetype}.")
                continue
            for archetype_function in archetype_functions:
                func = archetype_function(indicators_file)
                # check that the relevant properties are there for arch.
                for relevant_property in func.relevant_properties:
                    if not feature_properties.get(relevant_property):
                        print(
                                f"Archetype function exists for {archetype} but" +
                                f"building instance {id} is missing " + 
                                f"{relevant_property}"
                            )
                func.compute_indicator(feature)
                results.append(func)

        return results


ARCHETYPE_FUNCTIONS = {
        # Archetype.VALUE : List[ArchetypeFunction]
        Archetype._TEST_CLASS:[TestFunction,],
        }
