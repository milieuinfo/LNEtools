# -*- coding: utf-8 -*-
from PyQt4.QtGui import QIcon, QPixmap
from processing.core.AlgorithmProvider import AlgorithmProvider
from LNEtools_bufferELFbronnen import LNEtools_bufferELFbronnen
import os

class LNEtoolsProvider(AlgorithmProvider):

    def __init__(self):
        AlgorithmProvider.__init__(self)

        self.activate = True

        # Load algorithms
        self.alglist = [LNEtools_bufferELFbronnen() ]
        for alg in self.alglist:
            alg.provider = self

    def initializeSettings(self):
        """In this method we add settings needed to configure our
        provider.
        Do not forget to call the parent method, since it takes care
        or automatically adding a setting for activating or
        deactivating the algorithms in the provider. """
        AlgorithmProvider.initializeSettings(self)

    def unload(self):
        """Setting should be removed here, so they do not appear anymore
        when the plugin is unloaded. """
        AlgorithmProvider.unload(self)

    def getName(self):
        """This is the name that will appear on the toolbox group.
        It is also used to create the command line name of all the
        algorithms from this provider. """
        return 'LNE'

    def getDescription(self):
        """This is the provired full name."""
        return 'Processing Tools voor LNE'

    def getIcon(self):
        """We return the default icon."""
        curdir = os.path.dirname(__file__)
        icoFile = os.path.join( curdir, 'pics', 'icon.png' )
        icon = QIcon( QPixmap( icoFile))
        return icon

    def _loadAlgorithms(self):
        """Here we fill the list of algorithms in self.algs.
        This method is called whenever the list of algorithms should
        be updated. If the list of algorithms can change (for instance,
        if it contains algorithms from user-defined scripts and a new
        script might have been added), you should create the list again
        here. """
        self.algs = self.alglist
