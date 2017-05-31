import operator
import os.path
import threading
import tailer # Available in PIP
import time

from optparse import OptionParser

# Option Parser (provide filename to watch)
parser = OptionParser()
parser.add_option("-f", "--filename", dest="filename",
                  help="The filename of the log you'd like to monitor.")
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

  def watch_file(self, filename):
    """Follow a logfile indefinitely."""

    for line in tailer.follow(filename):
      lw.process_line(line)

  def process_line(line):
    """Parse w3c-formatted log lines."""

    first, rest = line.split(']')

    # Parse all the things
    ip, _ident, _user, _date, _timestamp = first.split(" ")
    method, section, protocol = rest.split('"')[1].split()
    response = rest.lstrip().split(" ")[3]

    for metric, count in [("ip", ip), ("user", user), ("method", method), ("section", section), ("protocol", protocol), ("response", response)]:
      self.stats[metric][count] += self.stats[metric].get(count, 0) + 1
      # self.stats["method"][method] += self.stats["method"].get(method, 0) + 1
    self.total += 1

  def dump(self):
    """Output interesting summary statistics to the console."""

    print("Usage stats:")

    # Total Requests
    print(self.total)

    # Top IP and percent of total requests
    top_ip = sorted(stats["ip"].items(), key=operator.itemgetter(1), reverse=True)
    print("Top IP: {0} ({1}%)".format(top_ip[0], (stats["ip"][top_ip] / self.total * 100)))

    # Most common request method
    most_common_request = sorted(stats["method"].items(), key=operator.itemgetter(1), reverse=True)
    print("Most Common Request: {}".format(most_common_request[0]))

    # Raw number of GETs and POSTs
    print("GETs: {0} ({1}%)".format(stats["method"]["GET"]), (stats["method"]["GET"] / self.total * 100))
    print("POSTs: {0} ({1}%)".format(stats["method"]["POST"]), (stats["method"]["POST"] / self.total * 100))

    # Most frequently requested section
    most_frequent_section = sorted(stats["section"].items(), key=operator.itemgetter(1), reverse=True)
    print("Most Frequent Section: {0} ({1}%)".format(most_frequent_section[0], (stats["section"][most_frequent_section] / self.total * 100)))

    # TODO
    # Response codes spread
    # Total 2xx: 30 (30%)
    # Total 3xx: 30 (30%)
    # Total 4xx: 30 (30%)
    # Total 5xx: 20 (10%)

if __name__ == "__main__":
  # Handle FNF exceptions
  try:
    print("==== Watching logfile: {}... ====".format(options.filename))
  except IOError as err:
    # Fail spectacularly
    print(err.errno)
    print(err.strerror)

  lw = LogWatcher(options.filename)
  thread = threading.Thread(target=lw.watch_file, args=(options.filename,))
  thread.start()

  while True:
    time.sleep(20)
    lw.dump()