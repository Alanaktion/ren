#!/usr/bin/env python3
"""Generate fish completion scripts from argument parsers"""

from argparse import ArgumentParser
import os

try:
    from ren import options
except ModuleNotFoundError:
    import sys
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.realpath(path))

    from ren import options


TEMPLATE = """complete -c %(cmd)s
%(opts)s
"""


def build_opts(cmd, parser: ArgumentParser):
    opts = []
    for action in parser._actions:
        if not action.option_strings:
            continue

        opt = "complete -c %s" % cmd

        if action.const and not action.nargs:
            opt += " -x"

        for optstr in action.option_strings:
            if optstr.startswith("--"):
                opt += " -l '" + optstr[2:] + "'"
            else:
                opt += " -s '" + optstr[1:] + "'"

        if action.help:
            opt += " -d '" + action.help.replace("'", '"') + "'"
            if action.default is not None:
                opt = opt.replace('%(default)s', str(action.default))

        opts.append(opt)
    return opts


everything: list[tuple[str, ArgumentParser]] = [
    ('ren', options.build_parser()),
]

for cmd, parser in everything:
    opts = build_opts(cmd, parser)
    os.makedirs("build/completion", exist_ok=True)
    PATH = "build/completion/%s.fish" % cmd
    with open(PATH, 'w') as fp:
        fp.write(TEMPLATE % {
            "opts": "\n".join(opts),
            "cmd": cmd,
        })
