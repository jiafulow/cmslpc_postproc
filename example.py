import os

from cmslpc_postproc import PostProcessJobs


jobs = PostProcessJobs()

jobs.submit(
    tag='SingleMuon_Run2017C',
    src='root://cmseos.fnal.gov///store/group/lpchbb/NanoTestProd010/SingleMuon/Data-NanoCrabProd010/171128_160020/',
    dst='root://cmseos.fnal.gov///store/user/sjwang/NanoTestPostProc/SingleMuon/Data-NanoCrabProd010/Run2017C/',
    is_data=True,
    no_submit=True,
)

jobs.submit(
    tag='TT_powheg',
    src='root://cmseos.fnal.gov///store/group/lpchbb/NanoTestProd010/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer17MiniAOD-92X-NanoCrabProd010/171128_160136/',
    dst='root://cmseos.fnal.gov///store/user/sjwang/NanoTestPostProc/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/',
    commands={
        'x509userproxy': os.environ['X509_USER_PROXY'],
        # The maximum runtime in seconds.
        '+MaxRuntime': 3600,
    },
    no_submit=True,
)

