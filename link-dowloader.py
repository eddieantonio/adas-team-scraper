#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Parses an XML sitemap into Make rules.
"""

import sys
import xml.etree.ElementTree as ET
from contextlib import redirect_stdout
from pathlib import Path

# Using values defined in sysexits.h:
# https://www.freebsd.org/cgi/man.cgi?query=sysexits&apropos=0&sektion=0&manpath=FreeBSD+4.3-RELEASE&format=html
EXIT_USAGE = 64
EXIT_DATAERR = 65

try:
    output_file = Path(sys.argv[1])
except IndexError:
    print("You forgot to suppy the output path!", file=sys.stderr)
    sys.exit(EXIT_USAGE)

try:
    tree = ET.parse('sitemap.xml')
except FileNotFoundError:
    print("sitemap.xml does not exist. Please download it first (use make!)",
          file=sys.stdout)
    sys.exit(EXIT_DATAERR)

raise NotImplementedError
