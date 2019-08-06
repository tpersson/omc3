"""
getIPx.out     :*            NAME              BETX           BETXSTD           BETXMDL              ALFX           ALFXSTD           ALFXMDL             BETX*          BETX*STD          BETX*MDL               SX*            SX*STD            SX*MDL           rt(2JX)        rt(2JX)STD
# column_names = ["DPP", "QX", "QXRMS", "QY", "QYRMS", "NATQX", "NATQXRMS", "NATQY", "NATQYRMS", "sqrt2JX", "sqrt2JXSTD", "sqrt2JY", "sqrt2JYSTD", "2JX", "2JXSTD", "2JY", "2JYSTD"]
#  column_names_ac = column_names + ["sqrt2JXRES", "sqrt2JXSTDRES", "sqrt2JYRES", "sqrt2JYSTDRES", "2JXRES", "2JXSTDRES", "2JYRES", "2JYSTDRES"]
"""
from os.path import join
import sys
import context
import numpy as np
import tfs
DIR = "output_directory"
PLANES = ("X", "Y")
# prefixes
ERROR = "ERR"
BEAT = "DELTA"
#suffixes
MODEL = "MDL"

OLD_EXT = ".out"
NEW_EXT = ".tfs"
COMP_SUFFIXES = ("", "_free", "_free2")


def convert_old_directory_to_new(outdir, comp_suffix):
    if comp_suffix not in COMP_SUFFIXES:
        raise ValueError("Invalid compensation suffix")
    for plane in PLANES:
        convert_old_beta_from_amplitude(outdir, comp_suffix, plane)
        convert_old_beta_from_phase(outdir, comp_suffix, plane)
        convert_old_phase(outdir, comp_suffix, plane)
        convert_old_total_phase(outdir, comp_suffix, plane)
        # TODO phase vs phasetot inconsistent naming NAME S , first and second BPMs swapped locations
        convert_old_closed_orbit(outdir, plane)
        convert_old_dispersion(outdir, plane)
    convert_old_normalised_dispersion(outdir)
    # TODO missing getIP, getcouple, getkick


def get_old_directory_from_new(outdir, comp_suffix="_free"):
    if comp_suffix not in COMP_SUFFIXES:
        raise ValueError("Invalid compensation suffix")
    for plane in PLANES:
        get_old_beta_from_amplitude(outdir, comp_suffix, plane)
        get_old_beta_from_phase(outdir, comp_suffix, plane)
        get_old_phase(outdir, comp_suffix, plane)
        get_old_total_phase(outdir, comp_suffix, plane)
        # TODO phase vs phasetot inconsistent naming NAME S , first and second BPMs swapped locations
        get_old_closed_orbit(outdir, plane)
        get_old_dispersion(outdir, plane)
    get_old_normalised_dispersion(outdir)
    open(join(outdir, f"getcouple{comp_suffix}{OLD_EXT}"),"w")
    # TODO missing getIP, getcouple, getkick


def convert_old_beta_from_amplitude(outdir, comp_suffix, plane):
    """
    getampbetax.out: *NAME S COUNT BETX BETXSTD BETXMDL MUXMDL BETXRES BETXSTDRES
    beta_from_amplitude_x.tfs
    """
    old_file_name = "ampbeta"
    new_file_name = "beta_amplitude_"
    try:
        df = tfs.read(join(outdir, f"get{old_file_name}{plane.lower()}{comp_suffix}{OLD_EXT}"))
    except FileNotFoundError:
        return
    df.rename(columns={f"BET{plane}STD": f"{ERROR}BET{plane}",
                       f"BET{plane}STDRES": f"{ERROR}BET{plane}RES"},
              inplace=True)
    df[f"{BEAT}BET{plane}"] = df_rel_diff(df, f"BET{plane}", f"BET{plane}{MODEL}")
    df[f"{ERROR}{BEAT}BET{plane}"] = df_ratio(df, f"{ERROR}BET{plane}", f"BET{plane}{MODEL}")
    tfs.write(join(outdir, f"{new_file_name}{plane.lower()}{NEW_EXT}"), df)


