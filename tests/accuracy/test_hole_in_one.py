from os.path import abspath, dirname, join, isdir
from shutil import rmtree
import glob
import tfs
import numpy as np
from omc3.hole_in_one import hole_in_one_entrypoint
from omc3.madx_wrapper import main as madx_run

PLANES = ('x', 'y')

RESULTS_PATH = abspath(join(dirname(__file__), "..", "results"))
MODEL_PATH = abspath(join(dirname(__file__), "..", "inputs", "models", "inj_2018_b1"))
TRACK_FILES = ['track1.one', 'track2.one', 'track3.one']
OPTICS_MEASUREMENTS_RESULTS_FILES = {
                 'beta_amplitude':      'beta_amplitude_{plane}.tfs',      # List containing all expected results files,
                 'beta_phase':          'beta_phase_{plane}.tfs',          # at later point, possibly replaced by importing
                 'interaction_point':   'interaction_point_{plane}.tfs',   # from global constants
                 'kick':                'kick_{plane}.tfs',
                 'orbit':               'orbit_{plane}.tfs',
                 'phase':               'phase_{plane}.tfs',
                 'special_phase':       'special_phase_{plane}.txt',
                 'total_phase':         'total_phase_{plane}.tfs',
                }
MEASUREMENT_FILES_EXTENSIONS = ['.tfs', '.txt',
                                '.ampsx', '.ampsy',
                                '.freqsx', '.freqsy',
                                '.linx', '.liny',
                                '.bad_bpms_x', '.bad_bpms_y',
                                ]

HARPY_RESULTS_FILES = [
                       '{track}.amps{{plane}}',
                       '{track}.freqs{{plane}}',
                       '{track}.lin{{plane}}',
                       '{track}.bad_bpms_{{plane}}',
                      ]

RDT_RESULT_FILES = {
                    'normal_octupole': ['f0013_y.tfs', 'f0040_y.tfs', 'f0211_y.tfs', 'f0220_y.tfs',
                                        'f1102_x.tfs', 'f1120_x.tfs', 'f1300_x.tfs', 'f2002_x.tfs',
                                        'f2011_y.tfs', 'f2020_x.tfs', 'f2020_y.tfs', 'f4000_x.tfs'],
                    'normal_sextupole': ['f0111_y.tfs', 'f0120_y.tfs', 'f1002_x.tfs', 'f1011_y.tfs',
                                         'f1020_x.tfs', 'f1020_y.tfs', 'f1200_x.tfs', 'f3000_x.tfs'],
                    'skew_quadrupole': ['f0110_y.tfs', 'f1001_x.tfs', 'f1010_x.tfs', 'f1010_y.tfs'],
                    'skew_sextupole': ['f0012_y.tfs', 'f0030_y.tfs', 'f0210_y.tfs', 'f1101_x.tfs',
                                       'f1110_x.tfs', 'f2001_x.tfs', 'f2010_x.tfs', 'f2010_y.tfs'],
                    }

PTC_RDT_NAMING = dict(AMP='GNFA_{j}_{k}_{l}_{m}_0_0',
                      REAL='GNFC_{j}_{k}_{l}_{m}_0_0',
                      IMAG='GNFS_{j}_{k}_{l}_{m}_0_0')


