# Multi-Hazard Resilience Integration into the SDSS

As ancillary support to the SDSS, the Command Line Interface (CLI, Figure _)
tool **`mres`** has been developed. `mres` provides functionality for
integrating the remaining natural hazard Resilience Readiness Levels (RRLs)
described in Deliverable 6.1, namely:

1. seismic 
2. flood 
3. wind 

The derivation of RRLs requires the calculation of several internal indicators.
For example, the seismic RRL incorporates four indicators related to building
response, three indicators related to the recovery period, and their respective
weightings. Each internal indicator used to compute the overall RRL depends on a
combination of external software tools, expert judgment, and case-specific
analysis. `mres` supports this process in two ways.  

![Figure _](image.MresHelp.png)

In the first case, it is assumed that experts compute the relevant indicators
for buildings in the region of interest outside the SDSS platform and provide
them as structured data. `mres` can ingest this structured data and update
common geospatial file formats—currently supporting
[`geojson`](https://geojson.org/). Figure _ illustrates the data flow for this
functionality, while Section _ describes it.

![Figure _](image.MresMerge.jpg)

In the second, more advanced case, users may define functions that draw on data
from the underlying exposure model in the SDSS to compute some or all indicators
and, optionally, the RRLs themselves. For example, building height and
construction typology data from the exposure model could be combined with
vulnerability curves to estimate probable losses from a given earthquake event.
Figure _ illustrates the data flow for this methodology, while Section _
describes it.  

![Figure _](image.MresApply.jpg)

`mres` is an open source tool and is available
[here](https://github.com/justinschembri/mres).

## Requirements, Installation and Setup

`mres` is built on Python and thus the requirements are:

1. A Python installation,
2. The Version Control System (VCS) `git`,
3. (Optional) An open-source package manager such as `poetry`, or `uv`.

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
ensure that the virtual environment is activate. Alternatively if using `uv`,
the command `uv run mres`.

## Templating and Merging Functionality

When `mres` is used to merge externally computed indicators into an exposure
model for ingestion with the rest of the SDSS, the following is required:

1. An exposure model in the [`geojson`](https://geojson.org/) format.  For more
   information.  

2. Resilience indicators for one or more of the hazards (heat, seismic, flood,
   or wind). 

## The `geojson` Exposure Model

The exposure model (1) represents the geospatial data describing the region of
interest. Multicare has collected baseline urban data at the demonstrator sites
in earlier deliverables.  

Exposure modeling includes more than building geometry; the exact content
depends on the data collection strategy or available information. Both the SDSS
and `mres` can ingest the standard `geojson` format, which is lightweight and
human-readable. GeoJSON includes a `properties` field and allows **any**
additional key-value pairs.  

For SDSS, the GeoJSON **must** be of type `FeatureCollection` and should include
an `id` (string or numeric) for each feature. While `id` is optional in the
schema, it is essential for `mres`.  

An example GeoJSON is shown below. Figure _ illustrates the schema visually.  

![Figure _](image.GeoJsonExplanation.jpg)  

## The Resilience Indicators

Each of the four hazard categories—**Energy, Seismic, Flood, and Wind**—has a
set of indicators. As described in deliverable D6.1, these indicators are
normalized, weighted, and combined to form four Resilience Readiness Levels
(RRLs). 

Calculating an RRL requires all indicators to be specified. Users can provide
these in a CSV file, which must follow a specific format.

### Generating Indicator Templates with `mres template`

As both files must refer to the same set of buildings using consistent
identifiers, it is particularly useful to template the data-structure from
before hand, which is a feature `mres` performs.

The first step is to generate a resilience indicator template that aligns with
the buildings defined in the exposure model. The `mres` CLI provides a
`template` command to automate this process. For example:

```bash
$ mres template heat
# Output
Generated heat_resilience_indicators.csv at ~/Desktop/MyResilienceProject for
5 buildings.
```

If the exposure model contains five buildings with IDs `3f9a7c2`, `b81d0e9`,
`f4276ab`, `c95f30d`, and `7e12a6f`, the resulting template file
heat_resilience_indicators.csv will appear as follows:

```csv
# heat_indicators.csv
id,res_1,res_2,res_3,rec_1,e_f,m_1,m_2
3f9a7c2,999,999,999,999,999,999,999
b81d0e9,999,999,999,999,999,999,999
f4276ab,999,999,999,999,999,999,999
c95f30d,999,999,999,999,999,999,999
7e12a6f,999,999,999,999,999,999,999
```

All headers (excluding id) correspond to the resilience indicators associated
with heat resilience. The placeholder value 999 indicates that the entry should
be completed by domain experts. An example of a populated file is shown below:

```csv
id,res_1,res_2,res_3,rec_1,e_f,m_1,m_2
3f9a7c2,0.42,0.81,0.13,0.77,0.58,0.92,0.36
b81d0e9,0.67,0.14,0.56,0.25,0.12,0.92,0.36
f4276ab,0.11,0.49,0.33,0.91,0.87,0.92,0.36
c95f30d,0.88,0.22,0.71,0.44,0.34,0.92,0.36
7e12a6f,0.34,0.95,0.09,0.68,0.63,0.92,0.36
```

### Merging Indicators with `mres merge`

Once the exposure model and resilience indicators have been prepared, the next
step is to merge them into a single dataset. This is achieved using the merge
command:

```bash
$ mres merge
# Output
Added heat RRLs to 1 buildings.
```

During this step, the application performs a series of validation and
calculation routines to combine the individual indicators into a single
Resilience Readiness Level (RRL). A detailed description of the validation
procedures is provided in Validation Procedures.

The resulting RRL values are embedded directly into the building features of the
original `geojson` file. For example:

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
        "heat_rrl": 0.56 
      }
    },
    ...
  ]
}
```

Here, the calculated `heat_rrl` is added to the properties of the relevant
building feature, making the resilience assessment directly accessible within
the geospatial dataset and consumable by the SDSS.

## Deriving Indicators from Exposure Models

In certain cases, information embedded within the exposure model may be used
directly to calculate resilience indicators. For example, building height, year
of construction, and other attributes can be exploited to estimate selected
seismic resilience indices.  

In `mres`, functions that derive resilience indicators from exposure model
attributes are referred to as **Archetype Functions**. These provide a
systematic way to translate building properties into indicator values.  

In the current version of `mres`, only the abstract base class (ABC) and a test
function are provided.

### Applying Archetype Functions

The command `mres apply` iterates through the available `ArchetypeFunctions` and
evaluates each building on a case-by-case basis. Where sufficient property data
is present, the relevant indicators are computed and the existing indicator CSVs
are updated.  

For example:

```bash
# Before: heat_resilience.csv
id,res_1,res_2,res_3,rec_1,e_f,m_1,m_2
3f9a7c2,999,999,999,999,999,999,999
b81d0e9,999,999,999,999,999,999,999
f4276ab,999,999,999,999,999,999,999
c95f30d,999,999,999,999,999,999,999
7e12a6f,999,999,999,999,999,999,999

