import pytest
import os
import tfs
import shutil
import numpy as np
from . import context
from run_kmod import analyse_kmod
from kmod import kmod_constants

CURRENT_DIR = os.path.dirname(__file__)
PLANES = ('X', 'Y')
LIMITS = {'Accuracy': 0.01,
          'Meas Accuracy': 0.05,
          'Num Precision': 1E-4,
          'Meas Precision': 0.1}


def test_kmod_simulation_ip1b1(_workdir_path):

    analyse_kmod(betastar=[0.25, 0.0],
                 work_dir=_workdir_path,
                 beam='b1',
                 simulation=True,
                 no_sig_dig=True,
                 no_plots=False,
                 ip='ip1',
                 cminus=0.0,
                 misalignment=0.0,
                 errorK=0.0,
                 errorL=0.0,
                 tunemeasuncertainty=0.0E-5)
    results = tfs.read(os.path.join(_workdir_path, "ip1B1", "results.tfs"))
    original_twiss = tfs.read(os.path.join(_workdir_path, "twiss.tfs"), index='NAME')

    for plane in PLANES:
        beta_sim = float(original_twiss.loc['IP1', f"BET{plane}"])
        beta_meas = float(results[kmod_constants.get_betastar_col(plane)].loc[0])
        assert (np.abs(beta_meas-beta_sim))/beta_sim < LIMITS['Accuracy']
        beta_err_meas = float(results[kmod_constants.get_betastar_err_col(plane)].loc[0])
        assert (np.abs(beta_err_meas)) < LIMITS['Num Precision']


def test_kmod_simulation_ip1b2(_workdir_path):

    analyse_kmod(betastar=[0.25, 0.25, 0.0],
                 work_dir=_workdir_path,
                 beam='b2',
                 simulation=True,
                 no_sig_dig=True,
                 no_plots=False,
                 ip='ip1',
                 cminus=0.0,
                 misalignment=0.0,
                 errorK=0.0,
                 errorL=0.0,
                 tunemeasuncertainty=0.0E-5)
    results = tfs.read(os.path.join(_workdir_path, "ip1B2", "results.tfs"))
    original_twiss = tfs.read(os.path.join(_workdir_path, "twiss.tfs"), index='NAME')

    for plane in PLANES:
        beta_sim = float(original_twiss.loc['IP1', f"BET{plane}"])
        beta_meas = float(results[kmod_constants.get_betastar_col(plane)].loc[0])
        assert (np.abs(beta_meas-beta_sim))/beta_sim < LIMITS['Accuracy']
        beta_err_meas = float(results[kmod_constants.get_betastar_err_col(plane)].loc[0])
        assert (np.abs(beta_err_meas)) < LIMITS['Num Precision']


def test_kmod_meas_ip1b1(_workdir_path):

    analyse_kmod(betastar=[0.44, 0.44, 0.0, 0.0],
                 work_dir=_workdir_path,
                 beam='b1',
                 simulation=False,
                 no_sig_dig=True,
                 no_plots=False,
                 ip='ip1',
                 cminus=0.0,
                 misalignment=0.0,
                 errorK=0.0,
                 errorL=0.0,
                 tunemeasuncertainty=2.5E-5)
    results = tfs.read(os.path.join(_workdir_path, "ip1B1", "results.tfs"))
    beta_sim = {'X': 0.45, 'Y': 0.43}
    for plane in PLANES:

        beta_meas = float(results[kmod_constants.get_betastar_col(plane)].loc[0])
        assert (np.abs(beta_meas-beta_sim[plane]))/beta_sim[plane] < LIMITS['Meas Accuracy']
        beta_err_meas = float(results[kmod_constants.get_betastar_err_col(plane)].loc[0])
        assert (beta_err_meas/beta_meas) < LIMITS['Meas Precision']


def test_kmod_meas_ip1b2(_workdir_path):

    analyse_kmod(betastar=[0.44, 0.0],
                 work_dir=_workdir_path,
                 beam='b2',
                 simulation=False,
                 no_sig_dig=True,
                 no_plots=False,
                 ip='ip1',
                 cminus=0.0,
                 misalignment=0.0,
                 errorK=0.0,
                 errorL=0.0,
                 tunemeasuncertainty=2.5E-5)
    results = tfs.read(os.path.join(_workdir_path, "ip1B2", "results.tfs"))
    beta_sim = {'X': 0.387, 'Y': 0.410}
    for plane in PLANES:

        beta_meas = float(results[kmod_constants.get_betastar_col(plane)].loc[0])
        assert (np.abs(beta_meas-beta_sim[plane]))/beta_sim[plane] < LIMITS['Meas Accuracy']
        beta_err_meas = float(results[kmod_constants.get_betastar_err_col(plane)].loc[0])
        assert (beta_err_meas/beta_meas) < LIMITS['Meas Precision']


