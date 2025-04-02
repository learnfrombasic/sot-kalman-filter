from __future__ import absolute_import, division, print_function, unicode_literals

from src.vendors.pysot.core.config import cfg
from src.vendors.pysot.tracker.siammask_tracker import SiamMaskTracker
from src.vendors.pysot.tracker.siamrpn_tracker import SiamRPNTracker
from src.vendors.pysot.tracker.siamrpnlt_tracker import SiamRPNLTTracker

TRACKS = {
    "SiamRPNTracker": SiamRPNTracker,
    "SiamMaskTracker": SiamMaskTracker,
    "SiamRPNLTTracker": SiamRPNLTTracker,
}


def build_tracker(model):
    return TRACKS[cfg.TRACK.TYPE](model)
