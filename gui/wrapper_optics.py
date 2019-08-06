import sys
import context
from hole_in_one import hole_in_one_entrypoint

old_options = ["--tbtana", "--lhcphase", "--errordefs", "--nprocesses", "--average_tune", "--numbpm", "--useerrorofmean", "--errthreshold"]
a = sys.argv[1:]
new_a = []
for i, b in enumerate(a):
    for old in old_options:
        if old in b:
            b = ""
    if len(b):
        new_a.extend(b.replace("--accel=LHCB", "--accel lhc --lhcmode lhc_runII_2018 --beam ").replace(
            "--accel=PSBOOSTER", "--accel psbooster").replace("--accel=PS", "--accel ps").replace(
            "--bpmu=", "").replace("=", " ").replace(",", " ").replace("twiss.dat", "").replace(
            "--coupling", "--only_coupling").replace("--threebpm", "--three_bpm_method").replace(
            "--bbthreshold", "--max_beta_beating").replace("--nbcpl", "--coupling_method").replace(
            "--cocut", "--max_closed_orbit").split())
new_a.extend(["--optics"])
hole_in_one_entrypoint(new_a)

# --three_d_excitation
