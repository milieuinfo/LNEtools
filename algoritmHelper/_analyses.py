# -*- coding: utf-8 -*-
from _geomConstruct import *
from _geomMath import  *

def BufferCabines(op_bronhoogte, hw, sterkte, inputFeatureLayer, isolijnenlayer):
    isolijnenProvider = isolijnenlayer.dataProvider()
    cabines = inputFeatureLayer.getFeatures()
    fields = isolijnenlayer.pendingFields()

    for cabine in cabines:
        fid = cabine.id()
        mx = cabine["X"]
        my = cabine["Y"]
        hb = cabine["Z"]

        if op_bronhoogte:
            hw = hb

        afstand = BufferAfstandCabine(hb, hw, sterkte)

        if afstand > 0:
            isolijn = QgsFeature( fields )
            isolijn["BRONTYPE"] = "cabine"
            isolijn["BRON_ID"] = fid
            isolijn["A_m"] = afstand
            isolijn["BH"] =  hw
            isolijn["B"] =  sterkte
            isolijn["SB"] = -9999
            isolijn["VOLTAGE"] = -9999
            isolijn.setGeometry( PuntenNaarPolygon(CirkelPunten(mx, my, afstand)) )
            isolijnenProvider.addFeatures([isolijn])
    isolijnenlayer.updateExtents()
    return isolijnenlayer

def BufferTransformatieposten(op_bronhoogte, hw, sterkte, inputFeatureLayer, isolijnenlayer):
    isolijnenProvider = isolijnenlayer.dataProvider()
    posten = inputFeatureLayer.getFeatures()
    fields = isolijnenlayer.pendingFields()

    for post in posten:
        fid = post.id()
        mx = post["X"]
        my = post["Y"]
        hb = post["Z"]

        if op_bronhoogte:
            hw = hb

        afstand = BufferAfstandTransformatieposten(hb, hw, sterkte)
        if afstand > 0:
            isolijn = QgsFeature(fields)
            isolijn["BRONTYPE"] = "transformatiesite"
            isolijn["BRON_ID"] = fid
            isolijn["A_m"] = afstand
            isolijn["BH"] =  hw
            isolijn["B"] =  sterkte
            isolijn["SB"] = -9999
            isolijn["VOLTAGE"] = -9999
            isolijn.setGeometry( PuntenNaarPolygon(CirkelPunten(mx, my, afstand)) )
            isolijnenProvider.addFeatures([isolijn])
    isolijnenlayer.updateExtents()
    return isolijnenlayer

def BufferOndergrondseKabels2(op_bronhoogte, hw, sterkte, belasting, inputFeatureLayer, isolijnenlayer):
    isolijnenProvider = isolijnenlayer.dataProvider()
    kabels = inputFeatureLayer.getFeatures()
    fields = isolijnenlayer.pendingFields()

    for kabel in kabels:
        fid = kabel.id()
        voltage = kabel["VOLTAGE"]
        stroom = kabel["Stroom_nom"]
        diepte = kabel["z_waarde"]

        if op_bronhoogte:
            hw = -diepte

        afstand = BufferAfstandOndergrondseKabels(diepte, hw, sterkte, voltage, stroom, belasting)
        if afstand > 0:
            geom = kabel.geometry().buffer( afstand, 100 )

            isolijn = QgsFeature( fields )
            isolijn["BRONTYPE"] = "kabel"
            isolijn["BRON_ID"] = fid
            isolijn["A_m"] = afstand
            isolijn["BH"] =  hw
            isolijn["B"] =  sterkte
            isolijn["SB"] = belasting
            isolijn["VOLTAGE"] = voltage
            isolijn.Shape = geom
            isolijnenProvider.addFeatures([isolijn])
    isolijnenlayer.updateExtents()
    return isolijnenlayer

