# -*- coding: utf-8 -*-
import sys, math

def CirkelPunten(x, y, r):
    points = []
    numpoints = 72
    for i in range(numpoints):
        ang = float(i)/float(numpoints) * math.pi * 2
        points.append( (x + r * math.cos(ang), y + r * math.sin(ang)) )

    return points

def HalveCirkelPunten(x, y, r, hoek):
    points = []
    numpoints = 36
    for i in range(1, numpoints):
        ang = hoek - float(i)/float(2*numpoints) * math.pi * 2
        points.append( (x + r * math.cos(ang), y + r * math.sin(ang)) )

    return points

def BufferAfstandCabine(hb, hw, sterkte):
    if sterkte <= 0:
        afstand = sys.float_info.max
    else :
        Ab = (1.08 / (sterkte ** 0.71))
        if hb == hw:
            afstand = Ab
        else:
            Aw_sqr = Ab * Ab - (hw - hb) * (hw - hb)
            if Aw_sqr <= 0:
                afstand = 0
            else:
                afstand = math.sqrt(Aw_sqr)

    return afstand

def BufferAfstandTransformatieposten(hb, hw, sterkte):
    if sterkte <= 0:
        afstand = sys.float_info.max
    else :
        Ab = 11.5 - 7.10 * math.log(sterkte)
        if Ab <= 0:
            afstand = 0
        else:
            if hb == hw:
                afstand = Ab
            else:
                Aw_sqr = Ab * Ab - (hw - hb) * (hw - hb)
                if Aw_sqr <= 0:
                    afstand = 0
                else:
                    afstand = math.sqrt(Aw_sqr)

    return afstand

def BufferAfstandOndergrondseKabels(diepte, hw, sterkte, voltage, stroom, belasting):
    if sterkte <= 0:
        afstand = sys.float_info.max
    else :
        if voltage == 36:
            if stroom == 0:
                stroom = 936
            afstand = (stroom / 936.0) * (2.75 - 0.5 * math.fabs(diepte + hw)) * (belasting / 100.0) * math.pow(sterkte, -0.626)

        elif voltage == 70:
            if stroom == 0:
                stroom = 895
            afstand = (stroom / 895.0) * (3.27 - 0.5 * math.fabs(diepte + hw)) * (belasting / 100.0) * math.pow(sterkte, -0.68)

        elif voltage == 150:
            if stroom == 0:
                stroom = 1540
            afstand = (stroom / 1540.0) * (5.64 - 0.5 * math.fabs(diepte + hw)) * (belasting / 100.0) * math.pow(sterkte, -0.64)

        elif voltage == 380:
            if stroom == 0:
                stroom = 1790
            afstand = (stroom / 1790.0) * (6.97 - 0.5 * math.fabs(diepte + hw)) * (belasting / 100.0) * math.pow(sterkte, -0.64)

        else:
            afstand = 0

    return afstand

def BufferAfstandLuchtlijnen(hb, hw, sterkte, voltage, stroom, belasting):
    if sterkte <= 0:
        afstand = sys.float_info.max
    else :
        if voltage == 36:
            if stroom == 0:
                stroom = 450
            afstand = math.pow((stroom / 450.0), 0.5) * (24 - 0.6 * math.fabs(hb - hw)) * math.pow((belasting / 100.0), 0.5) * math.pow(sterkte, -0.5)

        elif voltage == 70:
            if stroom == 0:
                stroom = 750
            afstand = math.pow((stroom / 750.0), 0.5) * (33.57 - 0.6 * math.fabs(hb - hw)) * math.pow((belasting / 100.0), 0.5) * math.pow(sterkte, -0.5)

        elif voltage == 150:
            if stroom == 0:
                stroom = 1383
            afstand = math.pow((stroom / 1383.0), 0.5) * (55.70 - 0.6 * math.fabs(hb - hw)) * math.pow((belasting / 100.0), 0.5) * math.pow(sterkte, -0.5)

        elif voltage == 380:
            if stroom == 0:
                stroom = 2766
            afstand = math.pow((stroom / 2766.0), 0.5) * (142.3 - 0.6 * math.fabs(hb - hw)) * math.pow((belasting / 100.0), 0.5) * math.pow(sterkte, -0.5)

        else:
            afstand = 0

    return afstand

def FitParabool(x1, y1, x2, y2, x3, y3):
    if x1 == x2 and x1 == x3:
        a = 0.0
        b = 0.0
        c = (y1 + y2 + y3) / 3.0
    elif x1 == x2 or x1 == x3 or x2 == x3:
         a = 0.0
         b = (3.0 * (x1*y1 + x2*y2 + x3*y3) - (x1 + x2 + x3) * (y1 + y2 + y3)) / (3.0 * (x1*x1 + x2*x2 + x3*x3) - (x1 + x2 + x3) * (x1 + x2 + x3))
         c = ((y1 + y2 + y3) - b * (y1 + y2 + y3)) / 3.0
    else:
        a = ((y2-y1) * (x1 - x3) + (y3 - y1) * (x2 - x1)) / ((x1 - x3) * (x2*x2 - x1*x1) + (x2- x1) * (x3*x3 - x1*x1))
        b = ((y2 - y1) - a * (x2*x2 - x1*x1)) / (x2 - x1)
        c = y1 - a * x1*x1 - b * x1

    return (a, b, c)


def BerekenHoekBeta(p0, p1):
    """
    :param p0: QgsPoint or [x,y]
    :param p1: QgsPoint or [x,y]
    :return: beta
    """
    if p0[0] == p1[0]:
        # verticale lijn
        beta = 0
    elif p0[1] == p1[1]:
        # horizontale lijn
        beta = math.pi/2
    elif p0[1] > p1[1]:
        # lijn schuin naar onder
        alpha = math.atan(math.fabs((p1[1] - p0[1]) / (p1[0] - p0[0])))
        beta = math.pi/2 - alpha
    else:
        # lijn schuin naar boven
        alpha = math.atan(math.fabs((p1[0] - p0[0]) / (p1[1] - p0[1])))
        beta = math.pi/2 - alpha

    return beta