def convert_old_beta_from_phase(outdir, comp_suffix, plane):
    """
    getbetax.out: *NAME S COUNT BETX SYSBETX STATBETX ERRBETX CORR_ALFABETA ALFX SYSALFX STATALFX ERRALFX BETXMDL ALFXMDL MUXMDL NCOMBINATIONS
    beta_from_amplitude_x.tfs
    """
    old_file_name = "beta"
    new_file_name = "beta_phase_"
    try:
        df = tfs.read(join(outdir, f"get{old_file_name}{plane.lower()}{comp_suffix}{OLD_EXT}"))
    except FileNotFoundError:
        return
    df.drop(columns=[f"STATBET{plane}", f"SYSBET{plane}", "CORR_ALFABETA",
                     f"STATALF{plane}", f"SYSALF{plane}"], inplace=True)
    df[f"{BEAT}BET{plane}"] = df_rel_diff(df, f"BET{plane}", f"BET{plane}{MODEL}")
    df[f"{ERROR}{BEAT}BET{plane}"] = df_ratio(df, f"{ERROR}BET{plane}", f"BET{plane}{MODEL}")
    df[f"{BEAT}ALF{plane}"] = df_diff(df, f"ALF{plane}", f"ALF{plane}{MODEL}")
    df[f"{ERROR}{BEAT}ALF{plane}"] = df.loc[:, f"{ERROR}ALF{plane}"].values
    tfs.write(join(outdir, f"{new_file_name}{plane.lower()}{NEW_EXT}"), df)


def convert_old_phase(outdir, comp_suffix, plane):
    """
    getphasex.out: *NAME NAME2 S S1 COUNT PHASEX STDPHX PHXMDL MUXMDL
    phase_x.tfs
    """
    old_file_name = "phase"
    new_file_name = "phase_"
    try:
        df = tfs.read(join(outdir, f"get{old_file_name}{plane.lower()}{comp_suffix}{OLD_EXT}"))
    except FileNotFoundError:
        return
    df.rename(columns={f"STDPH{plane}": f"{ERROR}PHASE{plane}",
                       f"PH{plane}{MODEL}": f"PHASE{plane}{MODEL}", "S1": "S2"},
              inplace=True)
    df[f"{BEAT}PHASE{plane}"] = df_ang_diff(df, f"PHASE{plane}", f"PHASE{plane}{MODEL}")
    df[f"{ERROR}{BEAT}PHASE{plane}"] = df.loc[:, f"{ERROR}PHASE{plane}"].values
    tfs.write(join(outdir, f"{new_file_name}{plane.lower()}{NEW_EXT}"), df)


def convert_old_total_phase(outdir, comp_suffix, plane):
    """
    getphasex.out: *NAME NAME2 S S1 COUNT PHASEX STDPHX PHXMDL MUXMDL
    phase_x.tfs
    """
    old_file_name = "phasetot"
    new_file_name = "total_phase_"
    try:
        df = tfs.read(join(outdir, f"get{old_file_name}{plane.lower()}{comp_suffix}{OLD_EXT}"))
    except FileNotFoundError:
        return
    df.rename(columns={f"STDPH{plane}": f"{ERROR}PHASE{plane}",
                       f"PH{plane}{MODEL}": f"PHASE{plane}{MODEL}", "S1": "S2"},
              inplace=True)
    df[f"{BEAT}PHASE{plane}"] = df_ang_diff(df, f"PHASE{plane}", f"PHASE{plane}{MODEL}")
    df[f"{ERROR}{BEAT}PHASE{plane}"] = df.loc[:, f"{ERROR}PHASE{plane}"].values
    tfs.write(join(outdir, f"{new_file_name}{plane.lower()}{NEW_EXT}"), df)


def convert_old_closed_orbit(outdir, plane):
    """
    getCOx.out: *NAME S COUNT X STDX XMDL MUXMDL
    orbit_x.tfs
    """
    old_file_name = "CO"
    new_file_name = "orbit_"
    try:
        df = tfs.read(join(outdir, f"get{old_file_name}{plane.lower()}{OLD_EXT}"))
    except FileNotFoundError:
        return
    df.rename(columns={f"STD{plane}": f"{ERROR}{plane}"},
              inplace=True)
    df[f"{BEAT}{plane}"] = df_diff(df, f"{plane}", f"{plane}{MODEL}")
    df[f"{ERROR}{BEAT}{plane}"] = df.loc[:, f"{ERROR}{plane}"].values
    tfs.write(join(outdir, f"{new_file_name}{plane.lower()}{NEW_EXT}"), df)


