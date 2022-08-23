import curses, time, sys, re, random, subprocess, signal

signal.signal(signal.SIGINT, signal.SIG_IGN)

def update_ema(emas, x):
    for (k, v) in emas.items():
        if v is None:
            emas[k] = x
        else:
            a = 1.0/k if k != 'INF' and total > k else 1.0/total
            emas[k] = v*(1-a) + a*x

def print_ema(screen, emas, is_ms):
    keys = [x for x in emas.keys()]
    for k in keys:
        v = emas[k] if emas[k] is not None else 0.0
        if is_ms:
            screen.addstr(('%s = %6.2f ms'%(str(k).rjust(5), v)).ljust(17))
        else:
            screen.addstr(('%s =%6.1f%%'%(str(k).rjust(5), v)).ljust(17))


DEBUG = False
spacing = 4
pong = re.compile('.*time=(\d+\.\d+) ms$')
miss = re.compile('Request timeout.*$')
setup = re.compile('PING (.*): \d+.*$')
lines = []

def reset_stats():
    ms_ema = { 120 : None, 600 : None, 1800 : None, 'INF' : None }
    pl_ema = { 120 : None, 600 : None, 1800 : None, 'INF' : None }
    total = 0
    return ms_ema, pl_ema, total

screen = curses.initscr()
screen.nodelay(1)
ms_ema, pl_ema, total = reset_stats()

try:
    curses.cbreak()
    curses.noecho()
    ping_process = subprocess.Popen(['ping'] + sys.argv[1:], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # read the first line, which is PING describing its setup
    line = ping_process.stdout.readline().decode('utf8')
    m = setup.match(line)
    # check for a match, if there is no match then it's likely ping is providing usage
    if m:
        target = m.group(1)

        line = ping_process.stdout.readline().decode('utf8')
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
            print_ema(screen, ms_ema, True)

            # packet loss
            screen.addstr(2, 0, 'Packet loss:'.ljust(12))
            print_ema(screen, pl_ema, False)

            for i in range(len(lines)):
                screen.addstr(spacing+i, 0, lines[i])
            screen.refresh()
            line = ping_process.stdout.readline().decode('utf8')
            total += 1

            if DEBUG and random.random() > 0.5:
                line = 'Request timeout DEBUG\n'

            reset = screen.getch()
            if reset == ord('r') or reset == ord('R'):
                ms_ema, pl_ema, total = reset_stats()
                lines += ['RESET']
    else:
        # capture usage/error info so we can print that
        lines += [line]
        lines += ping_process.stdout.readlines()

finally:
    screen.addstr(2, 0, 'Packet loss:'.ljust(12))
    screen.nodelay(0)
    curses.echo()
    curses.nocbreak()
    curses.endwin()
    # output the tail end of the ping, useful because ping has some final stats
    for line in lines:
        print(line.strip(),)
