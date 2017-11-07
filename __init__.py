# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AGRCGeocodingToolbox
                                 A QGIS plugin
 A QGIS plugin for geocoding addresses via api.mapserv.utah.gov (Utah-only addresses).
                             -------------------
        begin                : 2017-10-02
        copyright            : (C) 2017 by AGRC
        email                : stdavis@utah.gov
        git sha              : $Format:%H$
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


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load AGRCGeocodingToolbox class from file AGRCGeocodingToolbox.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .geocoding_toolbox import AGRCGeocodingToolbox
    return AGRCGeocodingToolbox(iface)
