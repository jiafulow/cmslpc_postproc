#!/usr/bin/env python
import os
import sys

import ROOT

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.analysis.higgs.vhbb.VHbbProducer import vhbb
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import btagSFProducer
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jecUncertainties import jecUncertAll_cppOut


def main():
    ROOT.PyConfig.IgnoreCommandLineOptions = True
    ROOT.gROOT.SetBatch(True)

    postprocessor = PostProcessor(
        # The output directory is the current working directory.
        outputDir='.',
        # Any and all command line arguments are taken to be an input file path.
        inputFiles=sys.argv[1:],
        # The skimming selection string.
        cut=(
            '(Sum$(Electron_pt > 20 && Electron_mvaSpring16GP_WP90) >= 2'
            '    || Sum$(Muon_pt > 20) >= 2'
            '    || Sum$(Electron_pt > 20 && Electron_mvaSpring16GP_WP80) >= 1'
            '    || Sum$(Muon_pt > 20 && Muon_tightId) >= 1'
            '    || (Sum$(Muon_pt > 20) == 0 && Sum$(Electron_pt > 20 && Electron_mvaSpring16GP_WP90) == 0 && MET_pt > 80))'
            '&& Sum$(abs(Jet_eta) < 2.5 && Jet_pt > 20 && Jet_jetId) >= 2'
        ),
        # The path to a text file describing which branches to keep and drop.
        branchsel='keep_and_drop.txt',
        # Additional postprocessing modules which add additional selections and branches.
        modules=[btagSFProducer('cmva'), jecUncertAll_cppOut(), vhbb()],
        # Preserve input file provenance information.
        provenance=True,
    )

    postprocessor.run()


if __name__ == '__main__':

    status = main()
    sys.exit(status)

