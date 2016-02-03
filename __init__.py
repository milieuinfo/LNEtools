# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LNEtools
                                 A QGIS plugin
 LNE-tools voor QGIS
                              -------------------
        begin                : 2016-01-27
        copyright            : (C) 2016 by Kay Warrie
        email                : kaywarrie@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

__author__ = 'Kay Warrie'
__date__ = '2016-01-27'
__copyright__ = '(C) 2016 by Kay Warrie'


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load LNEtools class from file LNEtools.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .LNEtools import LNEtoolsPlugin
    return LNEtoolsPlugin()
