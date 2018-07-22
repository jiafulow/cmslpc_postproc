# Installation

This Python module assumes that nanoAOD-tools has been installed alongside a CMSSW version.
A more recent CMSSW version is required because the postprocessing framework relies on a
TTreeReader constructor introduced since ROOT version 6.10. In the steps that follow,
CMSSW_9_4_0_pre3 is used.

I should probably mention that the Jinja2 templating engine is also a dependency, but it
has been distributed by CMSSW for quite a while now so it should be present.

1. Setup CMSSW and the vhbb fork of nanoAOD-tools.

```bash
export SCRAM_ARCH="slc6_amd64_gcc630"
cmsrel CMSSW_9_4_0_pre3
cd CMSSW_9_4_0_pre3/src
git clone git@github.com:vhbb/nanoAOD-tools.git PhysicsTools/NanoAODTools
scram b
```

2. Clone the cmslpc_postproc repository.

```bash
git clone git@github.com:swang373/cmslpc_postproc.git
```

# Usage

The `cmslpc_postproc` module is **NOT** a proper Python package, so while it doesn't need
to be installed, it does need to reside in the same working directory as your job submission
scripts in order to be imported.

The `cmslpc_postproc` module introduces a class called `PostProcessJobs`, which serves as the
interface for submitting nanoAOD postprocessing jobs to the HTCondor batch system at the LPC.
No arguments need to be passed to its constructor, so an instance of the class can be created like so:

```python
import cmslpc_postproc

jobs = cmslpc_postproc.PostProcessJobs()
```

Now that you have an instance of the class, what does it do? It really only has one useful method named
`submit` which has two required arguments:

* `src` The XRootD url of the directory containing the input ntuples to postprocess. The url should have
appropriate depth, as all ROOT files recursively located below it are assumed to be related input files.
* `dst` The XRootD url of the output directory for the postprocessed ntuples. The caveat is that this
output directory is only created if the jobs are automatically submitted. We'll touch on this point later.

and a few optional arguments:

* `tag` A name for the directory containing the automatically generated job submission files. The default
is the current timestamp in a CRAB3-esque format. The tag is very important not just for bookkeeping purposes,
but also for taking advantage of the way jobs are submitted, which is also touched on later.
* `is_data` A flag for whether the input ntuples are data or Monte-Carlo. The default is False for Monte-Carlo.
Because additional modules are needed when postprocesing Monte-Carlo ntuples, the job submission file generator
needs to know whether to include those additonal modules in the postprocessing script.
* `commands` A dictionary of HTCondor custom commands. The default is an empty dictionary for no custom commands.
The automatic job submission takes care of the usual commands such as `arguments`, `executable`, `log`, and more as
detailed in the docstring of the method. However, other commands such as `require_memory`, `+JobFlavour`, and `x509userproxy`
depend on the use case and should be left to the user's discretion.
* `no_submit` A flag for whether the jobs should be submitted immediately or only the job files need to be generated.
The default is False to submit jobs immediately upon their generation. This is useful for manual debugging the generated
job files, akin to typical "dry-run" submission options. Moreover, advanced users may find this option intriguing 
because it gives them a chance to modify the job submission files as they see fit before submitting the jobs.

Calling the `submit` method roughly sets into motion the following:
1. The directories containing the job submission files are created locally in the current working directory.
The top level directory will always be called `PostProcessDAGs/`, inside of which the directory specific to
individual job submissions are named according to the tag argument passed to the submit method.
2. The job context is created, which is a dictionary that collects the current timestamp, the resolved urls of all
input ROOT files, the destination url for the output ROOT files, whether the ntuples are data or Monte-Carlo, and
any custom HTCondor commands.
3. The job context is used to generate the following job submission files:
   * `dag` The HTCondor DAGMan input file, describing each node of the directed acyclic graph representing the job.
   * `node` The submit description file for each node. Most users of HTCondor will be familiar with the contents of this file.
   * `worker.sh` The executable used by each node. This script essentially prepares the CMSSW environment, installs
nanoAOD-tools, and runs the postprocessing script on the remote execution host.
   * `postprocess.py` The postprocessing script, which sets up and runs the VHbb postprocessing modules.
   * `keep_and_drop.txt` A text file describing which branches to keep and drop during postprocessing.
4. The output directory is created and the jobs are submitted. If the argument `no_submit` is True, then the jobs are not
submitted and the user is merely informed that the job submission files have been generated. It will be up to the user
to submit the jobs manually.

There is an example job submission script in the repository called `example.py`. You probably shouldn't run it since it
points to my CMS LPC EOS space, but let's step through one of the examples within.

```python
jobs.submit(
    tag='SingleMuon_Run2017C',
    src='root://cmseos.fnal.gov///store/group/lpchbb/NanoTestProd010/SingleMuon/Data-NanoCrabProd010/171128_160020/',
    dst='root://cmseos.fnal.gov///store/user/sjwang/NanoTestPostProc/SingleMuon/Data-NanoCrabProd010/Run2017C/',
    is_data=True,
    no_submit=True,
)
```

