#!/usr/bin/env bash

# Automatically generated on {{ timestamp }}

# The SCRAM architecture and CMSSW version of the submission environment.
readonly SUBMIT_SCRAM_ARCH="{{ environ['SCRAM_ARCH'] }}"
readonly SUBMIT_CMSSW_VERSION="{{ environ['CMSSW_VERSION'] }}"

# Capture the executable name and job input file from the command line.
readonly CONDOR_EXEC="$(basename $0)"
export CONDOR_EXEC
readonly TARBALL="default.tgz"
readonly ANALYSIS="$1"
readonly JOBID="$2"

main() {
  echo "$(date) - $CONDOR_EXEC - INFO - Setting up $SUBMIT_CMSSW_VERSION"

  # Setup the CMS software environment.
  export SCRAM_ARCH="$SUBMIT_SCRAM_ARCH"
  source /cvmfs/cms.cern.ch/cmsset_default.sh

  # Checkout the CMSSW release and set the runtime environment. These
  # commands are often invoked by their aliases "cmsrel" and "cmsenv".
  scram project CMSSW "$SUBMIT_CMSSW_VERSION"
  cd "$SUBMIT_CMSSW_VERSION/src"
  eval "$(scramv1 runtime -sh)"

  # Change back to the worker node's scratch directory.
  cd "$_CONDOR_SCRATCH_DIR"

  echo "$(date) - $CONDOR_EXEC - INFO - Unpacking files"
  tar xzf $TARBALL

  echo "$(date) - $CONDOR_EXEC - INFO - args: $ANALYSIS $JOBID"

  echo "$(date) - $CONDOR_EXEC - INFO - pwd: $PWD"

  echo "$(date) - $CONDOR_EXEC - INFO - ls"
  ls -l

  echo "$(date) - $CONDOR_EXEC - INFO - stand back I'm going to try Science"

  python rootpy_trackbuilding3.py $ANALYSIS $JOBID
  [ -f histos_tbb.root ] && mv histos_tbb.root histos_tbb_$JOBID.root
  [ -f histos_tbc.root ] && mv histos_tbc.root histos_tbc_$JOBID.root

  echo "$(date) - $CONDOR_EXEC - INFO - cleanup"
  tar tzf $TARBALL | xargs rm -rf
  rm $TARBALL

  echo "$(date) - $CONDOR_EXEC - INFO - ls"
  ls -l

  echo "$(date) - $CONDOR_EXEC - INFO - Science complete!"
  exit 0
}
main

