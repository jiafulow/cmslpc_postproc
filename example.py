import os

from core import PostProcessJobs


jobs = PostProcessJobs()


input_dir = '/home/jlow/L1MuonTrigger/P2_CMSSW_9_2_3_patch1/src/L1TMuonSimulations/Analyzers/test2/'
input_files = ['rootpy_trackbuilding4.py', 'encoder.py', 'histos_tb.12.npz', 'model.12.h5', 'model_weights.12.h5', 'model.12.json', 'model_discr.12.h5', 'model_discr_weights.12.h5', 'model_discr.12.json']
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
    src=range(40), # max: 100
    dst='',
    analysis='rates',
    no_submit=True,
    commands={
        '+ProjectName': 'cms.org.ufl',
    },
)

jobs.submit(
    tag='jftest3',
    src=range(40), # max: 800
    dst='',
    analysis='effie',
    no_submit=True,
    commands={
        '+ProjectName': 'cms.org.ufl',
    },
)

jobs.submit(
    tag='jftest4',
    src=range(100), # max: 100
    dst='',
    analysis='mixing',
    no_submit=True,
    commands={
        '+ProjectName': 'cms.org.ufl',
    },
)

