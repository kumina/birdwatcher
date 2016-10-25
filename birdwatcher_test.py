#!/usr/bin/env python

import StringIO
import birdwatcher
import unittest


class TestParseShowProtocols(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
