import glob
import json
import os
import pathlib
import re
from typing import Union

import pandas as pd

FIND_REPLACE = {  # original relative to /docs : redirect target
    "CODE_OF_CONDUCT.md": "development/#CODE_OF_CONDUCT",
    "CONTRIBUTING.md": "development/#CONTRIBUTING",
    "contributors.md": "development/#contributors",
    "architecture.md": "architecture",
    "tables.md": "tables",
}

def define_env(env):
    """
    This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    """

    @env.macro
    def include_file(filename: str, start_line: int = 0, end_line: int = None):
        """
        Include a file, optionally indicating start_line and end_line.

        Will create redirects if specified in FIND_REPLACE in main.py.

        args:
            filename: file to include, relative to the top directory of the documentation project.
            start_line (Optional): if included, will start including the file from this line
                (indexed to 0)
            end_line (Optional): if included, will stop including at this line (indexed to 0)
        """
        full_filename = os.path.join(env.project_dir, filename)
        with open(full_filename, "r") as f:
            lines = f.readlines()
        line_range = lines[start_line:end_line]
        content = "".join(line_range)

        _filenamebase = env.page.file.url

        for _find, _replace in FIND_REPLACE.items():
            if _filenamebase in _replace:
                _replace = _replace.replace(_filenamebase, "")
            content = content.replace(_find, _replace)
        return content
