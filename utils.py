import errno
import os
import subprocess


def safe_makedirs(path):
    """Recursively create a directory without race conditions.
    This borrows from solutions to these Stack Overflow questions:
        * http://stackoverflow.com/a/5032238
        * http://stackoverflow.com/a/600612
    Parameters
    ----------
    path : path
        The path of the created directory.
    """
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def eos_makedirs(path):
    """Recursively create an EOS directory."""
    subprocess.check_call(['xrdfs', 'root://cmseos.fnal.gov', 'mkdir', '-p', path])


def eos_isdir(path):
    """Return true if the path is an EOS directory."""
    try:
        # Redirect stderr messages such as "[ERROR] Query response negative" to /dev/null.
        with open(os.devnull, 'w') as devnull:
            subprocess.check_output(['xrdfs', 'root://cmseos.fnal.gov', 'stat', '-q', 'IsDir', path], stderr=devnull)
    except subprocess.CalledProcessError as e:
        if e.returncode == 55:
            return False
        else:
            raise
    else:
        return True


def eos_locate_root_files(path):
    """Recurse into an EOS directory hosted at CMS LPC
    and return the paths of all ROOT files encountered.
    """
    root_files = []
    output = subprocess.check_output(['xrdfs', 'root://cmseos.fnal.gov', 'ls', path]).splitlines()
    for path in output:
        if os.path.splitext(path)[1] == '.root':
            root_files.append(path)
        elif eos_isdir(path):
            root_files.extend(eos_locate_root_files(path))
    return root_files

