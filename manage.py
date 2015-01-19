# -*- coding: utf-8 -*-
import argparse
import sys


class DefaultHelpParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help()
        sys.exit(2)


if __name__ == '__main__':
    parser = DefaultHelpParser(description='RocketWS management interface')
    parser.add_argument(
        'method',
        help='execute `method_name`',
        type=str,
        choices=['runserver', 'tests', 'shell']
    )
    parser.add_argument(
        '--settings',
        help='set settings, for example: rocketws.settings.test',
        type=str
    )

    args = parser.parse_args()

    from rocketws.conf import configure_settings
    configure_settings(args.settings or 'rocketws.settings.default')

    if args.method == 'runserver':
        from rocketws.server import run_server
        run_server()
    elif args.method == 'tests':
        # FIXME: doesn't work
        import unittest
        unittest.main(module='rocketws.tests', verbosity=2)
    elif args.method == 'shell':
        from rocketws.shell import RocketWSShell
        RocketWSShell().cmdloop()
    else:
        parser.print_help()
