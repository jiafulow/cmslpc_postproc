import os

print 'Using CMSSW base: {0}'.format(os.environ['CMSSW_BASE'])

from core import PostProcessJobs

jobs = PostProcessJobs()

input_dir = '/home/jlow/L1MuonTrigger/P2_CMSSW_10_4_0/src/L1TMuonSimulations/Analyzers/test7/'
input_files = [
    'rootpy_trackbuilding9.py', 'nn_*.py', 'pattern_bank_18patt.27.npz',
    'model.27.h5', 'model_weights.27.h5', 'model.27.json',
    'model_omtf.27.h5', 'model_omtf_weights.27.h5', 'model_omtf.27.json',
    'model_run3.27.h5', 'model_run3_weights.27.h5', 'model_run3.27.json',
]
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
    src=range(0,30), # max: 100
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
    tag='jftest5',
    src=range(26), # max: 26
    dst='',
    algo='default',
    analysis='collusion',
    no_submit=True,
    commands={
        '+ProjectName': 'cms.org.ufl',
    },
)

jobs.submit(
    tag='jftest6',
    src=range(30,100), # max: 100
    dst='',
    algo='default',
    analysis='augmentation',
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
    src=range(0,20), # max: 50
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
    tag='jftest15',
    src=range(26), # max: 26
    dst='',
    algo='omtf',
    analysis='collusion',
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
    src=range(0,30), # max: 100
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
    tag='jftest25',
    src=range(26), # max: 26
    dst='',
    algo='run3',
    analysis='collusion',
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

