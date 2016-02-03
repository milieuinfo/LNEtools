# -*- coding: utf-8 -*-

import os, sys, inspect

from processing.core.Processing import Processing
from LNEtools_provider import LNEtoolsProvider

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


class LNEtoolsPlugin:

    def __init__(self):
        self.provider = LNEtoolsProvider()

    def initGui(self):
        Processing.addProvider(self.provider)

    def unload(self):
        Processing.removeProvider(self.provider)
