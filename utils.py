import errno
import os
import re
import subprocess
import glob
import tarfile


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


XROOTD_URL_RE = re.compile(r'^(?P<redirector>root://[^/]+)//(?P<path>.*)$')


def parse_xrootd_url(url):
    """Return the redirector and path from an XRootD url."""
    match = XROOTD_URL_RE.match(url)
    return match.group('redirector'), match.group('path')


def xrdfs_makedirs(url):
    """Recursively create an xrdfs directory."""
    redirector, path = parse_xrootd_url(url)
    subprocess.check_call(['xrdfs', redirector, 'mkdir', '-p', path])


def xrdfs_isdir(url):
    """Return True if the url is a directory."""
    redirector, path = parse_xrootd_url(url)
    try:
        # Redirect stderr messages such as "[ERROR] Query response negative" to /dev/null.
        with open(os.devnull, 'w') as devnull:
            subprocess.check_output(['xrdfs', redirector, 'stat', '-q', 'IsDir', path], stderr=devnull)
    except subprocess.CalledProcessError as e:
        if e.returncode == 55:
            return False
        else:
            raise
    else:
        return True


def xrdfs_locate_root_files(url):
    """Recurse into a directory and return the urls of all ROOT files encountered.
    """
    redirector, path = parse_xrootd_url(url)
    urls = []
    output = subprocess.check_output(['xrdfs', redirector, 'ls', path]).splitlines()
    for path in output:
        url = '//'.join([redirector, path])
        if os.path.splitext(path)[1] == '.root':
            urls.append(url)
        elif xrdfs_isdir(url):
            urls.extend(xrdfs_locate_root_files(url))
    return urls

def pack_files(name='default.tgz', mode='w:gz', dereference=True, files=None, filter_func=None):
    """Add user files into a tarball
    """
    files = files or []
    with tarfile.open(name, mode, dereference=dereference) as tar:
        for globname in files:
            filenames = glob.glob(globname)
            if not filenames:
                raise Exception("The input file '%s' cannot be found." % globname)
            for filename in filenames:
                arcname = os.path.basename(filename)
                tar.add(filename, arcname, recursive=True, filter=filter_func)
    return
