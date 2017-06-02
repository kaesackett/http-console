# http-console
A simple console program that watches a given actively written-to w3c-formatted logfile and monitors HTTP traffic on a machine, alerts during periods of high volume, and provides some summative metrics.

### Example Usage
This program is designed to be run in console. Command-line options are passed for both the logfile to watch (<code>-f</code> or <code>--filename</code>) and the critical threshold at which to alert for high traffic volume (<code>-m</code> or <code>--max</code>):
<pre><code>python logwatch.py -f access.log -m 100</code></pre>

### Environment

1. Clone the repository:

<pre><code>$ git clone https://github.com/kaesackett/RoomEase.git</code></pre>

2. Create and activate a virtual environment in the same directory: 

<pre><code>$ pip install virtualenv
$ virtualenv env
$ source env/bin/activate 
</code></pre>

3. Install the required packages using pip:

<pre><code>(env)$ pip install -r requirements.txt</code></pre>

### Troubleshooting / Bugs / Known Issues
1. The script's current logic only <i>follows</i>, so unless the file you're trying to watch is actively growing, the stats dict is never populated (because it's populated only by new events as they occur, not events that already exist in the log). This will cause Python to throw a key error, as the stats dict has no keys.
2. "Threading with Python? What about the Global Interpreter Lock? Why would you do such a thing?" - Right, that's a thing. In this case, I've got one thread to collect and manipulate the metrics (so, just fancy counting), and another to spit them out at regular intervals. I'm not doing anything here that requires any kind of precision. Give me a break. I literally wrote this in like an hour and a half.

### Improvements:
#### Single-Process:
 - Add TTL to stats dict to expire old items
 - Either retire on new write
   or
 - Spawn a garbage collector thread to walk dict and cleanup

#### Service:
 - Use a real DB
 - Add a frontend (Web UI) that reads from DB

#### Completely different approach:
 - Instead of watching file, wrap logging method