def test_hole_in_one():

    madx_run(dict(file=join(MODEL_PATH, 'model_and_track.madx'), cwd=MODEL_PATH))

    harpy_opt = dict(
        harpy=True,
        files=[join(MODEL_PATH, filename) for filename in TRACK_FILES],
        outputdir=RESULTS_PATH,
        model=join(MODEL_PATH, 'twiss.dat'),
        unit='m',
        turns=[0, 256],
        to_write=['lin', 'spectra', 'full_spectra', 'bpm_summary'],
        tbt_datatype='trackone',
    )
    clean_opt = dict(
        clean=False,
    )
    fft_opt = dict(
        autotunes="transverse",
        window="hann",
        turn_bits=12,
        output_bits=10,
    )
    optics_opt = dict(
        optics=True,
        coupling_method=0,
        range_of_bpms=11,
        nonlinear=True,
        three_bpm_method=False,
        compensation="none",
    )
    model_opt = dict(
        accel="lhc",
        year="2018",
        ats=False,
        beam=1,
        model_dir=MODEL_PATH,
    )

    hole_in_one_entrypoint({**harpy_opt, **clean_opt, **fft_opt, **optics_opt, **model_opt})

    # check if all optics measurements files are present
    check_if_all_files_present(RESULTS_PATH,
                               OPTICS_MEASUREMENTS_RESULTS_FILES.values())

    # check if all files from harmonic analysis are present
    check_if_all_files_present(join(RESULTS_PATH, 'lin_files'),
                               [harpyfiles.format(track=track) for track in TRACK_FILES
                                                               for harpyfiles in HARPY_RESULTS_FILES])

    # check if all files from RDT analysis are present
    [check_if_all_files_present(join(RESULTS_PATH, 'rdt', multipole), RDT_RESULT_FILES[multipole])
     for multipole in RDT_RESULT_FILES.keys()]

    # check if all files from optics measurements are not empty
    check_if_files_are_not_empty(RESULTS_PATH, ('.txt'))

    # check if all files from harmonic analysis are not empty
    check_if_files_are_not_empty(join(RESULTS_PATH, 'lin_files'), ('.bad_bpms_x', '.bad_bpms_y'))

    # check if all files from optics measurements are not empty
    [check_if_files_are_not_empty(join(RESULTS_PATH, 'rdt', multipole)) for multipole in RDT_RESULT_FILES.keys()]

    # load tracking model results
    modeltwiss = tfs.read(join(MODEL_PATH, 'twiss.dat'))
    modelrdt = tfs.read(join(MODEL_PATH, 'ptc_rdt.tfs'))
    modelkick = tfs.read(join(MODEL_PATH, 'Tracking_actions.tfs'))

    # check orbit files
    compare_orbit(modeltwiss, OPTICS_MEASUREMENTS_RESULTS_FILES['orbit'])
    # check kick files

    # check phase files

    # check optics files
    compare_optics(modeltwiss, OPTICS_MEASUREMENTS_RESULTS_FILES['beta_phase'])
    compare_optics(modeltwiss, OPTICS_MEASUREMENTS_RESULTS_FILES['beta_amplitude'])

    # check freq files (how & what?)

    # check RDT
    [compare_rdt(multipole, modelrdt) for multipole in RDT_RESULT_FILES.keys()]

    _clean_up(RESULTS_PATH)

def compare_optics(modeltwiss, opticsfilename):
    for plane in PLANES:
        opticsfile = tfs.read(join(RESULTS_PATH, opticsfilename.format(plane=plane)))
        assert np.max(np.abs(orbitfile[f'BET{plane.upper()}']-modeltwiss[f'BET{plane.upper()}'])) < 1E-4

def compare_orbit(modeltwiss, orbitfilename):
    for plane in PLANES:
        orbitfile = tfs.read(join(RESULTS_PATH, orbitfilename.format(plane=plane)))
        print(modeltwiss[~modeltwiss.NAME.isin(orbitfile.NAME)])
        assert np.max(np.abs(orbitfile[plane.upper()]-modeltwiss[plane.upper()])) < 1E-4

def compare_rdt(multipole, modelrdt):

    for rdtfile in RDT_RESULT_FILES[multipole]:
        j, k, l, m = extract_rdt_indices_from_filename(rdtfile)

        measured_rdt_file = tfs.read(join(RESULTS_PATH, 'rdt', multipole, rdtfile))

        for key, val in PTC_RDT_NAMING.items():
            assert measured_rdt_file[key] - modelrdt[val.format(j=j, k=k, l=l, m=m)] < 1E-2


def extract_rdt_indices_from_filename(filename):
    return filename[1], filename[2], filename[3], filename[4]


def get_all_files_in_dir(path='', fileext=[]):
    return [f for ext in fileext for f in glob.glob(join(path, f'*{ext}'))]


def check_if_all_files_present(resultpath, resultfiles):
    generated_results_files = get_all_files_in_dir(resultpath, MEASUREMENT_FILES_EXTENSIONS)
    test_results_files = [join(resultpath, filename.format(plane=plane)) for plane in PLANES
                                                                        for filename in resultfiles]
    assert set(generated_results_files) == set(test_results_files)


def check_if_files_are_not_empty(resultpath, exclude_extension=()):
    generated_results_files = get_all_files_in_dir(resultpath, MEASUREMENT_FILES_EXTENSIONS)
    for f in generated_results_files:
        if not f.endswith(exclude_extension):
            assert not tfs.read(f).empty


def _clean_up(path_dir):
    if isdir(path_dir):
        rmtree(path_dir, ignore_errors=True)