def BufferLuchtlijnen(op_bronhoogte, hw, sterkte, belasting, inputFeatureLayer, isolijnenlayer):
    isolijnenProvider = isolijnenlayer.dataProvider()
    fields = isolijnenlayer.pendingFields()
    lijnen = inputFeatureLayer.getFeatures()

    for lijn in lijnen:
        fid = lijn.id()
        geom = lijn.geometry().asPolyline()
        p0 = geom[0]
        p1 = geom[-1]
        s = lijn.geometry().length()

        voltage = lijn["VOLTAGE"]
        stroom = lijn["Stroom_nom"]
        h0 = lijn["z_s_lijn"]
        h1 = lijn["z_e_lijn"]
        doorhang = lijn["doorhang"]
        h2 = max(0, h0 + (1.0 / 2.0) * (h1 - h0) - doorhang)

        parabool = FitParabool(0, h0, s, h1, s/2.0, h2)
        a = parabool[0]
        b = parabool[1]
        c = parabool[2]

        if a > 0:
            x_min = -b / (2 * a)
            if x_min < 0:
                h_min = h0
            elif x_min > s:
                h_min = h1
            else:
                h_min = -((b * b) / (4 * a)) + c
        else:
            h_min = min(h0, h1)

        if op_bronhoogte:
            numpoints = 1
            staplengte = s / numpoints
        else:
            numpoints = max(1, math.trunc((s / 25.0) + 0.5))
            staplengte = s / numpoints

        punten_rechts = []
        punten_links = []
        heeft_buffer = False

        beta = BerekenHoekBeta(p0, p1)
        sin_beta = math.sin(beta)
        cos_beta = math.cos(beta)

        if op_bronhoogte:
            hw = h0

        afstand = BufferAfstandLuchtlijnen(h0, hw, sterkte, voltage, stroom, belasting)
        max_afstand = afstand
        if afstand > 0:
            heeft_buffer = True
            punten = BerekenRandPunten(p0, afstand, p0, p1, sin_beta, cos_beta)
            punten_links.append(punten[0])
            punten_rechts.append(punten[1])

        for stap in range(1, numpoints):
            ss = stap * staplengte
            h = a * ss * ss + b * ss + c

            if op_bronhoogte:
                hw = h

            afstand = BufferAfstandLuchtlijnen(h, hw, sterkte, voltage, stroom, belasting)
            if afstand > max_afstand:
                max_afstand = afstand

            if afstand > 0:
                p2 = QgsPoint()
                p2.setX( p0.x() + (ss / s) * (p1.x() - p0.x()) )
                p2.setY(  p0.y() + (ss / s) * (p1.y() - p0.y()) )

                if not heeft_buffer:
                    heeft_buffer = True

                punten = BerekenRandPunten(p2, afstand, p0, p1, sin_beta, cos_beta)
                punten_links.append(punten[0])
                punten_rechts.append(punten[1])

        if op_bronhoogte:
            hw = h1

        afstand = BufferAfstandLuchtlijnen(h1, hw, sterkte, voltage, stroom, belasting)
        if afstand > max_afstand:
            max_afstand = afstand
        if afstand > 0:
                if not heeft_buffer:
                    heeft_buffer = True

                punten = BerekenRandPunten(p1, afstand, p0, p1, sin_beta, cos_beta)
                punten_links.append(punten[0])
                punten_rechts.append(punten[1])

        if heeft_buffer:
            #  maak polylijn en voeg halve cirkels toe
            punten_rechts.reverse()
            polyline = []
            for punt in punten_links:
                polyline.append(punt)
            for (x, y) in HalveCirkel(punten_links[-1], punten_rechts[0]):
                polyline.append( QgsPoint(x,y) )
            for punt in punten_rechts:
                polyline.append(punt)
            for (x, y) in HalveCirkel(punten_rechts[-1], punten_links[0]):
                polyline.append( QgsPoint(x,y) )

            isolijn = QgsFeature( fields )
            isolijn["BRONTYPE"] = "luchtlijn"
            isolijn["BRON_ID"] = fid
            isolijn["A_m"] = max_afstand

            if op_bronhoogte:
                hw = h_min

            isolijn["BH"] = hw
            isolijn["B"] = sterkte
            isolijn["SB"] = belasting
            isolijn["VOLTAGE"] = voltage
            isolijn.setGeometry( QgsGeometry.fromPolygon([polyline]) )
            isolijnenProvider.addFeatures([isolijn])
    isolijnenlayer.updateExtents()
    return isolijnenlayer