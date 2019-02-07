"""
.. module: chromatic

Created on 11/01/19

:author: Lukas Malina

It computes chromaticity and chromatic beta-beating from 3D oscillations.
"""
import numpy as np
from os.path import join
from utils import outliers
import pandas as pd
import tfs
PLANES = ('X', 'Y')


def get_chromatic_beating(meas_input, input_files, tune_dict, dpp_amp, chromas):
    synch_beta_col = {"X": ["AMP101", "AMP10_1"], "Y": ["AMP011", "AMP01_1"]}
    for plane in PLANES:
        delta = tune_dict[plane]["Q"] - tune_dict[plane]["QF"]
        model = meas_input.accelerator.get_model_tfs()
        synch_beta = input_files.joined_frame(plane, synch_beta_col[plane])
        df = pd.merge(model.loc[:, ['NAME', 'S', 'WX', 'WY', 'PHIX', 'PHIY']], synch_beta,
                      how='inner', left_index=True, right_index=True)
        aver_amps = np.sqrt(synch_beta.loc[:, input_files.get_columns(
            synch_beta, synch_beta_col[plane][0])].values *
            synch_beta.loc[:, input_files.get_columns(synch_beta, synch_beta_col[plane][1])].values) * 2
        # 2 comes from sb lines on both sides...+ Qs is correction for driven motion

        # TODO do the sign correctly
        chroma_contribution = chromas[plane] * dpp_amp / np.abs(delta)
        chroma_beating_sqrt = aver_amps - chroma_contribution
        chroma_beating = (np.square(1 + chroma_beating_sqrt) - 1) / (2 * dpp_amp)
        for i in range(chroma_beating.shape[1]):
            df[f"CHBEAT__{i}"] = chroma_beating[:, i]
        df[f"CHROMBEAT"] = np.mean(chroma_beating, axis=1)
        df[f"STDCHROMBEAT"] = np.std(chroma_beating, axis=1)
        tfs.write(join(meas_input.outputdir, f"chrombeat{plane.lower()}.out"), df)

    return


def get_amp_chroma(meas_input, input_files, tune_dict, dpp_amp):
    synch_beta_col = {"X": ["AMP101", "AMP10_1"], "Y": ["AMP011", "AMP01_1"]}
    chromas = {}
    for plane in PLANES:
        delta = tune_dict[plane]["Q"] - tune_dict[plane]["QF"]
        synch_beta = input_files.joined_frame(plane, synch_beta_col[plane])
        mask = meas_input.accelerator.get_element_types_mask(synch_beta.index, ["arc_bpm"])
        aver_amps = np.sqrt(synch_beta.loc[mask, input_files.get_columns(
            synch_beta, synch_beta_col[plane][0])].values *
            synch_beta.loc[mask, input_files.get_columns(
                synch_beta, synch_beta_col[plane][1])].values) * 2 * np.abs(delta) / dpp_amp
        # 2 comes from sb lines on both sides...+ Qs is correction for driven motion

        if aver_amps.ndim == 1:
            filtered_amps = aver_amps[outliers.get_filter_mask(aver_amps)]
            chromas[plane] = np.average(filtered_amps)
            chromas[plane+'STD'] = np.std(filtered_amps)/np.sqrt(len(filtered_amps))
        else:
            avs = []
            stds = []
            for i in range(aver_amps.shape[1]):
                filtered_amps = aver_amps[outliers.get_filter_mask(aver_amps[:, i]), i]
                avs.append(np.average(filtered_amps))
                stds.append(np.std(filtered_amps) / np.sqrt(len(filtered_amps)))
            chromas[plane] = np.array(avs)
            chromas[plane+'STD'] = np.array(stds)
    return chromas
