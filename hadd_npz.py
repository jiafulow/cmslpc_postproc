import numpy as np
import os


class Hadd(object):

  def __init__(self):
    self.d = {}
    self.dout = {}

  def process(self, target, source, force=False):
    print('hadd Target file: {0}'.format(target))

    if not force:
      if os.path.isfile(target):
        print('hadd error opening target file (does {0} exist?).'.format(target))
        print('Pass "-f" argument to force re-creation of output file.')

    for i, s in enumerate(source):
      print('hadd Source file {0}: {1}'.format(i+1, s))
      with np.load(s) as data:
        if i == 0:
          for k in data.files:
            self.d[k] = []
        for k in data.files:
          self.d[k].append(data[k])
          
    print('hadding...')
    for k, v in self.d.iteritems():
      vv = np.vstack(v)
      self.dout[k] = vv

    np.savez_compressed(target, **self.dout)
    print('DONE')


if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser(description='hadd for npz files.')
  parser.add_argument('-f', '--force', action='store_true', help='Force write the target file')
  parser.add_argument('target', help='target file')
  parser.add_argument('source', nargs='+', help='source files')
  args = parser.parse_args()

  hadd = Hadd()
  hadd.process(args.target, args.source, force=args.force)
