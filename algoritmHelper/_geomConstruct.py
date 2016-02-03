# -*- coding: utf-8 -*-
from qgis.core import *
import math

def HalveCirkelPunten(x, y, r, hoek):
    points = []
    numpoints = 36
    for i in range(1, numpoints):
        ang = hoek - float(i)/float(2*numpoints) * math.pi * 2
        points.append( (x + r * math.cos(ang), y + r * math.sin(ang)) )

    return points

def HalveCirkel(p, q):
    if p.y() == q.y():
        alpha = 0
    else:
        alpha = math.atan((q.x() - p.x()) / (q.y() - p.y() ))

    if (q.y() > p.y() ) or (q.y() == p.y() and q.x() > p.x()):
        alpha = -math.pi/2 - alpha
    else:
        alpha = math.pi/2 - alpha

    punten = HalveCirkelPunten(p.x() + ((q.x() - p.x()) / 2), p.y() + ((q.y() - p.y() ) / 2),
                               math.sqrt((q.x() - p.x())*(q.x() - p.x()) + (q.y() - p.y() )*(q.y() - p.y() )) / 2, alpha)
    return punten

def PuntenNaarPolyLine(punten, sluit=False):
    polyline = QgsGeometry()
    pts = [QgsPoint(n[0], n[1]) for n in punten]

    if sluit:
        XY = QgsPoint(punten[0][0] , punten[0][1])
        pts.append(XY)

    polyline.addPart(pts)
    return polyline

def PuntenNaarPolygon(punten):
    polygon =  QgsGeometry()
    pts = [QgsPoint(n[0], n[1]) for n in punten]
    polygon.addPart(pts)
    return polygon

def BerekenRandPunten(p2, afstand, p0, p1, sin_beta, cos_beta):
    """
    :param p2: QgsPoint
    :param afstand: float
    :param p0: QgsPoint
    :param p1: QgsPoint
    :param sin_beta: float
    :param cos_beta: float
    :return:
    """
    if p0.x() == p1.x():
        # verticale lijn
        xr = afstand
        yr = 0
    elif p0.y() == p1.y():
        # horizontale lijn
        xr = 0
        yr = afstand
    elif p0.y() > p1.y():
        # lijn schuin naar onder
        xr = afstand * cos_beta
        yr = afstand * sin_beta
    else:
        # lijn schuin naar boven
        xr = afstand * sin_beta
        yr = afstand * cos_beta

    q_l = QgsPoint()
    q_r = QgsPoint()
    if p0.y() > p1.y():
        q_l.setX( p2.x() + xr )
        q_r.setX( p2.x() - xr )
    else:
        q_l.setX( p2.x() - xr )
        q_r.setX( p2.x() + xr )
    if p0.x() < p1.x():
        q_l.setY( p2.y() + yr )
        q_r.setY( p2.y() - yr )
    else:
        q_l.setY( p2.y() - yr )
        q_r.setY( p2.y() + yr )

    return (q_l, q_r)
