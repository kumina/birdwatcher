#!/usr/bin/env python

# Copyright (c) 2016 Kumina, https://kumina.nl/
#
# This file is distributed under a 2-clause BSD license.
# See the LICENSE file for details.

import BaseHTTPServer
import itertools
import subprocess
import sys
import traceback


def get_split_lines(f):
    """Returns lines in a file as a list of split words."""
    for line in f:
        yield line.split()


def skip_garbage(f):
    """Parses the output of birdcl(1) and removes garbage lines."""
    for line in get_split_lines(f):
        if len(line) == 3 and line[0] == 'BIRD' and line[2] == 'ready.':
            # Skip version line at the top of the output.
            pass
        elif line == ['name', 'proto', 'table', 'state', 'since', 'info']:
            # Skip the key that is printed right before the entries.
            pass
        else:
            yield line


def pairwise(iterable):
    """Iterates through a list as pairs [a, b, c, d] -> [a, b], [c, d]."""
    a = iter(iterable)
    return itertools.izip(a, a)


def parse_show_protocols(f):
    """Parses the output of 'birdcl show protocols all'."""
    lines = skip_garbage(f)
    while True:
        # Top line: instance name and state.
        line = lines.next()
        protocol_instance = line[0]
        yield ('bird_up{bird_protocol_instance="%s"}' % protocol_instance,
               int(line[3] == 'up'))

        for line in lines:
            # Empty line denotes the end of the entry.
            if not line:
                break

            # Parse lines and turn them into metrics.
            if line[0] == 'Preference:':
                yield ('bird_preference{bird_protocol_instance="%s"}' %
                       protocol_instance,
                       int(line[1]))
            elif line[0] == 'Routes:':
                for count, route_type in pairwise(line[1:]):
                    yield ('bird_routes{bird_protocol_instance="%s",bird_route_type="%s"}' %
                           (protocol_instance, route_type.rstrip(',')),
                           int(count))
            elif line[0] == 'Route' and line[1] == 'change' and line[2] == 'stats:':
                route_change_stats_keys = line[3:]
            elif line[0] in {'Import', 'Export'} and line[1] in {'updates:', 'withdraws:'}:
                for outcome, count in zip(route_change_stats_keys, line[2:]):
                    if count != '---':
                        yield ('bird_route_changes{bird_protocol_instance="%s",bird_direction="%s",bird_action="%s",bird_outcome="%s"}' %
                               (protocol_instance, line[0].lower(), line[1].rstrip(':'), outcome),
                               int(count))
            elif line[:2] == ['Hold', 'timer:']:
                v = line[2].split('/')
                yield ('bird_hold_timer_current{bird_protocol_instance="%s"}' %
                       protocol_instance,
                       int(v[0]))
                yield ('bird_hold_timer_initial{bird_protocol_instance="%s"}' %
                       protocol_instance,
                       int(v[1]))
            elif line[:2] == ['Keepalive', 'timer:']:
                v = line[2].split('/')
                yield ('bird_keepalive_timer_current{bird_protocol_instance="%s"}' %
                       protocol_instance,
                       int(v[0]))
                yield ('bird_keepalive_timer_initial{bird_protocol_instance="%s"}' %
                       protocol_instance,
                       int(v[1]))


class BirdHTTPServer(BaseHTTPServer.BaseHTTPRequestHandler):

    # Command that needs to be invoked to extract protocol statistics
    # through birdcl(1).
    _BIRDCL_COMMAND = [
        'birdcl', '-s', '/var/run/calico/bird.ctl',
        'show', 'protocols', 'all',
    ]

    def do_GET(self):
        try:
            # Invoke birdcl(1) and convert output to metrics.
            process = subprocess.Popen(self._BIRDCL_COMMAND,
                                       stdout=subprocess.PIPE)
            metrics = list(parse_show_protocols(process.stdout))
            process.wait()
            if process.returncode != 0:
                raise Exception('Failed to invoke birdcl')
        except Exception, err:
            # Failure. Return 500 and print backtrace in the browser.
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(traceback.format_exc())
        else:
            # Success. Print all metrics.
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            for key, value in metrics:
                self.wfile.write('%s %d\n' % (key, value))

if __name__ == '__main__':
    address = ('', 6502)
    server = BaseHTTPServer.HTTPServer(address, BirdHTTPServer)
    print 'Bound on %s. Waiting for requests.' % (repr(address))
    server.serve_forever()
