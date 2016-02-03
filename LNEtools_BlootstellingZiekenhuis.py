# -*- coding: utf-8 -*-
import os
from PyQt4.QtGui import QIcon, QPixmap
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.parameters import *
from processing.core.outputs import OutputVector, OutputFile
from processing.tools import dataobjects
from processing import runalg
from algoritmHelper import *

class LNEtools_BlootstellingZiekenhuis(GeoAlgorithm):
    """Berekent blootstelling van personen dooor ELF-bronnen"""
    INPUTZIEKENHUIS = "INPUTZIEKENHUIS"
    INPUTBUFFERS = "INPUTBUFFERS"
    BEREKENINGSWIJZE = "BEREKENINGSWIJZE"
    OUTPUTTABLE = "OUTPUTTABLE"
    OUTPUTFEATURE = "OUTPUTFEATURE"

    def getIcon(self):
        curdir = os.path.dirname(__file__)
        icoFile = os.path.join( curdir, 'pics', 'Script.png' )
        icon = QIcon( QPixmap( icoFile))
        return icon

    def help(self):
        return False, 'http://www.milieuinfo.be/'

    def defineCharacteristics(self):
        """Here we define the inputs and output of the algorithm, along with some other properties."""
        # The name that the user will see in the toolbox
        self.name = 'Blootstelling Ziekenhuis'
        self.group = 'ELF'
        self.addParameter( ParameterVector(self.INPUTZIEKENHUIS, u"Input Ziekenhuizen of zorginstellingen",
                                 ParameterVector.VECTOR_TYPE_ANY, False ) )
        self.addParameter( ParameterVector(self.INPUTBUFFERS, u"Input ELF buffers (berekend voor één hoogte)",
                                 ParameterVector.VECTOR_TYPE_ANY, False ) )
        self.addParameter( ParameterSelection(self.BEREKENINGSWIJZE, u"Berekeningswijze",
                           options=["Maximum telling","Minimum telling","Tussenvorm"] ) )

        self.addOutput(OutputFile(self.OUTPUTTABLE, u"Output Tabel", 'csv' ))
        self.addOutput(OutputVector(self.OUTPUTFEATURE, u"Output Features"))

    def processAlgorithm(self, progress):
        inputZiekenhuis = self.getParameterValue(self.INPUTZIEKENHUIS)
        inputBuffers = self.getParameterValue(self.INPUTBUFFERS)
        berekeningswijze = self.getParameterValue(self.BEREKENINGSWIJZE)
        outputTable = self.getParameterValue(self.OUTPUTTABLE)
        outputFeature = self.getParameterValue(self.OUTPUTFEATURE)

        inputZiekenhuislayer = dataobjects.getObjectFromUri(inputZiekenhuis)
        inputBuffersLayer = dataobjects.getObjectFromUri(inputBuffers)
        verdieping = VerdiepingUitBlootstellingsHoogte(inputBuffersLayer)

        if verdieping > 0:
            # arcpy.Select_analysis(inputZiekenhuis, "in_memory/gebouwen", "\"aant_verd\" >= " + str(verdieping))
            #
            # selectie_gebouwen = arcpy.SelectLayerByLocation_management(gebouw_lyr, "INTERSECT", inputBuffers, "", "NEW_SELECTION")
            #
            # aantal = int(arcpy.GetCount_management(selectie_gebouwen).getOutput(0))
            # if aantal == 0:
            #     arcpy.AddMessage("Er liggen geen gebouwen binnen de opgegeven buffers!")
            # if berekeningswijze == "Maximum telling":
            #     MaximumTelling(selectie_gebouwen, outputTable, outputFeatures)
            # elif berekeningswijze == "Minimum telling":
            #     MinimumTelling(selectie_gebouwen, inputBuffers, outputTable, outputFeatures)
            # elif berekeningswijze == "Tussenvorm":
            #     TussenTelling(selectie_gebouwen, outputTable, outputFeatures)

            selected = runalg("qgis:selectbylocation", inputZiekenhuis, inputBuffers, [u"intersects"] , 0 )['OUTPUT']

        elif verdieping == 0:
            raise Exception("Het bufferbestand is leeg, er kan geen blootstellingshoogte bepaald worden.")
        else:
            raise Exception("Negatieve hoogte buffers: ondergronds wordt geen blootstelling berekend.")