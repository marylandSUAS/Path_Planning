#!/usr/bin/env python
# CLI for interacting with interop server.

from __future__ import print_function
import argparse
import datetime
import getpass
import logging
import pprint
import sys
import time

from interop import Client
<<<<<<< HEAD
from interop import Odlc
from interop import Telemetry
from proxy_mavlink import proxy_mavlink
from upload_odlcs import upload_odlcs
=======
from interop import Target
from interop import Telemetry
from proxy_mavlink import proxy_mavlink
from upload_targets import upload_targets, upload_legacy_targets
>>>>>>> 6ecfea6f2aa884c93ff663d9577e4690691e94c5

logger = logging.getLogger(__name__)


def missions(args, client):
    missions = client.get_missions()
    for m in missions:
        pprint.pprint(m.serialize())


<<<<<<< HEAD
def odlcs(args, client):
    if args.odlc_dir:
        upload_odlcs(client, args.odlc_dir, args.team_id,
                     args.actionable_override)
    else:
        odlcs = client.get_odlcs()
        for odlc in odlcs:
            pprint.pprint(odlc.serialize())
=======
def targets(args, client):
    if args.legacy_filepath:
        if not args.target_dir:
            raise ValueError('--target_dir is required.')
        upload_legacy_targets(client, args.legacy_filepath, args.target_dir)
    elif args.target_dir:
        upload_targets(client, args.target_dir, args.team_id,
                       args.actionable_override)
    else:
        targets = client.get_targets()
        for target in targets:
            pprint.pprint(target.serialize())
>>>>>>> 6ecfea6f2aa884c93ff663d9577e4690691e94c5


def probe(args, client):
    while True:
        start_time = datetime.datetime.now()

        telemetry = Telemetry(0, 0, 0, 0)
        telemetry_resp = client.post_telemetry(telemetry)
        obstacle_resp = client.get_obstacles()

        end_time = datetime.datetime.now()
        elapsed_time = (end_time - start_time).total_seconds()
        logger.info('Executed interop. Total latency: %f', elapsed_time)

        delay_time = args.interop_time - elapsed_time
        if delay_time > 0:
            try:
                time.sleep(delay_time)
            except KeyboardInterrupt:
                sys.exit(0)


def mavlink(args, client):
    proxy_mavlink(args.device, client)


def main():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format='%(asctime)s: %(name)s: %(levelname)s: %(message)s')

    # Parse command line args.
    parser = argparse.ArgumentParser(description='AUVSI SUAS Interop CLI.')
<<<<<<< HEAD
    parser.add_argument(
        '--url', required=True, help='URL for interoperability.')
    parser.add_argument(
        '--username', required=True, help='Username for interoperability.')
=======
    parser.add_argument('--url',
                        required=True,
                        help='URL for interoperability.')
    parser.add_argument('--username',
                        required=True,
                        help='Username for interoperability.')
>>>>>>> 6ecfea6f2aa884c93ff663d9577e4690691e94c5
    parser.add_argument('--password', help='Password for interoperability.')

    subparsers = parser.add_subparsers(help='Sub-command help.')

    subparser = subparsers.add_parser('missions', help='Get missions.')
    subparser.set_defaults(func=missions)

    subparser = subparsers.add_parser(
<<<<<<< HEAD
        'odlcs',
        help='Upload odlcs.',
        description='''Download or upload odlcs to/from the interoperability
server.

Without extra arguments, this prints all odlcs that have been uploaded to the
server.

With --odlc_dir, this uploads new odlcs to the server.

This tool searches for odlc JSON and images files within --odlc_dir
conforming to the 2017 Object File Format and uploads the odlc
characteristics and thumbnails to the interoperability server.

There is no deduplication logic. Odlcs will be uploaded multiple times, as
unique odlcs, if the tool is run multiple times.''',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparser.set_defaults(func=odlcs)
    subparser.add_argument(
        '--odlc_dir',
        help='Enables odlc upload. Directory containing odlc data.')
    subparser.add_argument(
        '--team_id',
        help='''The username of the team on whose behalf to submit odlcs.
Must be admin user to specify.''')
    subparser.add_argument(
        '--actionable_override',
        help='''Manually sets all the odlcs in the odlc dir to be
=======
        'targets',
        help='Upload targets.',
        description='''Download or upload targets to/from the interoperability
server.

Without extra arguments, this prints all targets that have been uploaded to the
server.

With --target_dir, this uploads new targets to the server.

This tool searches for target JSON and images files within --target_dir
conforming to the 2017 Object File Format and uploads the target
characteristics and thumbnails to the interoperability server.

Alternatively, if --legacy_filepath is specified, that file is parsed as the
legacy 2016 tab-delimited target file format. Image paths referenced in the
file are relative to --target_dir.

There is no deduplication logic. Targets will be uploaded multiple times, as
unique targets, if the tool is run multiple times.''',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparser.set_defaults(func=targets)
    subparser.add_argument(
        '--legacy_filepath',
        help='Target file in the legacy 2016 tab-delimited format.')
    subparser.add_argument(
        '--target_dir',
        help='Enables target upload. Directory containing target data.')
    subparser.add_argument(
        '--team_id',
        help='''The username of the team on whose behalf to submit targets.
Must be admin user to specify.''')
    subparser.add_argument(
        '--actionable_override',
        help='''Manually sets all the targets in the target dir to be
>>>>>>> 6ecfea6f2aa884c93ff663d9577e4690691e94c5
actionable. Must be admin user to specify.''')

    subparser = subparsers.add_parser('probe', help='Send dummy requests.')
    subparser.set_defaults(func=probe)
<<<<<<< HEAD
    subparser.add_argument(
        '--interop_time',
        type=float,
        default=1.0,
        help='Time between sent requests (sec).')
=======
    subparser.add_argument('--interop_time',
                           type=float,
                           default=1.0,
                           help='Time between sent requests (sec).')
>>>>>>> 6ecfea6f2aa884c93ff663d9577e4690691e94c5

    subparser = subparsers.add_parser(
        'mavlink',
        help='''Receive MAVLink GLOBAL_POSITION_INT packets and
forward as telemetry to interop server.''')
    subparser.set_defaults(func=mavlink)
    subparser.add_argument(
        '--device',
        type=str,
        help='pymavlink device name to read from. E.g. tcp:localhost:8080.')

    # Parse args, get password if not provided.
    args = parser.parse_args()
    if args.password:
        password = args.password
    else:
        password = getpass.getpass('Interoperability Password: ')

    # Create client and dispatch subcommand.
    client = Client(args.url, args.username, password)
    args.func(args, client)


if __name__ == '__main__':
    main()
