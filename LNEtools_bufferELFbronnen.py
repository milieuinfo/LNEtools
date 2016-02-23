# -*- coding: utf-8 -*-
from PyQt4.QtGui import QIcon, QPixmap
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.outputs import OutputVector
from processing.core.parameters import *
from processing.core import GeoAlgorithmExecutionException
from algoritmHelper import *
from algoritmHelper.simpleHelpers import findOGRtype

class LNEtools_bufferELFbronnen(GeoAlgorithm):
    """Buffers rond ELF-bronnen"""
    INPUT_LAYERS = 'INPUT_LAYER'
    HOOGTE_BRON = 'HOOGTE_BRON'
    HOOGTE_VRIJ = 'HOOGTE_VRIJ'
    STERKTE = 'STERKTE'
    BELASTING = 'BELASTING'
    HOOGTE_NUM = 'HOOGTE_NUM'
    OUTPUT_LAYER = 'OUTPUT_LAYER'

    def getIcon(self):
        curdir = os.path.dirname(__file__)
        icoFile = os.path.join( curdir, 'pics', 'Script.png' )
        icon = QIcon( QPixmap( icoFile))
        return icon

    def help(self):
        return False, 'https://github.com/milieuinfo/LNEtools/blob/master/LNEtools_bufferELFbronnen.md'

    def defineCharacteristics(self):
        """Here we define the inputs and output of the algorithm, along with some other properties."""
        # The name that the user will see in the toolbox
        self.name = '_Buffers rond ELF-bronnen'
        self.group = 'Rekenmodel voor elektromagnetische straling (ELF)'
        #input paramters
        self.addParameter( ParameterMultipleInput(self.INPUT_LAYERS, u"ELF-Bronnen",
                                                  ParameterMultipleInput.TYPE_VECTOR_ANY, False) )
        self.addParameter( ParameterBoolean(self.HOOGTE_BRON, u"Op bron hoogte", False) )
        self.addParameter( ParameterNumber(self.HOOGTE_VRIJ, u"Hoogte (m)", 0, 10000 , 0) )
        self.addParameter( ParameterSelection(self.STERKTE, u"sterkte (µT)",
                            options=["0.1","0.2","0.3","0.4","0.6","0.8","1","2","10","20","25","30"], default=3 ) )
        self.addParameter( ParameterSelection(self.BELASTING, u"belasting (%)",
                            options=[str(n) for n in range(1,101)] , default=24 ) )
        # We add a vector layer as output
        self.addOutput(OutputVector(self.OUTPUT_LAYER, u"Output"))

    def processAlgorithm(self, progress):
        inputFilenames = self.getParameterValue(self.INPUT_LAYERS).split(';')
        hoogte_bron =  self.getParameterValue(self.HOOGTE_BRON)
        hoogte_vrij = float( self.getParameterValue(self.HOOGTE_VRIJ) )
        sterkte = float( self.getParameterValue(self.STERKTE) )
        belasting = float( self.getParameterValue(self.BELASTING) )
        output = self.getOutputValue(self.OUTPUT_LAYER)

        if len(inputFilenames) > 1: raise Exception("No inputdata given")

        isolijnen = QgsVectorLayer( "Polygon?crs=epsg:31370&field=BRONTYPE:string(80)&field=BRON_ID:integer" +
                       "&field=A_m:double&field=BH:double&field=B:double&field=SB:double&field=VOLTAGE:double",
                                   os.path.basename(output), "memory")
        if hoogte_bron:
            print "Hoogte: ter hoogte van de bron"
        else:
            print "Hoogte: {}".format(hoogte_vrij)
        print "ELF-bronnen: " + ";".join(inputFilenames)

        for inputFilename in inputFilenames:
            vectorLayer = dataobjects.getObjectFromUri(inputFilename)
            if vectorLayer.featureCount() == 0: break

            vectorFields = [ n.name() for n in vectorLayer.pendingFields() ]
            if not "type_bron" in vectorFields:
                print "Type van bron ontbreekt in ELF-bron '" + inputFilename + "'. Buffers zijn niet berekend."
                break

            type_bron = vectorLayer.getValues('type_bron')[0][0]

            print type_bron

            if type_bron == "cabine":
                print "ELF-bron '" + inputFilename + "' (" + type_bron + ") ..."
                BufferCabines(hoogte_bron, hoogte_vrij, sterkte, vectorLayer, isolijnen)
                print "is berekend"
            elif type_bron == "kabel":
                print "ELF-bron '" + inputFilename + "' (" + type_bron + ") ..."
                BufferOndergrondseKabels2(hoogte_bron, hoogte_vrij, sterkte, belasting, vectorLayer, isolijnen)
                print "is berekend"
            elif type_bron == "luchtlijn":
                print "ELF-bron '" + inputFilename + "' (" + type_bron + ") ..."
                BufferLuchtlijnen(hoogte_bron, hoogte_vrij, sterkte, belasting, vectorLayer, isolijnen)
                print "is berekend"
            elif type_bron == "transformatiesite":
                print "ELF-bron '" + inputFilename + "' (" + type_bron + ") ..."
                BufferTransformatieposten(hoogte_bron, hoogte_vrij, sterkte, vectorLayer,  isolijnen)
                print "is berekend"
            else:
                print "Type '"+ type_bron +"' van ELF-bron '"+ inputFilename +"'is onbekend. Buffers zijn niet berekend."

        #finish
        flType = findOGRtype(output)

        error = QgsVectorFileWriter.writeAsVectorFormat( isolijnen , output, "utf-8", None, flType )

        if error != QgsVectorFileWriter.NoError:
           QgsMapLayerRegistry.instance().addMapLayer(isolijnen)
           raise GeoAlgorithmExecutionException("Could not  write to " + output + " added memory instead ")
        else:
            del isolijnen
