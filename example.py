import os

print 'Using CMSSW base: {0}'.format(os.environ['CMSSW_BASE'])

from core import PostProcessJobs

jobs = PostProcessJobs()

input_dir = '/home/jlow/L1MuonTrigger/P2_CMSSW_10_4_0/src/L1TMuonSimulations/Analyzers/test7/'
input_files = ['rootpy_trackbuilding8.py', 'nn_*.py', 'pattern_bank_omtf.25.npz', 'model.25.h5', 'model_weights.25.h5', 'model.25.json', 'model_omtf.25.h5', 'model_omtf_weights.25.h5', 'model_omtf.25.json']
input_files = map(lambda x: os.path.join(input_dir, x), input_files)  # prepend input dir
cmssw_base = os.environ['CMSSW_BASE']
input_files += [cmssw_base]  # include CMSSW base
jobs.pack(input_files)

jobs.submit(
    tag='jftest1',
    src=range(100), # max: 100
    dst='',
    algo='default',
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
    algo='default',
    analysis='rates',
    no_submit=True,
    commands={
        '+ProjectName': 'cms.org.ufl',
    },
)

jobs.submit(
    tag='jftest3',
    src=range(30), # max: 100
    dst='',
    algo='default',
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
    algo='default',
    analysis='mixing',
    no_submit=True,
    commands={
        '+ProjectName': 'cms.org.ufl',
    },
)

jobs.submit(
    tag='jftest11',
    src=range(50), # max: 50
    dst='',
    algo='omtf',
    analysis='roads',
    no_submit=True,
    commands={
        '+ProjectName': 'cms.org.ufl',
    },
)

jobs.submit(
    tag='jftest13',
    src=range(20), # max: 50
    dst='',
    algo='omtf',
    analysis='effie',
    no_submit=True,
    commands={
        '+ProjectName': 'cms.org.ufl',
    },
)

jobs.submit(
    tag='jftest14',
    src=range(192), # max: 192
    dst='',
    algo='omtf',
    analysis='mixing',
    no_submit=True,
    commands={
        '+ProjectName': 'cms.org.ufl',
    },
)

jobs.submit(
    tag='jftest21',
    src=range(100), # max: 100
    dst='',
    algo='run3',
    analysis='roads',
    no_submit=True,
    commands={
        '+ProjectName': 'cms.org.ufl',
    },
)

jobs.submit(
    tag='jftest22',
    src=range(30,63), # max: 63
    dst='',
    algo='run3',
    analysis='rates',
    no_submit=True,
    commands={
        '+ProjectName': 'cms.org.ufl',
    },
)

jobs.submit(
    tag='jftest23',
    src=range(30), # max: 100
    dst='',
    algo='run3',
    analysis='effie',
    no_submit=True,
    commands={
        '+ProjectName': 'cms.org.ufl',
    },
)

jobs.submit(
    tag='jftest24',
    src=range(192), # max: 192
    dst='',
    algo='run3',
    analysis='mixing',
    no_submit=True,
    commands={
        '+ProjectName': 'cms.org.ufl',
    },
)

jobs.submit(
    tag='jftest2_140',
    src=range(20,56), # max: 56
    dst='',
    algo='default',
    analysis='rates140',
    no_submit=True,
    commands={
        '+ProjectName': 'cms.org.ufl',
    },
)

jobs.submit(
    tag='jftest2_250',
    src=range(50), # max: 50
    dst='',
    algo='default',
    analysis='rates250',
    no_submit=True,
    commands={
        '+ProjectName': 'cms.org.ufl',
    },
)

jobs.submit(
    tag='jftest2_300',
    src=range(53), # max: 53
    dst='',
    algo='default',
    analysis='rates300',
    no_submit=True,
    commands={
        '+ProjectName': 'cms.org.ufl',
    },
)

