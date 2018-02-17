import os

from core import PostProcessJobs


jobs = PostProcessJobs()


input_dir = '/home/jlow/L1MuonTrigger/P2_CMSSW_9_2_3_patch1/src/L1TMuonSimulations/Analyzers/test2/'
input_files = ['rootpy_trackbuilding3.py', 'histos_tb.10.npz', 'chsq.10.npz', 'model.10.h5', 'model_weights.10.h5']
#input_files = ['rootpy_trackbuilding3_2GeV.py', 'histos_tb.10.npz', 'chsq_2GeV.10.npz', 'model_2GeV.10.h5', 'model_weights_2GeV.10.h5']
prepend_input_dir = lambda x: os.path.join(input_dir, x)
jobs.pack(map(prepend_input_dir, input_files))

jobs.submit(
    tag='jftest1',
    src=range(30),
    dst='',
    analysis='rates',
    no_submit=True,
    commands={
        '+ProjectName': 'cms.org.ufl',
    },
)

jobs.submit(
    tag='jftest2',
    src=range(20),
    dst='',
    analysis='effie',
    no_submit=True,
    commands={
        '+ProjectName': 'cms.org.ufl',
    },
)

