# Urban Multi-Resilience Index Algorithms

## What is it?

`mres` is a CLI tool which merges Resilience Readiness Indices with existing
`GeoJSON` based exposure models. The calculation of a multi-hazard resilience
index is defined by dozens of indicators, and many of these indicators are
calculated by their own individual methodologies and domain experts. This useful
CLI tool allows domain experts to calculate individual indicators based on their
expertise and easily merge them with exposure models in the `GeoJSON` model
format.

## Example Usage

At the bare minimum `mres` requires two files:

1. an exposure model in the [`GeoJSON`](https://geojson.org/) format; for more
   information of the `GeoJSON` format refer [here](#the-geojson-exposure-file).

2. a set of resilience indicators for either heat, seismic, flood or wind
   hazard; for more information on the resilience indicators, refer [here]()2.
   an set of resilience indicators for either heat, seismic, flood or wind
   hazard; for more information on the resilience indicators, refer
   [here](#the-resilience-indicators).

### `mres template`

Both the exposure model and the resilience indicators must refer to buildings by
the same references. The first step is to create the required resilience
indicators template (using the same building IDs) with the `mres` CLI. For
example, the following command will generate a template CSV based on the
contents of the exposure model in the current working directory:

```bash
$ mres template heat
# Output
Generated heat_resilience_indicators.csv at ~/Desktop/MyResilienceProject for
5 buildings.
```

If the five buildings in the exposure model had IDs: `3f9a7c2`, `b81d0e9`,
`f4276ab`, `c95f30d` and `7e12a6f` then the output
heat_indicators.csv would look like:

```csv
# heat_indicators.csv
id,res_1,res_2,res_3,rec_1,e_f,m_1,m_2
3f9a7c2,999,999,999,999,999,999,999
b81d0e9,999,999,999,999,999,999,999
f4276ab,999,999,999,999,999,999,999
c95f30d,999,999,999,999,999,999,999
7e12a6f,999,999,999,999,999,999,999
```

All headers excluding `id` are the various resilience indicators associated with
heat resilience. They are derived from the MultiCare deliverable
[D6.1](https://multicare-project.eu/wp-content/uploads/2024/09/D6.1-Framework-and-rating-system-for-resilient-buildings.pdf).
Furthermore, the `999` values are special placeholders to be replaced by the
domain experts. 

An example of a completed indicator set might look like:

```csv
id,res_1,res_2,res_3,rec_1,e_f,m_1,m_2
3f9a7c2,0.42,0.81,0.13,0.77,0.58,0.92,0.36
b81d0e9,0.67,0.14,0.56,0.25,0.12,0.92,0.36
f4276ab,0.11,0.49,0.33,0.91,0.87,0.92,0.36
c95f30d,0.88,0.22,0.71,0.44,0.34,0.92,0.36
7e12a6f,0.34,0.95,0.09,0.68,0.63,0.92,0.36
```

### `mres merge`

To merge the exposure model with the resilience indicators simply run the
command:

```bash
$ mres merge  
# Output
Added heat RRLs to 1 buildings.
```

The application will perform a number of validation and calculation steps to
combine the invidual indicators into a single heat RRL. The validation steps are
many and more detailed information can be found [here](#validation-procedures).

Navigating to the original `GeoJSON` one finds the calculated heat_rrl embedded
in the `properties` field of the building feature as follows:

```json
    {
    "type": "FeatureCollection",
    "features": [
        {
        "type": "Feature",
        "id": "3f9a7c2",
        "geometry": {
            "type": "Polygon",
            "coordinates": [
            [
                [33.4262, 49.1028],
                [33.4261, 49.1029],
                [33.4265, 49.1030],
                [33.4262, 49.1028]
            ]
            ]
        },
        "properties": {
            "name": "Example Building",
            "numStoreys": 3,
            "storeyHeight": 5,
            "footprintArea": 240.5,
            "...": "...",
            "heat_rrl": 0.56,
       }
        },
        ...
    ]
    }
```

### archetype-functions

Sometimes it is possible to use information embedded in the exposure model to
calculate resilience indicators. By way of example, an exposure model might
define building height, construction year and other information; this data could
be used to make estimates of some of the seismic resilience indices. `mres`
refers to the any functinos which derive resilience indices from an exposure
model as `ArchetypeFunctions`. In the present version of `mres` only the
abstract base class (ABC) and a test function has been defined, and more detail
may be found the [Archetype Functions](#building-archetype-functions) section.

Running the function `mres archetype-functions apply` cycles through the available
`ArchetypeFunctions`, extracts the available information on a building by
building basis. If the exposure model contains the required information to
calculate any resilience indicator, the existing indicator CSVs will be
modified, and extensive logs provided:

```bash
# before heat_resilience.csv:
id,res_1,res_2,res_3,rec_1,e_f,m_1,m_2
3f9a7c2,999,999,999,999,999,999,999
b81d0e9,999,999,999,999,999,999,999
f4276ab,999,999,999,999,999,999,999
c95f30d,999,999,999,999,999,999,999
7e12a6f,999,999,999,999,999,999,999
$ mres archetype-functions
# Output
Building 3f9a7c2: Calculated e_f from ("year_of_construction", "cooling_system")
Building b81d0e9: No resilience indicators estimated [insufficient data]
...
```

## Building Archetype Functions

In `mres`, an Archetype is a value embedded in the `properties` field of the
exposure `geojson`. Archetypes are completely user defined, it is possible to
define archetypes for buildings in any region on a case-by-base basis. The
`ArchetypeFunction` itself is any function which applies to a specific building
archetype and can, given known building features, calculate some resilience
indicator. `ArchetypeFunction`s will be built up over the course of the project
and are located at 'src/mres/archetype_functions.py'. The available archetypes
are an `enum`s at the beggining of the file:

```python
class Archetype(Enum):
    """Supported archetypes."""
    _TEST_CLASS = "_test_class"
    RESIDENTIAL = "residential"
    COMMERICIAL = "commercial"
    ...
```

Even though the they are called archetype _functions_, `ArchetypeFunctions` are
actually built as abstract base classes (`ABC`) with the following attributes:

    1. indicators_csv (Path): Path to the indicators_csv, passed as an argument to the
       initilizer,
    2. archetype (Archetype): Archetype this function is applicable too.
    3. hazard (HazardType): Hazard this function is applicable too.
    4. indicator (str): Resilience indicator this function is applicable too.
    5. relevant_properties (list[str]): a list of relevant properties to extract
       from the exposure model required for the calculation of the resilience
       indicator.
    6. results (dict[str, float]): Defaults to a defaultdict(999). The results
       of the resilience indicator calculation.

The `ABC` has to implemented methods for validating and modifying the indicators
csv and one undefined (abstract) method `compute_indicator`. This method is the
main arithmetic or methodology used for calculating the indicator is implemented
here. 

### Example Implementation

The main contribution of researchers will be defining archetype functions. To
better illustrate how these are added to the project, a mock case is presented
below. It begins through the definition of a new archetype:
`acerra_residential`. This new type must be added to the `Archetype` enum at the
top of the file:

```python
class Archetype(Enum):
    """Supported archetypes."""
    # note that the test class should remain.
    _TEST_CLASS = "_test_class"
    ACERRA_RESIDENTIAL = "acerra_residential"
    ...
```

Next, a concrete class is implemented, beginning with the initiziliation
function:

```python
class AcerraResidentialHeat(ArchetypeFunction):
    """Archetype function for residential buildings in Acerra."""

    def __init__(self, indicators_csv: Path):
        super().__init__(indicators_csv)
        self.archetype = Archetype("acerra_residential")
        self.hazard = HazardType("heat")
        self.indicator = "e_f"
        self.relevant_properties = ["has_cooling", "year_of_construction"]
```

The intilization signature shows that the resilience indicator that this
function calculates is for the heat hazard and specifically the effeciency
factor `e_f`. Furthermore, the required properties for calculation are
`has_cooling` and `year_of_construction`. If any of these properties are
missing, even if the archetype is known, the function will not be able to
complete its calculation.

Now, the `compute_indicator` function can be implemented:

```python
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
```

This particular implementation is fairly trivial: where an effeciency factor is
associated with the year of construction of the building and the results being
stored in the `results` attribute of the class. 

Lastly, the new function is added to the mapping which takes on this particular
format:

```python
ARCHETYPE_FUNCTIONS = {
        # Archetype.VALUE : List[ArchetypeFunction]
        Archetype.ACERRA_RESIDENTIAL:[AcerraResidentialHeat,],
        } 
```

Notice how the mapping takes values which are of the type
`list[ArchetypeFunction]`, as there may be many functions mapped to a single
archetype.

The exposure model should duly contain a properties field making reference to
the archetype (if known), for example:

```json
"properties": {
    "archetype": "acerra_residential",
    <other features>,
}
```

The parser that runs with the command `mres archetype-functions apply` will now
know that any entity in the exposure model that has a given archetype
"acerra_residential" is associated with some specific archetypical functions.
The exposure model is parsed, the functions are invoked and the `indicators_csv`
for the respective hazards are thus modified.

## Requirements, Installation and Setup

`mres` is built on Python and thus the requirements are:

1. A Python installation,
2. `git`,
3. (Optional) A community package manager such as `poetry`, or `uv`.

Clone the repository using:

```bash
git clone https://github.com/justinschembri/st-utils.git mres
```

The application uses a modern `pyproject.toml` specification and it is
recommended that a virtual environment (`venv`) is used to run the application:

**pip**
```bash
# from the .../mres directory
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

**uv**
```bash
# from the .../mres directory
uv venv .venv
uv sync
source .venv/bin/activate
```

For `mres` to be available as a command in your shell session, don't forget to
ensure that the virtual environment is installed.

## Reference Usage

## The Resilience Indicators

## The GeoJSON Exposure File

## Validation Procedures


