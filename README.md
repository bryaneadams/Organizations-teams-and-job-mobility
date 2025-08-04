# Organizations-teams-and-job-mobility
This repository contains code to support [Organizations, teams, and job mobility: A social microdynamics approach inspired by a large US organization](https://arxiv.org/abs/2503.24117). Please contact the [corresponding author](https://arxiv.org/show-email/9c1ecd64/2503.24117) for more details.

## Example Data

Example data is found in [example_data.py](example_data.py) and is a python dictionary of Pandas DataFrames. This data is used to show examples of scenarios you encounter when building teams based off empirical data. The same example data is used to test our algorithms in [algo_tests.py](algo_tests.py). In this document we provide our python testing ([Coverage tests](#coverage-tests)) framework with results of code coverage. The test are designed to ensure we are handling the situations we encountered in our data; however, there may be different situations based on your own organization data.

## Calculations

Code used to calculate statistics is found in [calculations](calculations/), with instructions for use found in the [calculations/README.md](calculations/README.md). These calculations take specific data structures and will need to be adjusted based on your organization and data. Please contact the [corresponding author](https://arxiv.org/show-email/9c1ecd64/2503.24117) for more details.


## Coverage tests

To ensure proper functionality we ran a series of unit tests. 

### Current results

Here are the coverage results

```
---------- coverage: platform darwin, python 3.12.3-final-0 ----------
Name                   Stmts   Miss  Cover   Missing
----------------------------------------------------
utils/build_teams.py     168      8    95%   25, 248, 395, 430-436
utils/helpers.py          COMPLETE COVERAGE
----------------------------------------------------

Lines missed `utils/build_teams.py`:
1.  `25` - only needed if there is a uid duplicate, which does not happen
2.  `430-436` - only needed if there is a uid duplicate, which does not happen
3.  `248`, `395` - no longer in use