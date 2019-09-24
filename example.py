import os

print 'Using CMSSW base: {0}'.format(os.environ['CMSSW_BASE'])

from core import PostProcessJobs

jobs = PostProcessJobs()

input_dir = '/home/jlow/nobackup/L1MuonTrigger/P2_CMSSW_10_6_3/src/L1TMuonSimulations/Analyzers/test7/'
input_files = [
    'rootpy_trackbuilding11.py', 'nn_*.py', 'pattern_bank_18patt.29.npz',
    'model.29.h5', 'model_weights.29.h5', 'model.29.json',
]
input_files = map(lambda x: os.path.join(input_dir, x), input_files)  # prepend input dir
cmssw_base = os.environ['CMSSW_BASE']
input_files += [cmssw_base]  # include CMSSW base
jobs.pack(input_files)

commands = {
    '+ProjectName': 'cms.org.ufl',
    '+REQUIRED_OS': '\"rhel7\"',
}

jobs.submit(
    tag='jftest1',
    src=range(100), # max: 100
    dst='',
    algo='default',
    analysis='roads',
    no_submit=True,
    commands=commands,
)

jobs.submit(
    tag='jftest2',
    src=range(80,168), # max: 168
    dst='',
    algo='default',
    analysis='rates',
    no_submit=True,
    commands=commands,
)

jobs.submit(
    tag='jftest3',
    src=range(0,3), # max: 3
    dst='',
    algo='default',
    analysis='effie',
    no_submit=True,
    commands=commands,
)

jobs.submit(
    tag='jftest4',
    src=range(228), # max: 228
    dst='',
    algo='default',
    analysis='mixing',
    no_submit=True,
    commands=commands,
)

jobs.submit(
    tag='jftest5',
    src=range(15), # max: 33
    dst='',
    algo='default',
    analysis='collusion',
    no_submit=True,
    commands=commands,
)

jobs.submit(
    tag='jftest6',
    src=range(100), # max: 100
    dst='',
    algo='default',
    analysis='augmentation',
    no_submit=True,
    commands=commands,
)

jobs.submit(
    tag='jftest2_140',
    src=range(60,125), # max: 125
    dst='',
    algo='default',
    analysis='rates140',
    no_submit=True,
    commands=commands,
)

jobs.submit(
    tag='jftest2_250',
    src=range(100,250), # max: 250
    dst='',
    algo='default',
    analysis='rates250',
    no_submit=True,
    commands=commands,
)

jobs.submit(
    tag='jftest2_300',
    src=range(100,250), # max: 250
    dst='',
    algo='default',
    analysis='rates300',
    no_submit=True,
    commands=commands,
)

jobs.submit(
    tag='jftest3_200',
    src=range(15,33), # max: 33
    dst='',
    algo='default',
    analysis='effie200',
    no_submit=True,
    commands=commands,
)

