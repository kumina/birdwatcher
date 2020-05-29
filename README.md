**Important** Kumina is no longer actively maintaining this code. Feel free to fork and publish yourself!

# Birdwatcher: Prometheus exporter for Calico/BIRD

When using [Calico](https://www.projectcalico.org/) in combination with
[Kubernetes](http://kubernetes.io/]), it may make sense to have some
basic monitoring for it through [Prometheus](https://prometheus.io/).

This utility implements a simple web server written in Python that
extracts metrics from the BIRD internet routing daemon that is used by
Calico. It parses the output of `birdcl show protocols all` and turns it
into a series of metrics in Prometheus' format, exporting them over HTTP.

It typically makes sense to run this daemon in a Kubernetes `DaemonSet`,
so that every node in your cluster runs exactly one copy of this daemon.
Just make sure that `/var/run/calico/bird.ctl` points to the UNIX socket
exposed by BIRD by using a `hostPath` directive. The provided
`Dockerfile` already contains a copy of the `birdcl` utility.

Be sure to check out `birdwatcher_test.py` to get an idea of how the
output of `birdcl` is translated to a set of metrics.
