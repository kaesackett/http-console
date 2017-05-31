# http-console
A simple console program that monitors HTTP traffic on your machine.

## Improvements:
### Single-Process:
 - Add TTL to stats dict to expire old items
 - Either retire on new write
   or
 - Spawn a garbage collector thread to walk dict and cleanup

### Service:
 - Use a real DB
 - Add a frontend (Web UI) that reads from DB

### Completely different approach:
 - Instead of watching file, wrap logging method
