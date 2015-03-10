import curses, time, sys, re, random
screen = curses.initscr()
curses.cbreak()
curses.noecho()

DEBUG_PACKET_LOSS = False
spacing = 4
ms_ema = { 5 : None, 20 : None, 100 : None, 'INF' : None }
pl_ema = { 10 : None, 100 : None, 1000 : None, 'INF' : None }
pong = re.compile('.*time=(\d+\.\d+) ms$')
miss = re.compile('Request timeout.*$')
setup = re.compile('PING (.*): \d+.*$')
total = 0

def update_ema(emas, x):
    for (k, v) in emas.items():
        if v is None:
            emas[k] = x
        else:
            a = 1.0/k if k != 'INF' and total > k else 1.0/total
            emas[k] = v*(1-a) + a*x

def print_ema(emas, is_ms):
    keys = emas.keys()
    keys.sort()
    for k in keys:
        v = emas[k] if emas[k] is not None else 0.0
        if is_ms:
            screen.addstr(('%s = %6.2f ms'%(str(k).rjust(5), v)).ljust(17))
        else:
            screen.addstr(('%s =%6.1f%%'%(str(k).rjust(5), v)).ljust(17))

try:
    lines = []
    # read the first line, which is PING describing its setup
    line = sys.stdin.readline()
    m = setup.match(line)
    target = m.group(1)

    line = sys.stdin.readline()
    total += 1
    while line:
        lines += [line]
        m = pong.match(line)
        if m:
            ms = float(m.group(1))
            update_ema(ms_ema, ms)
            update_ema(pl_ema, 0.0)

        elif miss.match(line):
            update_ema(pl_ema, 100.0)

        while len(lines) >= screen.getmaxyx()[0] - spacing:
            lines.pop(0)

        screen.erase()
        screen.addstr(0, 0, 'Total pings to %s: %d'%(target, total))
        # EMAs of latency
        screen.addstr(1, 0, 'Latency:'.ljust(12))
        print_ema(ms_ema, True)

        # packet loss
        screen.addstr(2, 0, 'Packet loss:'.ljust(12))
        print_ema(pl_ema, False)

        for i in range(len(lines)):
            screen.addstr(spacing+i, 0, lines[i])
        screen.refresh()
        line = sys.stdin.readline()
        total += 1
        if DEBUG_PACKET_LOSS and random.random() > 0.5:
            line = 'Request timeout DEBUG'

finally:
    curses.echo()
    curses.nocbreak()
    curses.endwin()
