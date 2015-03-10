# Usage

$ ping www.google.com | python ping_parse.py

....

at some point later press CTRL-C to escape.

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
