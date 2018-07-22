#export SCRAM_ARCH=slc6_amd64_gcc630
#source /cvmfs/cms.cern.ch/cmsset_default.sh

cd CMSSW_9_3_11/src
cmsenv
cd -

source ~/software/connect-client/client_source.sh

alias connsetup='connect setup --replace-keys jiafulow@login.uscms.org'
alias connnode='connect submit node'

#connect shell
#export HOME=/home/$USER
#voms-proxy-init -voms cms -valid 192:00
#exit

