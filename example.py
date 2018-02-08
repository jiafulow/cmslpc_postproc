import os

from core import PostProcessJobs


jobs = PostProcessJobs()


input_dir = '/home/jlow/L1MuonTrigger/P2_CMSSW_9_2_3_patch1/src/L1TMuonSimulations/Analyzers/test2/'
input_files = ['rootpy_trackbuilding3.py', 'histos_tb.8.npz', 'encoder.8.npz', 'model.8.h5', 'model_weights.8.h5', 'bpca.8.npz']
prepend_input_dir = lambda x: os.path.join(input_dir, x)
jobs.pack(map(prepend_input_dir, input_files))

jobs.submit(
    tag='jftest1',
    src=range(10),
    dst='',
    analysis='rates',
    no_submit=True,
    commands={
        '+ProjectName': 'cms.org.ufl',
    },
)

jobs.submit(
    tag='jftest2',
    src=range(10),
    dst='',
    analysis='effie',
    no_submit=True,
    commands={
        '+ProjectName': 'cms.org.ufl',
    },
)

