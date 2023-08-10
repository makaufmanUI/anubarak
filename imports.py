"""
imports.py
~~~~~~~~~~

Date: 08/09/2023 05:54
"""
import re
import os
import sys
import time
import json
import requests
import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import scipy.stats as stats
import matplotlib.pyplot as plt
from rich.progress import track
from collections import namedtuple
from typing import Any, NamedTuple
from rich.traceback import install
from rich import print as richprint

install()
print( '\n\n' + '-' * 120 + '\n\n\n'   )
main_ending_print_string = '\n\n' + '-' * 120 + '\n\n'
mpl.rcParams['figure.figsize'] = (14, 8)
mpl.rcParams['axes.grid'] = True
mpl.rcParams['grid.alpha'] = 0.5
mpl.rcParams['grid.linewidth'] = 1.0
mpl.rcParams['axes.labelpad'] = 20
mpl.rcParams['axes.labelsize'] = 13
mpl.rcParams['axes.titlepad'] = 25
mpl.rcParams['axes.titlesize'] = 16
mpl.rcParams['axes.titleweight'] = 'bold'
mpl.rcParams['legend.fontsize'] = 11
mpl.rcParams['legend.fancybox'] = False
mpl.rcParams['legend.markerscale'] = 1.5
mpl.rcParams['legend.borderpad'] = 0.5
mpl.rcParams['legend.framealpha'] = 1.0
mpl.rcParams['legend.labelspacing'] = 1.0
mpl.rcParams['legend.handlelength'] = 1.5
mpl.rcParams['legend.handleheight'] = 0.5

def rprint(*args, **kwargs):
    """Prints to console with arrow indicator."""
    richprint(f"[bold red] >>> [/bold red]", *args, **kwargs)

def rprints(numspaces: int, *args, **kwargs):
    """Prints to console with arrow indicator."""
    richprint(f"{' '*(numspaces-1)} [bold red] >>> [/bold red]", *args, **kwargs)
