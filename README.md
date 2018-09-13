# sat6-traces

List all Satellite hosts with traces.

# What does code do

Gets the count of traces for all hosts.

Traces indicate if services on the host need to be restarted. Refer to [Satellite 6.3 Feature Overview: Tracer](https://access.redhat.com/articles/3358611) for details on enabling [Tracer](http://tracer-package.com) on hosts.

# Requirements

* Python 2.x
* [Requests](http://python-requests.org/)
* [PyYAML](https://pyyaml.org/)

Tested from RHEL 7.5 against Satellite 6.3.2.

# Usage

~~~
./sat6-traces.py
~~~

# Example Output

~~~
system_id,name,traces
2,host.example.com,20
~~~

## Configuration file
Server, username and password are loaded from a [Hammer CLI configuration file](https://github.com/theforeman/hammer-cli-foreman/blob/master/doc/configuration.md). The default path for the configuration file is `~/.hammer/cli_config.yml`.

~~~
./sat6-traces.py [-f path/to/config.yml]
~~~
