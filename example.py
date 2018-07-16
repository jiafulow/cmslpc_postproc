import os

from core import PostProcessJobs


jobs = PostProcessJobs()


input_dir = '/home/jlow/L1MuonTrigger/P2_CMSSW_10_1_5/src/L1TMuonSimulations/Analyzers/test7/'
input_files = ['rootpy_trackbuilding5.py', 'encoder.py', 'histos_tb.14.npz', 'model.14.h5', 'model_weights.14.h5', 'model.14.json']
prepend_input_dir = lambda x: os.path.join(input_dir, x)
jobs.pack(map(prepend_input_dir, input_files))

jobs.submit(
    tag='jftest1',
    src=range(200), # max: 200
    dst='',
    analysis='application',
    no_submit=True,
    commands={
        '+ProjectName': 'cms.org.ufl',
    },
)

jobs.submit(
    tag='jftest2',
    src=range(33), # max: 63
    dst='',
    analysis='rates',
    no_submit=True,
    commands={
        '+ProjectName': 'cms.org.ufl',
    },
)

jobs.submit(
    tag='jftest3',
    src=range(30), # max: 200
    dst='',
    analysis='effie',
    no_submit=True,
    commands={
        '+ProjectName': 'cms.org.ufl',
    },
)

jobs.submit(
    tag='jftest4',
    src=range(63), # max: 63
    dst='',
    analysis='mixing',
    no_submit=True,
    commands={
        '+ProjectName': 'cms.org.ufl',
    },
)

