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
            "seismic_rrl": 0.09,
            "flood_rrl": 0.45,
            "wind_rrl": 0.08
        }
        },
        ...
    ]
    }
```

## Archetype Usage

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