$ mres apply
# Output
Building 3f9a7c2: Calculated e_f from ("year_of_construction", "cooling_system")
Building b81d0e9: No resilience indicators estimated [insufficient data]
...
```

As shown, calculated values replace the 999 placeholders when sufficient data is
present, while missing data is explicitly flagged in the logs.

### Building Archetype Functions

An archetype in mres refers to a value embedded in the properties field of a
building feature in the exposure `geojson`. Archetypes are user-defined and can
be tailored to specific regions, construction typologies, or case-study
requirements.

An Archetype Function is a function associated with a particular archetype and
hazard type. It extracts relevant properties from the exposure model and
computes one or more resilience indicators. Archetype Functions will be
progressively developed throughout the project and are located in `src/mres/archetype_functions.py`

The available archetypes are defined (and may be extended) in the Archetype
enumeration:

```python
# example only:
class Archetype(Enum):
    """Supported archetypes."""
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    ...
```

### Structure of an Archetype Function

Despite their name, Archetype Functions are implemented as abstract base classes
(`ABC`). Each subclass must define a specific computation for a resilience
indicator. The ABC provides the following key attributes:

- indicators_csv (Path): Path to the indicator file to be updated.

- archetype (Archetype): The archetype to which the function applies.

- hazard (HazardType): The hazard type (e.g., heat, seismic, flood, wind).

- indicator (str): The resilience indicator to be computed.

- relevant_properties (list[str]): Exposure model attributes required for the calculation.

- results (dict[str, float]): A dictionary mapping building IDs to results, defaulting to 999 where calculation is not possible.

The base class provides validation and CSV modification methods. A single
abstract method, compute_indicator, must be implemented to define the actual
calculation logic.

### Example Implementation

The main contribution of researchers will be the development of new Archetype
Functions. As an illustration, consider a mock case for residential buildings in
Acerra.

First, a new archetype must be defined in the Archetype enum:

```python
class Archetype(Enum):
    """Supported archetypes."""
    # note that the test class should remain.
    _TEST_CLASS = "_test_class"
    ACERRA_RESIDENTIAL = "acerra_residential"
    ...
```

Next, a concrete class is created, inheriting from the base `ArchetypeFunction`:

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

This initialization specifies that the function applies to the
`acerra_residential archetype`, relates to the heat hazard, and computes the
efficiency factor e_f. The calculation depends on the has_cooling and
year_of_construction properties.

The compute_indicator method defines the calculation logic:

```python
def compute_indicator(self, building: dict):
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

In this simplified example, the efficiency factor is determined by the
construction year and cooling system status. Results are stored in the results
dictionary.

Finally, the new function must be registered in the function mapping:

```python
ARCHETYPE_FUNCTIONS = {
    # Archetype.VALUE : List[ArchetypeFunction]
    Archetype.ACERRA_RESIDENTIAL: [AcerraResidentialHeat],
}
```

### Linking Archetypes to the Exposure Model

To enable function execution, the exposure model must include an archetype
property for each building. For example:

```json
"properties": {
    "archetype": "acerra_residential",
    "...": "..."
}
```

When `mres apply` is executed, the parser identifies the archetype of each
building, invokes the relevant functions, and updates the indicator CSVs
accordingly.

This process ensures that exposure data can be systematically transformed into
resilience indicators wherever sufficient information is available.

## Look-ahead and Future Work

`mres` is the first in a series of links between MultiCare deliverables and the
SDSS described in this document. In its current stage, it allows the SDSS to
consume and visualize RRLs not associated with energy. The IES engine
contributes substantially to energy-related indicators and RRLs, enabling native
computation. Many remaining indicators still rely on external tools and
methodologies.  

Future revisions of `mres` will aim to:

- Develop more abstract **ArchetypeFunctions**, potentially as individual
  modules that can integrate with other open-source software.  
- Expand the CLI into a **web service**, aligned with the concept of a CDE.  
- Integrate with recently published MultiCare WS6 deliverables.
