from omc3.tbt import handler
from pathlib import Path
import matplotlib
from matplotlib import pyplot as plt
from omc3.plotting.utils.annotations import make_top_legend

FILENAME = "plot_tbt"

default_style = {
    u'figure.figsize': [18, 9],
    u'axes.labelsize': 15,
    u'lines.linestyle': '-',
    u'lines.marker': 'None',
    u'markers.fillstyle': u'none',
    u'figure.subplot.hspace': 0.3,  # space between subplots
    u"savefig.format": "pdf",
}


def main(path, bpms, output_dir=None, planes="XY", bunch_id=0, datatype="lhc",
         n_axes=None, turns=None, ylim=None, n_cols_legend=3, manual_style={}):

    manual_style.update(default_style)
    matplotlib.rcParams.update(manual_style)

    data = handler.read_tbt(path, datatype)

    if not n_axes:
        n_axes = len(planes)

    figure, axs = plt.subplots(n_axes, 1)
    if n_axes == 1:
        axs = [axs] * len(planes)

    turns_slice = slice(None)
    if turns:
        turns_slice = slice(*turns)

    for idx_ax, (ax, plane) in enumerate(zip(axs, planes)):
        df = data.matrices[bunch_id][plane]
        for bpm in bpms:
            ax.plot(df.loc[bpm, turns_slice], label=bpm)

        if idx_ax == 0 and n_cols_legend > 0:
            make_top_legend(ax, n_cols_legend)

        ax.set_ylim(ylim)
        ax.set_xlim(_get_xlim(df, turns_slice))
        ax.set_xlabel("Turns")
        ax.set_ylabel(f"Position {plane} [mm]")

    if output_dir:
        path = Path(output_dir)
        path.mkdir(exist_ok=True)
        figure.tight_layout()
        figure.tight_layout()
        figure.savefig(path / f"{FILENAME}.{matplotlib.rcParams['savefig.format']}")

    return figure


def _get_xlim(df, slice_):
    length = df.shape[1]
    start = slice_.start
    if start is None:
        start = 0
    if start < 0:
        start = length-start

    stop = slice_.stop
    if stop is None:
        stop = length-1
    if stop < 0:
        stop = length-start
    stop += 1
    return start, stop


if __name__ == '__main__':
    main(
        path="/home/josch/Work/pres.phd.first_committee_meeting/data/Beam1@Turn@2018_10_30@14_22_42_956/Beam1@Turn@2018_10_30@14_22_42_956.sdds",
        bpms=['BPM.15L6.B1'],
        output_dir="/home/josch/Work/pres.phd.first_committee_meeting/data/plot_output"
    )

