# Usage

$ python ping_parse.py www.google.com

....

at some point later press CTRL-C to escape. When CTRL-C is pressed, the tail of
ping will be output.

# What Does it Do

ping_parse.py takes the output of ping, and computes the moving averages of
latency and packet loss at several window sizes. Here's a sample of the output:

    Total pings to www.google.com (74.125.28.147): 973
    Latency:        5 =  38.51 ms   20 =  40.18 ms  100 =  37.90 ms  INF =  36.33 ms
    Packet loss:   10 =   6.6%     100 =   2.0%    1000 =   0.7%     INF =   0.7%

    64 bytes from 74.125.28.147: icmp_seq=942 ttl=46 time=33.096 ms
    64 bytes from 74.125.28.147: icmp_seq=943 ttl=46 time=31.667 ms
    64 bytes from 74.125.28.147: icmp_seq=944 ttl=46 time=31.521 ms
    64 bytes from 74.125.28.147: icmp_seq=945 ttl=46 time=38.498 ms
    64 bytes from 74.125.28.147: icmp_seq=946 ttl=46 time=33.976 ms
    64 bytes from 74.125.28.147: icmp_seq=947 ttl=46 time=34.596 ms
    64 bytes from 74.125.28.147: icmp_seq=948 ttl=46 time=32.890 ms
    64 bytes from 74.125.28.147: icmp_seq=949 ttl=46 time=35.039 ms

Below the windowed statistics the latest lines from ping are written, as seen above.

# Known Issues

I wrote this program in a few hours while drinking whiskey in a ski chalet.
It's my first time using curses, and my first time using subprocess. It really
shouldn't work at all.  But every so often it does, here are somethings that
will probably go wrong.

* All command line arguments are passed to ping. I haven't tested parse_ping
  with most options. If an option affects the output, it could easily break the
  regex's I rely on for extracting data from ping's output.
* ping doesn't flush STDOUT when a request times-out. This means timeouts won't
  be reported until the next successful response (or until STDOUT is flushed).
