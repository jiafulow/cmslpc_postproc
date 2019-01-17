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


echo "$(date) - $CONDOR_EXEC - INFO - home: $HOME"
echo "$(date) - $CONDOR_EXEC - INFO - condor_scratch: $_CONDOR_SCRATCH_DIR"
echo "$(date) - $CONDOR_EXEC - INFO - pwd: $PWD"
echo "$(date) - $CONDOR_EXEC - INFO - args: $ANALYSIS $JOBID"

echo "$(date) - $CONDOR_EXEC - INFO - Unpacking files"
tar xzf $TARBALL

echo "$(date) - $CONDOR_EXEC - INFO - Setting up $SUBMIT_CMSSW_VERSION"

# Setup the CMS software environment.
export SCRAM_ARCH="$SUBMIT_SCRAM_ARCH"
source /cvmfs/cms.cern.ch/cmsset_default.sh

# Checkout the CMSSW release and set the runtime environment. These
# commands are often invoked by their aliases "cmsrel" and "cmsenv".
#scram project CMSSW "$SUBMIT_CMSSW_VERSION"
cd "$SUBMIT_CMSSW_VERSION/src"
eval "$(scramv1 runtime -sh)"

echo "$(date) - $CONDOR_EXEC - INFO - Setting up virtualenv"
source venv/bin/activate

# Change back to the worker node's scratch directory.
cd "$_CONDOR_SCRATCH_DIR"

echo "$(date) - $CONDOR_EXEC - INFO - pwd: $PWD"

echo "$(date) - $CONDOR_EXEC - INFO - ls: -"
ls -l

# Do Science
echo "$(date) - $CONDOR_EXEC - INFO - Stand back I'm going to try Science!"

python rootpy_trackbuilding7.py $ANALYSIS $JOBID

EXIT_STATUS=$?
ERROR_TYPE=""
ERROR_MESSAGE="This is an error message."

if [ $EXIT_STATUS -ne 0 ]; then
  echo "$(date) - $CONDOR_EXEC - ERROR - Job has failed!"
  # Write report
  cat << EOF > FrameworkJobReport.xml
<FrameworkJobReport>
<FrameworkError ExitStatus="$EXIT_STATUS" Type="$ERROR_TYPE" >
$ERROR_MESSAGE
</FrameworkError>
</FrameworkJobReport>
EOF
fi

echo "$(date) - $CONDOR_EXEC - INFO - Postprocessing"

# Clean up
tar tzf $TARBALL | xargs rm -rf
rm -rf $TARBALL
rm -rf *.pyc

echo "$(date) - $CONDOR_EXEC - INFO - ls: -"
ls -l

exit $EXIT_STATUS
