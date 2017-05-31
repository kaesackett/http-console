#!/usr/bin/env python

"""
A simple console program that monitors HTTP traffic
on a machine and provides some summative metrics.

Example Usage: python logwatch.py -f access.log -m 100
"""

import threading
import operator
import tailer # Available in PIP
import time
import os

from optparse import OptionParser

# Option Parser (provide filename to watch)
parser = OptionParser()
parser.add_option("-f", "--filename", dest="filename",
                  help="The filename of the log you'd like to monitor.")
parser.add_option("-m", "--max", type=int, dest="high_threshold",
                  help="The critical threshold at which to alert for high traffic volume.")
options, args = parser.parse_args()

class LogWatcher(object):
  """LogWatcher object definition."""

  def __init__(self, filename):
    super(LogWatcher, self).__init__()
    self.filename = filename
    self.stats = {}
    self.stats["ip"] = {}
    self.stats["method"] = {}
    self.stats["section"] = {}
    self.stats["protocol"] = {}
    self.stats["response"] = {}
    self.total = 0
    self.queue = []
    self.alert = False

  def watch_file(self):
    """Follow a logfile indefinitely."""

    for line in tailer.follow(open(self.filename)):
      self.process_line(line)
      self.queue.append(time.time())
      while time.time() - self.queue[0] > 119:
        self.queue.pop(0)

  def process_line(self, line):
    """Parse w3c-formatted log lines."""

    first, rest = line.split(']')

    # Parse all the things
    ip, _ident, _user, _date, _timestamp = first.split(" ")
    method, section, protocol = rest.split('"')[1].split()
    response = rest.lstrip().split(" ")[3]

    for metric, count in [("ip", ip), ("method", method), ("section", section), ("protocol", protocol), ("response", response)]:
      self.stats[metric][count] = self.stats[metric].get(count, 0) + 1
    self.total += 1

  def dump(self):
    """Output interesting summary statistics to the console."""

    print("USAGE STATS")

    # Total Requests
    print("Total Requests: {}".format(self.total))

    # Top IP and percent of total requests
    top_ip = sorted(self.stats["ip"].items(), key=operator.itemgetter(1), reverse=True)
    print("Top IP: {0} ({1}%)".format(top_ip[0][0], (top_ip[0][1] / self.total * 100)))

    # Most common request method
    most_common_request = sorted(self.stats["method"].items(), key=operator.itemgetter(1), reverse=True)
    print("Most Common Request: {}".format(most_common_request[0][0], (most_common_request[0][1] / self.total * 100)))

    # Raw number of GETs and POSTs
    print("GETs: {0} ({1}%)".format(self.stats["method"].get("GET", 0), self.stats["method"].get("GET", 0) / self.total * 100))
    print("POSTs: {0} ({1}%)".format(self.stats["method"].get("POST", 0), self.stats["method"].get("POST", 0) / self.total * 100))

    # Most frequently requested section
    most_frequent_section = sorted(self.stats["section"].items(), key=operator.itemgetter(1), reverse=True)
    print("Most Frequently Requested URI: {0} ({1}%)".format(most_frequent_section[0][0], (most_frequent_section[0][1] / self.total * 100)))

    if len(self.queue) > options.high_threshold:
      print("High traffic generated an alert - hits = {0}, triggered at{1}".format(len(self.queue), time.strftime('%l:%M%p %z on %b %d')))
      self.alert = True
    else:
      if self.alert:
        self.alert = False
        print("High traffic alert resolved at {}.".format(time.strftime('%l:%M%p %z on %b %d')))

def main():
  # Handle FNF exceptions
  try:
    file = open(options.filename, 'r')
    print("====== Watching logfile: {}... ======".format(options.filename))
  except IOError:
    print('There was an error opening the file! Check that the filename was correctly entered, that the file exists, and that its permissions are correct.')
    return

  lw = LogWatcher(options.filename)
  thread = threading.Thread(target=lw.watch_file)
  thread.start()

  # Console output every 10 seconds
  while True:
    time.sleep(10)
    os.system('clear')
    lw.dump()

if __name__ == "__main__":
  main()