def convert_old_dispersion(outdir, plane):
    """
    getDx.out: *NAME S COUNT DX STDDX DPX DXMDL DPXMDL MUXMDL
    dispersion_x.tfs
    """
    old_file_name = "D"
    new_file_name = "dispersion_"
    try:
        df = tfs.read(join(outdir, f"get{old_file_name}{plane.lower()}{OLD_EXT}"))
    except FileNotFoundError:
        return
    df.rename(columns={f"STDD{plane}": f"{ERROR}D{plane}"},
              inplace=True)
    df[f"{BEAT}D{plane}"] = df_diff(df, f"D{plane}", f"D{plane}{MODEL}")
    df[f"{ERROR}{BEAT}D{plane}"] = df.loc[:, f"{ERROR}D{plane}"].values
    tfs.write(join(outdir, f"{new_file_name}{plane.lower()}{NEW_EXT}"), df)


def convert_old_normalised_dispersion(outdir):
    """
    getNDx.out: *NAME S COUNT NDX STDNDX DX DPX NDXMDL DXMDL DPXMDL MUXMDL
    normalised_dispersion_x.tfs
    """
    plane = "X"
    old_file_name = "ND"
    new_file_name = "normalised_dispersion_"
    try:
        df = tfs.read(join(outdir, f"get{old_file_name}{plane.lower()}{OLD_EXT}"))
    except FileNotFoundError:
        return
    if "DX" in df.columns:
        df.rename(columns={f"STDND{plane}": f"{ERROR}ND{plane}",
                           f"STDD{plane}": f"{ERROR}D{plane}"},
                  inplace=True)
        df[f"{BEAT}ND{plane}"] = df_diff(df, f"ND{plane}", f"ND{plane}{MODEL}")
        df[f"{ERROR}{BEAT}ND{plane}"] = df.loc[:, f"{ERROR}ND{plane}"].values
        df[f"{BEAT}D{plane}"] = df_diff(df, f"D{plane}", f"D{plane}{MODEL}")
        df[f"{ERROR}{BEAT}D{plane}"] = df.loc[:, f"{ERROR}D{plane}"].values
    else:
        df.rename(columns={f"STDND{plane}": f"{ERROR}ND{plane}"},
                  inplace=True)
        df[f"{BEAT}ND{plane}"] = df_diff(df, f"ND{plane}", f"ND{plane}{MODEL}")
        df[f"{ERROR}{BEAT}ND{plane}"] = df.loc[:, f"{ERROR}ND{plane}"].values
    tfs.write(join(outdir, f"{new_file_name}{plane.lower()}{NEW_EXT}"), df)


def df_diff(df, a_col, b_col):
    return _diff(df.loc[:, a_col].values, df.loc[:, b_col].values)


def _diff(a, b):
    return a - b


def df_ratio(df, a_col, b_col):
    return _ratio(df.loc[:, a_col].values, df.loc[:, b_col].values)


def _ratio(a, b):
    return a / b


def df_rel_diff(df, a_col, b_col):
    return _rel_diff(df.loc[:, a_col].values, df.loc[:, b_col].values)


def _rel_diff(a, b):
    return (a / b) - 1


def df_ang_diff(df, a_col, b_col):
    return _ang_diff(df.loc[:, a_col].values, df.loc[:, b_col].values)


def _ang_diff(a, b):
    return _interval_check(_interval_check(a) - _interval_check(b))


def _interval_check(ang):
    return np.where(np.abs(ang) > 0.5, ang - np.sign(ang), ang)


def get_old_beta_from_amplitude(outdir, comp_suffix, plane):
    """
    getampbetax.out: *NAME S COUNT BETX BETXSTD BETXMDL MUXMDL BETXRES BETXSTDRES
    beta_from_amplitude_x.tfs
    """
    old_file_name = "ampbeta"
    new_file_name = "beta_amplitude_"
    try:
        df = tfs.read(join(outdir, f"{new_file_name}{plane.lower()}{NEW_EXT}"))
    except FileNotFoundError:
        return
    df.rename(columns={f"{ERROR}BET{plane}": f"BET{plane}STD",
                       f"{ERROR}BET{plane}RES": f"BET{plane}STDRES"},
              inplace=True)
    tfs.write(join(outdir, f"get{old_file_name}{plane.lower()}{comp_suffix}{OLD_EXT}"), df)


