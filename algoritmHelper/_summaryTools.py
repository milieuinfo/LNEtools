# -*- coding: utf-8 -*-
from qgis.core import QgsVectorFileWriter, QgsFeatureRequest, QgsExpression
from simpleHelpers import findOGRtype
from processing import runalg

def VerdiepingUitBlootstellingsHoogte(buffers):
    verdieping = 0
    if len(buffers.getDoubleValues("BH")):
        blootstellingshoogte = buffers.getDoubleValues("BH")[0]
        if blootstellingshoogte >= 0:
            verdieping = max(1, int(blootstellingshoogte / 3.0))
        else:
            verdieping = -1
    return verdieping

def MaakOverzichtstabel(selectie, statistics_fields, outputTable):
    gemeenteField = selectie.fieldNameIndex("Gemeente")
    gemeentes = selectie.uniqueValues(gemeenteField)
    outString = ";".join(statistics_fields) + ";Gemeente" + "\n"

    for field in statistics_fields:
        sumVals = sum( selectie.getDoubleValues(field, False)[0] )
        outString += str( sumVals ) +";"
    outString += ";total\n"

    for gemeente in gemeentes:
        expression = QgsExpression("Gemeente = '{}'".format(gemeente) )
        qry = QgsFeatureRequest( expression )
        feats = selectie.getFeatures( qry )
        for field in statistics_fields:
            sumVals = sum([feat[field] for feat in feats ])
            outString += str( sumVals ) +";"
        outString += ";"+ gemeente +"\n"

    fl = open( outputTable, 'w' )
    fl.write(outString)
    fl.close()

def MaximumTelling(selectie_gebouwen, outputTable, outputFeatures):
    if outputTable:
        statistics_fields = ["AZ_T","PZ_T","PVT_T","WZC_T","SOM_T"]
        MaakOverzichtstabel(selectie_gebouwen, statistics_fields , outputTable)
    if outputFeatures:
        flType = findOGRtype(outputFeatures)
        QgsVectorFileWriter.writeAsVectorFormat( selectie_gebouwen , outputFeatures, "utf-8", None, flType )

def MinimumTelling(selectie_gebouwen, inputBuffers, outputTable, outputFeatures):
    # buffer_lyr = arcpy.MakeFeatureLayer_management(inputBuffers, "buffer_lyr")
    # selectie_buffers = arcpy.SelectLayerByLocation_management(buffer_lyr, "INTERSECT", selectie_gebouwen, "", "NEW_SELECTION")
    # arcpy.Dissolve_management(selectie_buffers, "in_memory/disbuf", "", "", "SINGLE_PART", "DISSOLVE_LINES")
    #
    # doorsnede = arcpy.Intersect_analysis (["gebouw_lyr", "in_memory/disbuf"], "in_memory/intersect", "ALL", "", "")
    #
    # arcpy.AddField_management(doorsnede, "AZ_b", "DOUBLE", 11, 8, None, "", "NULLABLE", "NON_REQUIRED")
    # arcpy.CalculateField_management(doorsnede, "AZ_b", '!shape.area! * !AZ_D!', "PYTHON")
    #
    # arcpy.AddField_management(doorsnede, "PZ_b", "DOUBLE", 11, 8, None, "", "NULLABLE", "NON_REQUIRED")
    # arcpy.CalculateField_management(doorsnede, "PZ_b", '!shape.area! * !PZ_D!', "PYTHON")
    #
    # arcpy.AddField_management(doorsnede, "PVT_b", "DOUBLE", 11, 8, None, "", "NULLABLE", "NON_REQUIRED")
    # arcpy.CalculateField_management(doorsnede, "PVT_b", '!shape.area! * !PVT_D!', "PYTHON")
    #
    # arcpy.AddField_management(doorsnede, "WZC_b", "DOUBLE", 11, 8, None, "", "NULLABLE", "NON_REQUIRED")
    # arcpy.CalculateField_management(doorsnede, "WZC_b", '!shape.area! * !WZC_D!', "PYTHON")
    #
    # arcpy.AddField_management(doorsnede, "SOM_b", "DOUBLE", 11, 8, None, "", "NULLABLE", "NON_REQUIRED")
    # arcpy.CalculateField_management(doorsnede, "SOM_b", '!shape.area! * !SOM_D!', "PYTHON")
    #
    # if outputTable:
    #     MaakOverzichtstabel(doorsnede, "AZ_b SUM;PZ_b SUM;PVT_b SUM;WZC_b SUM;SOM_b SUM", outputTable)
    # if outputFeatures:
    #     arcpy.CopyFeatures_management(doorsnede, outputFeatures)
    pass

def TussenTelling(selectie_gebouwen, outputTable, outputFeatures):
    if outputTable:
        statistics_fields = ["AZ_T","PZ_T","PVT_T","WZC_T","SOM_T"]
        MaakOverzichtstabel(selectie_gebouwen, statistics_fields, outputTable)
    if outputFeatures:
        flType = findOGRtype(outputFeatures)
        QgsVectorFileWriter.writeAsVectorFormat(selectie_gebouwen , outputFeatures, "utf-8", None, flType )