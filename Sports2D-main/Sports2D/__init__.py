#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
try:
    from importlib.metadata import version
    __version__ = version("sports2d")
except Exception:
    __version__ = "0.0.0.dev0"
VERSION = __version__