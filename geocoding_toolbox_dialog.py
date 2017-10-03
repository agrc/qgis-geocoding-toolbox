# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AGRCGeocodingToolboxDialog
                                 A QGIS plugin
 This plugin provides tools for geocoding addresses using AGRC's web services.
                             -------------------
        begin                : 2017-10-02
        git sha              : $Format:%H$
        copyright            : (C) 2017 by AGRC
        email                : stdavis@utah.gov
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import csv
import os

from geocode_address_table import UNIQUE_RUN, TableGeocoder
from PyQt4 import QtGui, uic
from PyQt4.QtGui import QFileDialog

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'geocoding_toolbox_dialog_base.ui'))


class AGRCGeocodingToolboxDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(AGRCGeocodingToolboxDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        # clear and set up file and folder pickers
        self.outputFolderEdit.clear()
        self.outputFolderButton.clicked.connect(self.select_output_folder)
        self.addressTableEdit.clear()
        self.addressTableButton.clicked.connect(self.select_address_table)

        self.locatorComboBox.addItems(TableGeocoder.locatorMap.keys())
        self.spatialRefComboBox.addItems(TableGeocoder.spatialRefMap.keys())

    def get_parameters(self):
        return {
            'apiKey': self.apiKeyEdit.text(),
            'inputTable': self.addressTableEdit.text(),
            'idField': self.idFieldComboBox.currentText(),
            'addressField': self.addressFieldComboBox.currentText(),
            'zoneField': self.zoneFieldComboBox.currentText(),
            'locator': self.locatorComboBox.currentText(),
            'spatialRef': self.spatialRefComboBox.currentText(),
            'outputDir': self.outputFolderEdit.text(),
            'outputFileName': 'GeocodeResults_' + UNIQUE_RUN + '.csv'
        }

    def select_output_folder(self):
        folder = str(QFileDialog.getExistingDirectory(self, "Select output directory"))
        self.outputFolderEdit.setText(folder)

    def select_address_table(self):
        filepath = str(QFileDialog.getOpenFileName(self, "Select CSV", filter="*.csv"))
        self.addressTableEdit.setText(filepath)

        # get field names from CSV to populate field drop downs
        with open(filepath, 'rb') as csvfile:
            first_line = csvfile.readline()
            dialect = csv.Sniffer().sniff(first_line)
            csvfile.seek(0)
            if csv.Sniffer().has_header(first_line):
                csvfile.seek(0)
                reader = csv.reader(csvfile, dialect)
                headers = reader.next()
                for field_picker in [self.idFieldComboBox, self.addressFieldComboBox, self.zoneFieldComboBox]:
                    field_picker.addItems(headers)
            else:
                # TODO
                pass
