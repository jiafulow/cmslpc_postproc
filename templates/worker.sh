#!/usr/bin/env bash

# Automatically generated on {{ timestamp }}

# The SCRAM architecture and CMSSW version of the submission environment.
readonly SUBMIT_SCRAM_ARCH="{{ environ['SCRAM_ARCH'] }}"
readonly SUBMIT_CMSSW_VERSION="{{ environ['CMSSW_VERSION'] }}"

# Capture the executable name and job input file from the command line.
readonly CONDOR_EXEC="$(basename $0)"
readonly INPUT_FILE="$1"
readonly OUTPUT_DIR="$2"

main() {
  echo "$(date) - $CONDOR_EXEC - INFO - Setting up $JOB_CMSSW_VERSION"

  # Setup the CMS software environment.
  export SCRAM_ARCH="$SUBMIT_SCRAM_ARCH"
  source /cvmfs/cms.cern.ch/cmsset_default.sh

  # Checkout the CMSSW release and set the runtime environment. These
  # commands are often invoked by their aliases "cmsrel" and "cmsenv".
  scram project CMSSW "$SUBMIT_CMSSW_VERSION"
  cd "$SUBMIT_CMSSW_VERSION/src"
  eval "$(scramv1 runtime -sh)"

  echo "$(date) - $CONDOR_EXEC - INFO - Setting up NanoAOD-tools"

  # Clone and compile the vhbb fork of NanoAOD-tools.
  git clone https://github.com/vhbb/nanoAOD-tools.git PhysicsTools/NanoAODTools
  scram b

  # Change back to the worker node's scratch directory.
  cd "$_CONDOR_SCRATCH_DIR"

  echo "$(date) - $CONDOR_EXEC - INFO - Postprocessing $INPUT_FILE"

  # Postprocess the input file.
  python postprocess.py "$INPUT_FILE"

  # Copy the output file to an EOS directory.
  local OUTPUT_FILE="$(basename $INPUT_FILE)"
  OUTPUT_FILE="${OUTPUT_FILE%.root}_Skim.root"
  xrdcp -NP "$OUTPUT_FILE" "$OUTPUT_DIR"
}
main

