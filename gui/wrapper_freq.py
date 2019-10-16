import sys
import context
from hole_in_one import hole_in_one_entrypoint
old_options = ["harpy", "svd_mode", "harpy_mode", ]
a = sys.argv[1:]
new_a = []
for i, b in enumerate(a):
    if "nattunex" in b:
        a.append(a.pop(i))
for i, b in enumerate(a):
    if "nattuney" in b:
        a.append(a.pop(i))
for i, b in enumerate(a):
    for old in old_options:
        if old in b:
            b = ""
    if len(b):
        new_a.extend(b.replace("=", " ").replace(",", " ").replace("clean", "--clean").replace(
            "--pk-2-pk", "--peak_to_peak").replace("--max-peak-cut", "--max_peak").replace(
            "--no_exact_zeros", "--keep_exact_zeros").replace("--startturn", "--turns").replace(
            "--endturn", "").replace("--single_svd_bpm_threshold", "--svd_dominance_limit").replace(
            "--tune_--clean_limit", "--tune_clean_limit").replace("--tunex", "--tunes").replace(
            "--tuney", "").replace("--tunez","").replace("--nattunex", "--nattunes").replace(
            "--nattuney", "").split())
new_a.extend(["0.0", "--harpy"])
hole_in_one_entrypoint(new_a)#--first_bpm BPM.33L2.B1 #BPM.34R8.B2 --opposite_direction 
