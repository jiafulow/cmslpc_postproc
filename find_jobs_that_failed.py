import os
import sys


if __name__ == '__main__':

  #if len(sys.argv) != 2:
  #  print "Usage: python %s %s" % (sys.argv[0], "DIR")
  #  exit(1)

  #directory = 'PostProcessDAGs/jftest1'
  #n = 200
  #fname = 'histos_tba_%i.npz'

  directory = 'PostProcessDAGs/jftest4'
  n = 164
  fname = 'histos_tbd_%i.npz'

  files = os.listdir(directory)
  select = lambda x: x.endswith('.npz')
  files = set(filter(select, files))

  print "Jobs that failed:"
  for i in xrange(n):
    if (fname % i) not in files:
      print (fname % i)
