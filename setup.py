import sys
from cx_Freeze import setup, Executable

buildOptions = dict(include_files = ['monerdnode/'], packages = ['requests', 're', 'json', 'datetime', 'multiprocessing'])

setup(
    name = "Update Commitment Doctor",
    version = "101",
    description = "There is no description.",
	options = dict(build_exe = buildOptions),
    executables = [Executable("mdcli.py")])