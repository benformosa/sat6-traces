#!/usr/bin/python

"""
List all Satellite hosts with traces.
"""

"""
This program is heavily on https://github.com/RedHatSatellite/sat6-currency
"""

"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import csv
import json
import os
import requests
import sys
import yaml


def get_with_json(location, json_data):
    """
    Performs a GET and passes the data to the url location
    """
    try:
        result = requests.get(
            location,
            data=json_data,
            auth=(username, password),
            verify=ssl_verify,
            headers=post_headers
        )

    except requests.ConnectionError, e:
        print("{} Couldn't connect to the API,"
              " check connection or url".format(location))
        print(e)
        sys.exit(1)
    if result.ok:
        return result.json()
    else:
        print(" Error connecting to '{}'. HTTP Status: {}".format(
            location, str(result.status_code)))
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="List all Satellite hosts with traces")
    parser.add_argument(
        "-f", "--config",
        type=argparse.FileType(mode='r'),
        help="Hammer CLI config file (defaults to ~/.hammer/cli_config.yml",
        default=os.path.expanduser('~/.hammer/cli_config.yml')
    )
    parser.add_argument(
        "-s", "--search",
        type=str,
        help="Search string for host."
        " (like ?search=lifecycle_environment=Test)",
        default=('')
    )
    parser.add_argument(
        "-a", "--all",
        action='store_const',
        const=-1,
        default=0,
        help="Also list hosts with no traces",
    )
    parser.add_argument(
        "-o", "--output",
        choices=['csv', 'json', 'yaml'],
        default='csv',
        help="Set output format",
    )

    args = parser.parse_args()

    # Load the Hammer CLI configuration file
    config = yaml.safe_load(args.config)
    # If the key is present in the config file, attempt to load values
    key = ':foreman'
    url = config[key][':host']
    username = config[key][':username']
    password = config[key][':password']

    api = url + "/api/"
    post_headers = {'content-type': 'application/json'}
    ssl_verify = True

    # Get all hosts (alter if you have more than 10000 hosts)
    hosts = get_with_json(
        "{}hosts{}".format(api, args.search),
        json.dumps({"per_page": "10000"})
    )["results"]

    output = []
    for host in hosts:
        # Get traces for host
        traces = get_with_json(
            "{}hosts/{}/traces".format(api, host["id"]),
            json.dumps({"per_page": "10000"})
        )
        host["traces"] = traces["total"]

        # Add to output if traces > 0
        if host["traces"] > args.all:
            output.append({
                "system_id": host["id"],
                "name": str(host["name"]),
                "traces": host["traces"],
            })

    if output:
        if args.output == 'csv':
            w = csv.DictWriter(sys.stdout, ["system_id", "name", "traces"])
            w.writeheader()
            w.writerows(output)
        elif args.output == 'json':
            print(json.dumps(output, separators=(',', ':')))
        elif args.output == 'yaml':
            print(yaml.dump(
                output,
                explicit_start=True,
                default_flow_style=False,
                encoding='utf-8'
            ))
