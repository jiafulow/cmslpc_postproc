# Requirements

You need to have the CMS Connect account, and install the Connect client locally. See:

- <https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCMSConnect>

In particular:

- <https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCMSConnect#Option_2_Installing_the_client_l>

# Installation

1. Check out the repository

``` sh
mkdir PostProcessJobs
cd PostProcessJobs
git clone -b jftest git@github.com:jiafulow/cmslpc_postproc.git 
ln -s cmslpc_postproc/example.py
```

2. Create CMSSW area

``` sh
export SCRAM_ARCH=slc6_amd64_gcc630
source /cvmfs/cms.cern.ch/cmsset_default.sh

cmsrel CMSSW_9_3_11
cd CMSSW_9_3_11/src
cmsenv
cd -

source ~/software/connect-client/client_source.sh
```

# Usage

1. Setup environments

``` sh
cd CMSSW_9_3_11/src
cmsenv
cd -

source ~/software/connect-client/client_source.sh
```

2. Submit a job (for example)

``` sh
# Modify example.py as necessary
python example.py

cd PostProcessDAGs/jftest1
connect submit node
cd -
```

3. Check job queue

``` sh
connect q
```

4. Retrieve outputs

```sh
cd PostProcessDAGs/jftest1
connect pull
cd -

```