The above submits postprocessing jobs for each of the ROOT files located under the url passed to the `src` argument. The postprocessed output files will be copied to the directory url passed to the `dst` argument. The `is_data` argument is set to True because the ntuples to postprocess are data and not MC, and `no_submit` is True because it makes the example less trivial for a teachable moment.

If you run the above call to `submit`, you'll find a new `PostProcessDAGs/` directory in your current working directory. Inside that directory will be subdirectory named `SingleMuon_Run2017C/`, which you'll recognize as the string passed to the `tag` argument. Inside of that directory, you'll see the following files: `dag`, `node`, `worker.sh`, `postprocess.py`, and `keep_and_drop.txt`. Feel free to poke inside of them to see what's going on. If you want to customize the postprocessing behaviour, you'll want to modify either `postprocess.py` and/or `keep_and_drop.txt`. If you want to modify job submission behaviour, you may want to modify `dag`, `node`, and/or `worker.sh`.

I'll describe the HTCondor-related files in brief. The commands in `dag` are used by the DAGMan metascheduler to submit jobs for each of its nodes. Because it's a metascheduler, we enjoy such amenities as automatic job retry upon failure of a node (hardcoded to twice for now) and a fallback in case jobs totally fail even after retrying. The commands in `node` actually describe the job to the scheduler. There's only one node file because every node is doing the exact same job, with small variations based on the input file url. Also, we see in `node` that the stdout and stderr are piped to output files which can be found inside the log directory within the job submission directory (in so few words, `PostProcessDAGs/SingleMuon_Run2017C/logs/`).

Great, so now we have a bunch of files but how should we submit them? Wait, not so fast! Because the `no_submit` argument was set to True, the output directory was not created. First, manually create the output directory:

```bash
xrdfs root://cmseos.fnal.gov mkdir -p /store/user/sjwang/NanoTestPostProc/SingleMuon/Data-NanoCrabProd010/Run2017C/
```

and then submit the DAG using the following command:

```bash
condor_submit_dag -usedagdir -maxjobs 250 PostProcessDAGs/SingleMuon_Run2017C/dag
```

The above command submits the `dag` file to DAGMan with two stipulations:
* Use the parent directory of the `dag` file as the submission directory. Recall that, for this example, all of the job submission files reside in `PostProcessDAGs/SingleMuon_Run2017C/`. Because the job commands reference other job files such as `node` and `worker.sh` but the submission directory is treated as the current working directory by DAGMan, the submission will fail because it can't find those files other than `dag` itself. The `-usedagdir` option allows you to submit the job from any directory.
* Only 250 jobs can run concurrently. Under the current design, each node only postprocesses a single file. But a dataset may consist of hundreds or even thousands of files, resulting in an equivalent number of nodes or postprocessing jobs. Postprocessing multiple datasets and Monte-Carlo samples would likely result in tens of thousands of jobs. And while there are tons of resources at the LPC, it's not very nice or good to haphazardly flood the batch system like that (at least, I suppose so). The `-maxjobs` option allows us to set a limit on the number of concurrently running jobs. All of the jobs will be queued, but at most `-maxjobs` will be running at any given time. The 250 running jobs limit is imposed when submitting jobs automatically, but feel free to tweak it when submitting manually.

Once the DAG is running, you'll see new files pop up within `PostProcessDAGs/SingleMuon_Run2017C/`. They're all useful, but I usually poke around the following:

* `dag.dagman.out` The DAG status reports as it is running. I usually look for the following summary:
```
12/03/17 23:22:06 DAG status: 0 (DAG_STATUS_OK)
12/03/17 23:22:06 Of 1 nodes total:
12/03/17 23:22:06  Done     Pre   Queued    Post   Ready   Un-Ready   Failed
12/03/17 23:22:06   ===     ===      ===     ===     ===        ===      ===
12/03/17 23:22:06     1       0        0       0       0          0        0
12/03/17 23:22:06 0 job proc(s) currently held
```
* `dag.metrics` A JSON formatted report of the DAG. The keys `jobs`, `jobs_failed`, and `jobs_succeeded` give a good indication of whether something went wrong.

If things went horribly wrong and some jobs failed, you'll also find a rescue DAG file named something like `dag.rescue001` (the postfix number is tracked). The rescue DAG keeps track of which jobs succeeded and failed to determine whether they should not or should be resubmitted, respectively. This gives you a chance to debug the failed jobs, hopefully fix things, and then resubmit only those failed jobs. Submitting a rescue DAG uses the same command as submitting the original DAG, since DAGMan will automatically discover the appropriate rescue DAG. And then if things go horribly wrong again, you'll wind up iterating the previous step with `dag.rescue002`, and so on and so forth. If you want to override the rescue DAG and submit the original DAG, use the `-f` option in the original command like so:

```bash
condor_submit_dag -f -usedagdir -maxjobs 250 PostProcessDAGs/SingleMuon_Run2017C/dag
```

Remember how explicit tags were mentioned to be important for how jobs are submitted? When no `tag` argument is specified, repeatedly calling the `submit` method with the same arguments creates a new job submission directory and job submission files each time. However, if a `tag` argument is provided and a matching DAG input file already exists for that tag, then the job submission files are reused and not overwritten. This is a quality of life consideration for large job submission scripts that make lots of calls to the `submit` method.
