import terminaltables
import operator
import os.path
import thread
import tailer # Available in PIP
import time

from optparse import OptionParser

# Option Parser (provide filename to watch)
parser = OptionParser()
parser.add_option("-f", "--logfile", dest="filename",
                  help="The filename of the log you'd like to monitor.")
options, args = parser.parse_args()


class LogWatcher(object):
  """TODO"""

  def __init__(self, filename):
    super(LogWatcher, self).__init__()
    self.filename = filename
    self.stats = {}
    self.stats["method"] = {}
    # ....
    self.total = 0

  def watchFile(self, filename):
    """Follow a logfile indefinitely."""

    for line in tailer.follow(filename)
      lw.processLine(line)

  def processLine(line):
    """Parse w3c-formatted log lines."""

    first, rest = line.split(']')

    # Parse all the things
    method, addr, proto = rest.split('"')[1].split()
    for metric, count in [("method", method), ("addr", addr), ...]
      self.stats[metric][count] += self.stats[metric].get(count, 0) + 1
      # self.stats["method"][method] += self.stats["method"].get(method, 0) + 1
    self.total += 1

  def dump(self):
    """Output interesting summary statistics to the console."""

    print "Usage stats:"
    topIPs = sorted(stats.["ip"].items(),
                   key=operator.itemgetter(1),
                   reverse=True)
    print "Top IP:{}".format(topIPs[0])
    # ...
    # Total: 110
    # Top IP: 1.2.3.4 (50%)
    # GETs: 50 (45%)
    # POSTs: 60 (55%)
    # Top Address: "/status" (30%)
    # Total 2xx: 30 (30%)
    # Total 3xx: 30 (30%)
    # Total 4xx: 30 (30%)
    # Total 5xx: 20 (10%)

def main():
  # Parse filename
  if not os.path.exists(filename):
    # Fail spectacularly
    pass

  lw = LogWatcher(filename)
  thread.start_new_thread(lw.watchFile, ())
  while True:
    time.sleep(20)
    lw.dump()
