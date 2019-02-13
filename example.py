import os

print 'Using CMSSW base: {0}'.format(os.environ['CMSSW_BASE'])

from core import PostProcessJobs

jobs = PostProcessJobs()


input_dir = '/home/jlow/L1MuonTrigger/P2_CMSSW_10_4_0/src/L1TMuonSimulations/Analyzers/test7/'
input_files = ['rootpy_trackbuilding8.py', 'nn_*.py', 'pattern_bank_omtf.23.npz', 'model.23.h5', 'model_weights.23.h5', 'model.23.json', 'model_omtf.23.h5', 'model_omtf_weights.23.h5', 'model_omtf.23.json']
input_files = map(lambda x: os.path.join(input_dir, x), input_files)  # prepend input dir
cmssw_base = os.environ['CMSSW_BASE']
input_files += [cmssw_base]  # include CMSSW base
jobs.pack(input_files)

jobs.submit(
    tag='jftest1',
    src=range(100), # max: 100
    dst='',
    analysis='roads',
    no_submit=True,
    commands={
        '+ProjectName': 'cms.org.ufl',
    },
)

jobs.submit(
    tag='jftest2',
    src=range(30,63), # max: 63
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
    src=range(192), # max: 192
    dst='',
    analysis='mixing',
    no_submit=True,
    commands={
        '+ProjectName': 'cms.org.ufl',
    },
)

