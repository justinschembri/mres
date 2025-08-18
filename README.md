# Urban Multi-Resilience Index Algorithms

## What is it?

**mres** is a CLI tool for adding multi-hazard resilience indexes to geospatial
datasets.

The calculation of a multi-hazard resilience index is defined by dozens of
indicators. Many of these indicators are calculated by their own individual
methodologies and domain experts. 

At the most basic level, `mres` is a tool for collating the individual
indicators, performing the required normalization and calculating a
building-by-building *multi-hazard resilience index*. In this use case, the
inputs are the indicators and a reference `GeoJSON` which represents and defines
the buildings. The output is a modified `GeoJSON` with the calculated indexes
appended. 

## Installation

## Usage


### Heat Resilience

Heat Resilience is defined as a normalized combination of four resilience
indicators, `I_res1`, `I_res2`, `I_res3`, `I_rec` and finally augmented by an
effeciency factor `ef`. The full definitions of the five components are
available as part of MultiCare's D6.1 deliverable
[here](https://multicare-project.eu/wp-content/uploads/2024/09/D6.1-Framework-and-rating-system-for-resilient-buildings.pdf).


