import os
import shutil
import subprocess
import time

import jinja2

import utils


TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))


class PostProcessJobs(object):
    """An interface for submitting nanoAOD-tools postprocessing jobs to HTCondor.
    """
    def __init__(self, datatype=None):
        self.datatype ='mc' if datatype is None else datatype
        self._templates = jinja2.Environment(
            loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
            trim_blocks=True,
        )

    def submit(self, src, dst, tag=None, is_data=False, commands={}, no_submit=False):
        """Submit postprocessing jobs to HTCondor's DAGMan.

        DAGMan jobs can be retried automatically and should jobs fail, users can
        take advantage of the automatically generated rescue DAG for resubmitting
        only failed jobs.

        For more information, see the DAGMan documentation at
        http://research.cs.wisc.edu/htcondor/manual/latest/2_10DAGMan_Applications.html

        Parameters
        ----------
        src : url
            The XRootD url of the directory containing the ntuples to postprocess.
            Any .root files are automatically located by recursing through subdirectories.
        dst : url
            The XRootD url of the output directory for the postprocessed ntuples.
            The directory will only be created if jobs are submitted.
        tag : str, optional
            The name of the parent directory for the generated job submission
            files. The default is the current timestamp.
        is_data : bool, optional
            Whether the ntuples are data or Monte-Carlo. This determines the
            postprocessing modules in the postprocessing template script.
            The default is False for Monte-Carlo.
        commands : dict, optional
            HTCondor commands to include in the submit description file, in addition to the
            following which are handled automatically:
                * arguments
                * error
                * executable
                * getenv
                * log
                * output
                * queue
                * should_transfer_files
                * transfer_input_files
                * transfer_output_files
                * universe
            The default is no additional commands.
        no_submit : bool, optional
            If True, the job submission files are generated but not submitted
            to the HTCondor scheduler. The default is False.
        """
        # Create the directory tree for the job submission files.
        if not tag:
            tag = time.strftime('%Y%m%d_%H%M%S')
        dagdir = os.path.join(os.getcwd(), 'PostProcessDAGs', tag)
        logdir = os.path.join(dagdir, 'logs')
        utils.safe_makedirs(logdir)
        # Generate the job submission files.
        context = {
            'timestamp': time.strftime('%a %b %d %H:%M:%S %Z %Y'),
            'environ': os.environ,
            'urls': utils.xrdfs_locate_root_files(src),
            'destination': dst,
            'is_data': is_data,
            'commands': commands,
        }
        dag_path = os.path.join(dagdir, 'dag')
        self._generate_from_template('dag_input_file', dag_path, context)
        self._generate_from_template('node_submit_description', os.path.join(dagdir, 'node'), context)
        self._generate_from_template('worker.sh', os.path.join(dagdir, 'worker.sh'), context)
        self._generate_from_template('postprocess.py', os.path.join(dagdir, 'postprocess.py'), context)
        shutil.copy(os.path.join(TEMPLATE_DIR, 'keep_and_drop.txt'), dagdir)
        # Unless otherwise directed, submit the DAG input file to DAGMan.
        if no_submit:
            print 'HTCondor DAG input file generated but not submitted: {0}'.format(dag_path)
        else:
            utils.xrdfs_makedirs(dst)
            subprocess.check_call(['condor_submit_dag', '-usedagdir', dag_path, '-maxjobs', '250'])

    def _generate_from_template(self, name, path, context):
        """Generate a job submission file by rendering its template.
        Each job submission file has a corresponding template with variables
        that are rendered using the job submission arguments and environment.

        Parameters
        ----------
        name : str
            The name of the template. The available templates are:
                * dag_input_file
                * node_submit_description
                * worker.sh
        path : path
            The output file path.
        context : dict
            The mapping between job submission arguments and environment
            variables to the names of their corresponding template variables.
        """
        template = self._templates.get_template(name)
        with open(path, 'w') as f:
            f.write(template.render(context))

