#!/usr/bin/env python

# Copyright (c) 2016 Kumina, https://kumina.nl/
#
# This file is distributed under a 2-clause BSD license.
# See the LICENSE file for details.

import StringIO
import birdwatcher
import unittest


class TestParseShowProtocols(unittest.TestCase):

    maxDiff = 4000

    def test_static(self):
        """Tests the metrics output for a static route."""
        text = '''BIRD 1.5.0 ready.
name     proto    table    state  since       info
static1  Static   master   up     2016-10-21
  Preference:     200
  Input filter:   ACCEPT
  Output filter:  REJECT
  Routes:         1 imported, 0 exported, 1 preferred
  Route change stats:     received   rejected   filtered    ignored   accepted
    Import updates:              1          0          0          0          1
    Import withdraws:            0          0        ---          0          0
    Export updates:              0          0          0        ---          0
    Export withdraws:            0        ---        ---        ---          0
'''
        self.assertEqual(
            list(birdwatcher.parse_show_protocols(StringIO.StringIO(text))),
            [('bird_up{bird_protocol_instance="static1"}', 1),
             ('bird_info{bird_protocol_instance="static1",value="unknown"}', 1),
             ('bird_info{bird_protocol_instance="static1",value="Active"}', 0),
             ('bird_info{bird_protocol_instance="static1",value="Established"}', 0),
             ('bird_preference{bird_protocol_instance="static1"}', 200),
             ('bird_routes{bird_protocol_instance="static1",bird_route_type="imported"}', 1),
             ('bird_routes{bird_protocol_instance="static1",bird_route_type="exported"}', 0),
             ('bird_routes{bird_protocol_instance="static1",bird_route_type="preferred"}', 1),
             ('bird_route_changes{bird_protocol_instance="static1",bird_direction="import",bird_action="updates",bird_outcome="received"}', 1),
             ('bird_route_changes{bird_protocol_instance="static1",bird_direction="import",bird_action="updates",bird_outcome="rejected"}', 0),
             ('bird_route_changes{bird_protocol_instance="static1",bird_direction="import",bird_action="updates",bird_outcome="filtered"}', 0),
             ('bird_route_changes{bird_protocol_instance="static1",bird_direction="import",bird_action="updates",bird_outcome="ignored"}', 0),
             ('bird_route_changes{bird_protocol_instance="static1",bird_direction="import",bird_action="updates",bird_outcome="accepted"}', 1),
             ('bird_route_changes{bird_protocol_instance="static1",bird_direction="import",bird_action="withdraws",bird_outcome="received"}', 0),
             ('bird_route_changes{bird_protocol_instance="static1",bird_direction="import",bird_action="withdraws",bird_outcome="rejected"}', 0),
             ('bird_route_changes{bird_protocol_instance="static1",bird_direction="import",bird_action="withdraws",bird_outcome="ignored"}', 0),
             ('bird_route_changes{bird_protocol_instance="static1",bird_direction="import",bird_action="withdraws",bird_outcome="accepted"}', 0),
             ('bird_route_changes{bird_protocol_instance="static1",bird_direction="export",bird_action="updates",bird_outcome="received"}', 0),
             ('bird_route_changes{bird_protocol_instance="static1",bird_direction="export",bird_action="updates",bird_outcome="rejected"}', 0),
             ('bird_route_changes{bird_protocol_instance="static1",bird_direction="export",bird_action="updates",bird_outcome="filtered"}', 0),
             ('bird_route_changes{bird_protocol_instance="static1",bird_direction="export",bird_action="updates",bird_outcome="accepted"}', 0),
             ('bird_route_changes{bird_protocol_instance="static1",bird_direction="export",bird_action="withdraws",bird_outcome="received"}', 0),
             ('bird_route_changes{bird_protocol_instance="static1",bird_direction="export",bird_action="withdraws",bird_outcome="accepted"}', 0)])

    def test_mesh_start(self):
        """Tests the metrics output for a mesh route that is not up yet."""
        text = '''BIRD 1.5.0 ready.
Mesh_10_101_4_114 BGP      master   start  2016-10-23  Active        Socket: Host is unreachable
  Description:    Connection to BGP peer
  Preference:     100
  Input filter:   ACCEPT
  Output filter:  calico_pools
  Routes:         0 imported, 0 exported, 0 preferred
  Route change stats:     received   rejected   filtered    ignored   accepted
    Import updates:              0          0          0          0          0
    Import withdraws:            0          0        ---          0          0
    Export updates:              0          0          0        ---          0
    Export withdraws:            0        ---        ---        ---          0
  BGP state:          Active
    Neighbor address: 10.101.4.114
    Neighbor AS:      64511
    Connect delay:    3/5
    Last error:       Socket: Host is unreachable
'''
        self.assertEqual(
            list(birdwatcher.parse_show_protocols(StringIO.StringIO(text))),
            [('bird_up{bird_protocol_instance="Mesh_10_101_4_114"}', 0),
             ('bird_info{bird_protocol_instance="Mesh_10_101_4_114",value="unknown"}', 0),
             ('bird_info{bird_protocol_instance="Mesh_10_101_4_114",value="Active"}', 1),
             ('bird_info{bird_protocol_instance="Mesh_10_101_4_114",value="Established"}', 0),
             ('bird_preference{bird_protocol_instance="Mesh_10_101_4_114"}', 100),
             ('bird_routes{bird_protocol_instance="Mesh_10_101_4_114",bird_route_type="imported"}', 0),
             ('bird_routes{bird_protocol_instance="Mesh_10_101_4_114",bird_route_type="exported"}', 0),
             ('bird_routes{bird_protocol_instance="Mesh_10_101_4_114",bird_route_type="preferred"}', 0),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_114",bird_direction="import",bird_action="updates",bird_outcome="received"}', 0),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_114",bird_direction="import",bird_action="updates",bird_outcome="rejected"}', 0),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_114",bird_direction="import",bird_action="updates",bird_outcome="filtered"}', 0),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_114",bird_direction="import",bird_action="updates",bird_outcome="ignored"}', 0),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_114",bird_direction="import",bird_action="updates",bird_outcome="accepted"}', 0),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_114",bird_direction="import",bird_action="withdraws",bird_outcome="received"}', 0),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_114",bird_direction="import",bird_action="withdraws",bird_outcome="rejected"}', 0),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_114",bird_direction="import",bird_action="withdraws",bird_outcome="ignored"}', 0),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_114",bird_direction="import",bird_action="withdraws",bird_outcome="accepted"}', 0),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_114",bird_direction="export",bird_action="updates",bird_outcome="received"}', 0),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_114",bird_direction="export",bird_action="updates",bird_outcome="rejected"}', 0),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_114",bird_direction="export",bird_action="updates",bird_outcome="filtered"}', 0),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_114",bird_direction="export",bird_action="updates",bird_outcome="accepted"}', 0),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_114",bird_direction="export",bird_action="withdraws",bird_outcome="received"}', 0),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_114",bird_direction="export",bird_action="withdraws",bird_outcome="accepted"}', 0)])

    def test_mesh_up(self):
        """Tests the metrics output for a mesh route that is up."""
        text = '''BIRD 1.5.0 ready.
Mesh_10_101_4_182 BGP      master   up     2016-10-23  Established
  Description:    Connection to BGP peer
  Preference:     100
  Input filter:   ACCEPT
  Output filter:  calico_pools
  Routes:         1 imported, 1 exported, 1 preferred
  Route change stats:     received   rejected   filtered    ignored   accepted
    Import updates:              1          0          0          0          1
    Import withdraws:            0          0        ---          0          0
    Export updates:             44         25         18        ---          1
    Export withdraws:            0        ---        ---        ---          0
  BGP state:          Established
    Neighbor address: 10.101.4.182
    Neighbor AS:      64511
    Neighbor ID:      10.101.4.182
    Neighbor caps:    refresh enhanced-refresh restart-able AS4 add-path-rx add-path-tx
    Session:          internal multihop AS4 add-path-rx add-path-tx
    Source address:   10.101.4.148
    Hold timer:       177/240
    Keepalive timer:  61/80
'''
        self.assertEqual(
            list(birdwatcher.parse_show_protocols(StringIO.StringIO(text))),
            [('bird_up{bird_protocol_instance="Mesh_10_101_4_182"}', 1),
             ('bird_info{bird_protocol_instance="Mesh_10_101_4_182",value="unknown"}', 0),
             ('bird_info{bird_protocol_instance="Mesh_10_101_4_182",value="Active"}', 0),
             ('bird_info{bird_protocol_instance="Mesh_10_101_4_182",value="Established"}', 1),
             ('bird_preference{bird_protocol_instance="Mesh_10_101_4_182"}', 100),
             ('bird_routes{bird_protocol_instance="Mesh_10_101_4_182",bird_route_type="imported"}', 1),
             ('bird_routes{bird_protocol_instance="Mesh_10_101_4_182",bird_route_type="exported"}', 1),
             ('bird_routes{bird_protocol_instance="Mesh_10_101_4_182",bird_route_type="preferred"}', 1),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_182",bird_direction="import",bird_action="updates",bird_outcome="received"}', 1),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_182",bird_direction="import",bird_action="updates",bird_outcome="rejected"}', 0),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_182",bird_direction="import",bird_action="updates",bird_outcome="filtered"}', 0),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_182",bird_direction="import",bird_action="updates",bird_outcome="ignored"}', 0),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_182",bird_direction="import",bird_action="updates",bird_outcome="accepted"}', 1),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_182",bird_direction="import",bird_action="withdraws",bird_outcome="received"}', 0),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_182",bird_direction="import",bird_action="withdraws",bird_outcome="rejected"}', 0),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_182",bird_direction="import",bird_action="withdraws",bird_outcome="ignored"}', 0),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_182",bird_direction="import",bird_action="withdraws",bird_outcome="accepted"}', 0),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_182",bird_direction="export",bird_action="updates",bird_outcome="received"}', 44),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_182",bird_direction="export",bird_action="updates",bird_outcome="rejected"}', 25),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_182",bird_direction="export",bird_action="updates",bird_outcome="filtered"}', 18),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_182",bird_direction="export",bird_action="updates",bird_outcome="accepted"}', 1),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_182",bird_direction="export",bird_action="withdraws",bird_outcome="received"}', 0),
             ('bird_route_changes{bird_protocol_instance="Mesh_10_101_4_182",bird_direction="export",bird_action="withdraws",bird_outcome="accepted"}', 0),
             ('bird_hold_timer_current{bird_protocol_instance="Mesh_10_101_4_182"}', 177),
             ('bird_hold_timer_initial{bird_protocol_instance="Mesh_10_101_4_182"}', 240),
             ('bird_keepalive_timer_current{bird_protocol_instance="Mesh_10_101_4_182"}', 61),
             ('bird_keepalive_timer_initial{bird_protocol_instance="Mesh_10_101_4_182"}', 80)])


if __name__ == '__main__':
    unittest.main()
