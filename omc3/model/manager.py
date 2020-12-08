"""
Manager
-------------------

Contains entrypoint wrappers to get accelerator classes or their instances
"""
from generic_parser.entrypoint_parser import entrypoint, EntryPoint, EntryPointParameters
from omc3.model.accelerators import lhc, ps, esrf, psbooster, skekb, petra, iota

ACCELS = {
    lhc.Lhc.NAME: lhc.Lhc,
    ps.Ps.NAME: ps.Ps,
    esrf.Esrf.NAME: esrf.Esrf,
    psbooster.Psbooster.NAME: psbooster.Psbooster,
    skekb.SKekB.NAME: skekb.SKekB,
    "JPARC": skekb.SKekB,
    petra.Petra.NAME: petra.Petra,
    iota.Iota.NAME: iota.Iota
}


def _get_params():
    print("LLLLLLLLLL")
    params = EntryPointParameters()
    params.add_parameter(name="accel", required=True, choices=list(ACCELS.keys()),
                         help="Choose the accelerator to use.Can be the class already.")
    return params


@entrypoint(_get_params())
def get_accelerator(opt, other_opt):
    """ Returns accelerator instance. """
    print("bbbb", other_opt)
    if not isinstance(opt.accel, str):
        # assume it's the class
        return opt.accel
    print("ccccc", other_opt, opt)
    myinst = ACCELS[opt.accel](other_opt)
    print("nnnnnn", myinst.modifiers )
    return ACCELS[opt.accel](other_opt)


@entrypoint(_get_params())
def get_parsed_opt(opt, other_opt):
    """ Get all accelerator related options as a nice dict. """
    accel = ACCELS[opt.accel]
    parser = EntryPoint(accel.get_parameters(), strict=True)
    accel_opt = parser.parse(other_opt)
    print("ffff", accel_opt)
    return {**opt, **accel_opt}