def test_kmod_meas_ip4b1(_workdir_path):

    analyse_kmod(betastar=[200.0, -100.0],
                 work_dir=_workdir_path,
                 beam='b1',
                 simulation=False,
                 no_sig_dig=True,
                 no_plots=False,
                 circuits=['RQ6.R4B1', 'RQ7.R4B1'],
                 cminus=0.0,
                 misalignment=0.0,
                 errorK=0.0,
                 errorL=0.0,
                 tunemeasuncertainty=0.5E-5)
    results = tfs.read(os.path.join(_workdir_path, "MQY.6R4.B1-MQM.7R4.B1", "beta_instrument.tfs"), index='INSTRUMENT')

    original = {
                'BPMCS.7R4.B1': (17.5074335336, 157.760070696),
                'BPM.7R4.B1': (17.6430538896, 157.972911909),
                'BQSH.7R4.B1': (455.457631868, 124.586686684),
                'BPLH.7R4.B1': (423.68951095, 123.578577484)
    }

    for inst in results.index:
        beta_x, beta_y = original[inst]
        beta_meas = float(results[kmod_constants.get_beta_col('X')].loc[inst])
        assert (np.abs(beta_meas-beta_x))/beta_x < LIMITS['Meas Accuracy']
        beta_err_meas = float(results[kmod_constants.get_beta_err_col('X')].loc[inst])
        assert (beta_err_meas/beta_meas) < LIMITS['Meas Precision']

        beta_meas = float(results[kmod_constants.get_beta_col('Y')].loc[inst])
        assert (np.abs(beta_meas-beta_y))/beta_y < LIMITS['Meas Accuracy']
        beta_err_meas = float(results[kmod_constants.get_beta_err_col('Y')].loc[inst])
        assert (beta_err_meas/beta_meas) < LIMITS['Meas Precision']


def test_kmod_meas_ip4b2(_workdir_path):

    analyse_kmod(betastar=[200.0, -100.0],
                 work_dir=_workdir_path,
                 beam='b2',
                 simulation=False,
                 no_sig_dig=True,
                 no_plots=False,
                 circuits=['RQ7.L4B2', 'RQ6.L4B2'],
                 cminus=0.0,
                 misalignment=0.0,
                 errorK=0.0,
                 errorL=0.0,
                 tunemeasuncertainty=0.5E-5)
    results = tfs.read(os.path.join(_workdir_path, "MQM.7L4.B2-MQY.6L4.B2", "beta_instrument.tfs"), index='INSTRUMENT')

    original = {
                'BPMYA.6L4.B2': (456.789268726, 149.073169556),
                'BGVCA.B7L4.B2': (119.359634764, 152.116072289),
                'BPLH.B7L4.B2': (434.440558008, 148.460642194),
                'BPLH.A7L4.B2': (441.781928671, 148.654814221)
    }

    for inst in results.index:
        beta_x, beta_y = original[inst]
        beta_meas = float(results[kmod_constants.get_beta_col('X')].loc[inst])
        assert (np.abs(beta_meas-beta_x))/beta_x < LIMITS['Meas Accuracy']
        beta_err_meas = float(results[kmod_constants.get_beta_err_col('X')].loc[inst])
        assert (beta_err_meas/beta_meas) < LIMITS['Meas Precision']

        beta_meas = float(results[kmod_constants.get_beta_col('Y')].loc[inst])
        assert (np.abs(beta_meas-beta_y))/beta_y < LIMITS['Meas Accuracy']
        beta_err_meas = float(results[kmod_constants.get_beta_err_col('Y')].loc[inst])
        assert (beta_err_meas/beta_meas) < LIMITS['Meas Precision']


@pytest.fixture()
def _workdir_path():
    try:
        workdir = os.path.join(CURRENT_DIR, os.pardir, "inputs", "kmod")
        yield workdir
    finally:
        if os.path.isdir(os.path.join(workdir, 'ip1B1')):
            shutil.rmtree(os.path.join(workdir, 'ip1B1'))

        if os.path.isdir(os.path.join(workdir, 'ip1B2')):
            shutil.rmtree(os.path.join(workdir, 'ip1B2'))

        if os.path.isdir(os.path.join(workdir, 'MQY.6R4.B1-MQM.7R4.B1')):
            shutil.rmtree(os.path.join(workdir, 'MQY.6R4.B1-MQM.7R4.B1'))

        if os.path.isdir(os.path.join(workdir, 'MQM.7L4.B2-MQY.6L4.B2')):
            shutil.rmtree(os.path.join(workdir, 'MQM.7L4.B2-MQY.6L4.B2'))
