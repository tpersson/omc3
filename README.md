# <img src="https://twiki.cern.ch/twiki/pub/BEABP/Logos/OMC_logo.png" height="28"> 3
[![Travis (.com)](https://img.shields.io/travis/com/pylhc/omc3.svg?style=popout)](https://travis-ci.com/pylhc/omc3/)
[![Code Climate coverage](https://img.shields.io/codeclimate/coverage/pylhc/omc3.svg?style=popout)](https://codeclimate.com/github/pylhc/omc3)
[![Code Climate maintainability (percentage)](https://img.shields.io/codeclimate/maintainability-percentage/pylhc/omc3.svg?style=popout)](https://codeclimate.com/github/pylhc/omc3)
[![GitHub last commit](https://img.shields.io/github/last-commit/pylhc/omc3.svg?style=popout)](https://github.com/pylhc/omc3/)
[![GitHub release](https://img.shields.io/github/release/pylhc/omc3.svg?style=popout)](https://github.com/pylhc/omc3/)

This is the python-tool package of the optics measurements and corrections group (OMC).

If you are not part of that group, you will most likely have no use for the codes provided here, unless you have a 9km wide accelerator at home.
Feel free to use them anyway, if you wish!

## Documentation

- Autogenerated docs via `Sphinx` can be found on <https://pylhc.github.io/omc3/>.
- General documentation of the OMC-Teams software on <https://twiki.cern.ch/twiki/bin/view/BEABP/OMC>

## Getting Started

### Prerequisites

The codes use a multitude of packages as can be found in the [`setup.py`](setup.py) file.

Important ones are: `numpy`, `pandas` and `scipy` as well as our `tfs-pandas`, `sdds` and `generic_parser`.

### Installing

To use the codes, a local copy should be obtained via `git clone`,  which then has to be either installed using
`pip install -e /path/to/omc3` or can be used temporarily by appending the path to `PYTHONPATH`.

Alternatively, the previous two steps can be combined with `pip install git+https://github.com/pylhc/omc3.git`.

After installing, codes can be run with either `python -m omc3.SCRIPT --FLAG ARGUMENT`.
or calling path to the `.py` file directly.

## Description

This is the new repository ([old one](https://github.com/pylhc/Beta-Beat.src)) of the codes, rewritten for python 3.6+.  


## Functionality

#### Main Scripts
 to be executed lie in [`/omc3`](https://github.com/pylhc/omc3/tree/master/omc3) directory. These include
- `hole_in_one.py` to perform frequency analysis on turn by turn BPM data and infer optics and more for a given accelerator
- `madx_wrapper.py` to start a MADX with a file or string as input
- `model_creator.py` to provide optics models required for optics analysis
- `run_kmod.py` to analyse data from K-modulation and return measured optics functions
- `tbt_converter.py` to convert different turn by turn datatypes to sdds and add noise 
- `amplitude_detuning_analysis.py` to perform amp. det. analysis on optics data with tune correction


#### Plotting Scripts
 can be found in [`/omc3/plotting`](https://github.com/pylhc/omc3/tree/master/omc3/plotting)
- `plot_spectrum.py` to generate plots from files generated by frequency analysis
- `plot_bbq.py` to generate plots from files generated by frequency analysis
- `plot_amplitude_detuning.py` to generate plots from files generated by frequency analysis


#### Other Scripts
are in [`/omc3/scripts`](https://github.com/pylhc/omc3/tree/master/omc3/scripts)
- `update_nattune_in_linfile.py` to update the natural tune columns in the lin files by finding the highest
peak in the spectrum in a given interval 

#### Examples
can be found in the [`tests`](https://github.com/pylhc/omc3/tree/master/tests) files.

### Changelog

#### 2020-03-04

- Added:
   - lin-file natural tune updater

#### 2020-02-24

- Added:
   - amplitude detuning analysis
   - amplitude detuning and bbq plotting
   - time tools
   - plotting helpers
- Distinction between `BasicTests` and `Extended Tests`

#### Before

- Updated and moved main functionalities from python 2.7
    - Madx wrapper
    - Frequency Analysis of turn by turn
    - Optics measurement analysis scripts
    - Accelerator class and Model Creator
    - K-mod
    - Spectrum Plotting
    - Turn-by-Turn Converter

- `setup.py` and packaging functionality 
- Automated CI
    - Multiple versions of python
    - Accuracy tests
    - Unit tests
    - Release automation

### Development in progress

- Regression tests
- Responsematrix calculation
- Global corrections

## Quality checks

Issues and introduction of new features should take place in branches. After completion, a pull request should be created and merging into the master branch 
is possible after positive review of a reviewer. More details can be found [here](https://twiki.cern.ch/twiki/bin/view/BEABP/Git). 
Coding style guide is found [here](https://twiki.cern.ch/twiki/bin/view/BEABP/PythonStyleGuide). 

### Tests

- Pytest unit- and accuracy-tests are run automatically after each commit via [Travis-CI](https://travis-ci.com/pylhc/omc3). 

### Maintainability

- Additional checks for code-complexity, design-rules, test-coverage, duplication on [CodeClimate](https://codeclimate.com/github/pylhc/omc3).


## Related Packages

- [tfs-pandas](https://github.com/pylhc/tfs)
- [sdds-reader](https://github.com/pylhc/sdds)
- [generic parser](https://github.com/pylhc/generic_parser)
- [pyLHC](https://github.com/pylhc/PyLHC)
- [Beta-Beat Source](https://github.com/pylhc/Beta-Beat.src)
- [optics functions](https://github.com/pylhc/optics_functions)

## Hints for Developers

### Install in Editable Mode

In case you want to install `omc3` as a development package
from the current folder, you can use:

```
git clone https://github.com/pylhc/omc3
pip install --editable omc3
```

This installs the package as a link into the python environment and any changes 
are reflected immediately, without the need to reinstall.

#### Dependencies
```
pip install --editable omc3
```
will also install the required dependencies. 

If you want to install more dependencies, you can use for example:
```
pip install --editable omc3[test]
pip install --editable omc3[setup]
pip install --editable omc3[test,doc]
pip install --editable omc3[all]
```
 where the last one installs **all** dependencies defined in `setup.py`.
 
 Note that the default dependencies and omc3-as-link are also always installed.

## Authors

* **pyLHC/OMC-Team** - *Working Group* - [pyLHC](https://github.com/orgs/pylhc/teams/omc-team)


## License
This project is licensed under the GNU GPLv3 License - see the [LICENSE](LICENSE) file for details.