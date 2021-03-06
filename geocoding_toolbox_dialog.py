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
from functools import partial

from geocode_address_table import UNIQUE_RUN, TableGeocoder
from PyQt4 import QtGui, uic
from PyQt4.QtCore import QSettings
from PyQt4.QtGui import QFileDialog
from qgis.utils import showPluginHelp

SETTINGS_API_KEY = 'agrc_geocoding/apikey'
SETTINGS_ADDRESS_TABLE = 'agrc_geocoding/addresstable'
SETTINGS_OUTPUT_FOLDER = 'agrc_geocoding/outputfolder'
SETTINGS_ID_FIELD = 'agrc_geocoding/idfield'
SETTINGS_ADDRESS_FIELD = 'agrc_geocoding/addressfield'
SETTINGS_ZONE_FIELD = 'agrc_geocoding/zonefield'
SETTINGS_LOCATOR = 'agrc_geocoding/locator'
SETTINGS_SPATIAL_REFERENCE = 'agrc_geocoding/spatialreference'

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

        self.showHelpButton.clicked.connect(partial(showPluginHelp, None, filename='help/index'))

        # insert cached values, if any
        s = QSettings()
        self.apiKeyEdit.setText(s.value(SETTINGS_API_KEY))
        addressTableValue = s.value(SETTINGS_ADDRESS_TABLE)
        if addressTableValue is not None:
            self.addressTableEdit.setText(addressTableValue)
            self.update_field_names(addressTableValue, True)
        self.outputFolderEdit.setText(s.value(SETTINGS_OUTPUT_FOLDER))

        self.locatorComboBox.addItems(TableGeocoder.locatorMap.keys())
        locatorValue = s.value(SETTINGS_LOCATOR)
        if locatorValue is not None:
            self.locatorComboBox.setCurrentIndex(TableGeocoder.locatorMap.keys().index(locatorValue))
        self.spatialRefComboBox.addItems(TableGeocoder.spatialRefMap.keys())
        spatialRefValue = s.value(SETTINGS_SPATIAL_REFERENCE)
        if spatialRefValue is not None:
            self.spatialRefComboBox.setCurrentIndex(TableGeocoder.spatialRefMap.keys().index(spatialRefValue))

    def get_parameters(self):
        # set global settings for use the next time
        s = QSettings()
        s.setValue(SETTINGS_API_KEY, self.apiKeyEdit.text())
        s.setValue(SETTINGS_ADDRESS_TABLE, self.addressTableEdit.text())
        s.setValue(SETTINGS_OUTPUT_FOLDER, self.outputFolderEdit.text())
        s.setValue(SETTINGS_ID_FIELD, self.idFieldComboBox.currentText())
        s.setValue(SETTINGS_ADDRESS_FIELD, self.addressFieldComboBox.currentText())
        s.setValue(SETTINGS_ZONE_FIELD, self.zoneFieldComboBox.currentText())
        s.setValue(SETTINGS_LOCATOR, self.locatorComboBox.currentText())
        s.setValue(SETTINGS_SPATIAL_REFERENCE, self.spatialRefComboBox.currentText())

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

        self.update_field_names(filepath)

    def update_field_names(self, filepath, is_init=False):
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
                raise Exception('CSV file has no headers!')

        if is_init:
            s = QSettings()

            mappings = [[SETTINGS_ID_FIELD, self.idFieldComboBox],
                        [SETTINGS_ADDRESS_FIELD, self.addressFieldComboBox],
                        [SETTINGS_ZONE_FIELD, self.zoneFieldComboBox]]
            for setting, combobox in mappings:
                value = s.value(setting, False)
                if value:
                    combobox.setCurrentIndex(headers.index(value))