def get_old_beta_from_phase(outdir, comp_suffix, plane):
    """
    getbetax.out: *NAME S COUNT BETX SYSBETX STATBETX ERRBETX CORR_ALFABETA ALFX SYSALFX STATALFX ERRALFX BETXMDL ALFXMDL MUXMDL NCOMBINATIONS
    beta_from_amplitude_x.tfs
    """
    old_file_name = "beta"
    new_file_name = "beta_phase_"
    try:
        df = tfs.read(join(outdir, f"{new_file_name}{plane.lower()}{NEW_EXT}"))
    except FileNotFoundError:
        return
    tfs.write(join(outdir, f"get{old_file_name}{plane.lower()}{comp_suffix}{OLD_EXT}"), df)


def get_old_phase(outdir, comp_suffix, plane):
    """
    getphasex.out: *NAME NAME2 S S1 COUNT PHASEX STDPHX PHXMDL MUXMDL
    phase_x.tfs
    """
    old_file_name = "phase"
    new_file_name = "phase_"
    try:
        df = tfs.read(join(outdir, f"{new_file_name}{plane.lower()}{NEW_EXT}"))
    except FileNotFoundError:
        return
    df.rename(columns={f"{ERROR}PHASE{plane}": f"STDPH{plane}",
                       f"PHASE{plane}{MODEL}": f"PH{plane}{MODEL}", "S2": "S1"},
              inplace=True)
    tfs.write(join(outdir, f"get{old_file_name}{plane.lower()}{comp_suffix}{OLD_EXT}"), df)


def get_old_total_phase(outdir, comp_suffix, plane):
    """
    getphasex.out: *NAME NAME2 S S1 COUNT PHASEX STDPHX PHXMDL MUXMDL
    phase_x.tfs
    """
    old_file_name = "phasetot"
    new_file_name = "total_phase_"
    try:
        df = tfs.read(join(outdir, f"{new_file_name}{plane.lower()}{NEW_EXT}"))
    except FileNotFoundError:
        return
    df.rename(columns={f"{ERROR}PHASE{plane}": f"STDPH{plane}",
                       f"PHASE{plane}{MODEL}": f"PH{plane}{MODEL}", "S2": "S1"},
              inplace=True)
    tfs.write(join(outdir, f"get{old_file_name}{plane.lower()}{comp_suffix}{OLD_EXT}"), df)


def get_old_closed_orbit(outdir, plane):
    """
    getCOx.out: *NAME S COUNT X STDX XMDL MUXMDL
    orbit_x.tfs
    """
    old_file_name = "CO"
    new_file_name = "orbit_"
    try:
        df = tfs.read(join(outdir, f"{new_file_name}{plane.lower()}{NEW_EXT}"))
    except FileNotFoundError:
        return
    df.rename(columns={f"{ERROR}{plane}": f"STD{plane}"},
              inplace=True)
    tfs.write(join(outdir, f"get{old_file_name}{plane.lower()}{OLD_EXT}"), df)


def get_old_dispersion(outdir, plane):
    """
    getDx.out: *NAME S COUNT DX STDDX DPX DXMDL DPXMDL MUXMDL
    dispersion_x.tfs
    """
    old_file_name = "D"
    new_file_name = "dispersion_"
    try:
        df = tfs.read(join(outdir, f"get{new_file_name}{plane.lower()}{NEW_EXT}"))
    except FileNotFoundError:
        return
    df.rename(columns={f"{ERROR}D{plane}": f"STDD{plane}"},
              inplace=True)
    tfs.write(join(outdir, f"{old_file_name}{plane.lower()}{OLD_EXT}"), df)


def get_old_normalised_dispersion(outdir):
    """
    getNDx.out: *NAME S COUNT NDX STDNDX DX DPX NDXMDL DXMDL DPXMDL MUXMDL
    normalised_dispersion_x.tfs
    """
    plane = "X"
    old_file_name = "ND"
    new_file_name = "normalised_dispersion_"
    try:
        df = tfs.read(join(outdir, f"get{new_file_name}{plane.lower()}{NEW_EXT}"))
    except FileNotFoundError:
        return
    df.rename(columns={f"{ERROR}ND{plane}": f"STDND{plane}",
                       f"{ERROR}D{plane}": f"STDD{plane}"},
              inplace=True)

    tfs.write(join(outdir, f"{old_file_name}{plane.lower()}{OLD_EXT}"), df)


if __name__ == '__main__':
    #convert_old_directory_to_new("test_converter", "_free2")
    get_old_directory_from_new([b.replace("--output=","") for b in sys.argv[1:] if "--output" in b][0])
