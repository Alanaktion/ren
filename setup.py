import os
from setuptools import setup

def check_file(f):
    path = os.path.join(os.path.dirname(__file__), f)
    return os.path.exists(path)

# TODO: run completion build: scripts/completion*.py automatically
# TODO: make sure this actually bundles the files
data_files = [
    (path, [f for f in files if check_file(f)])
    for (path, files) in [
        ("share/bash-completion/completions", ["build/completion/ren"]),
        ("share/zsh/site-functions", ["build/completion/_ren"]),
        ("share/fish/vendor_completions.d", ["build/completion/ren.fish"]),
    ]
]

setup()
