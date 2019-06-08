#!/usr/bin/env python

'''
Company name : Rapidsafeguard
Author  : Punit Darji
Twitter  : rapidsafeguard
instagram : Rapidsafeguard
Blog : www.easyhack.in
'''

import re
from PyQt5 import QtWidgets, QtGui, QtCore
from app.auxiliary import *                                                 # for bubble sort

class CvesTableModel(QtCore.QAbstractTableModel):
    
    def __init__(self, controller, cves = [[]], headers = [], parent = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.__headers = headers
        self.__cves = cves
        self.__controller = controller
        
    def setCves(self, cves):
        self.__cves = cves
        
    def getCves(self):
        return self.__cves

    def rowCount(self, parent):
        return len(self.__cves)

    def columnCount(self, parent):
        if not len(self.__cves) is 0:
            return len(self.__cves[0])
        return 0

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:            
            if orientation == QtCore.Qt.Horizontal:                
                if section < len(self.__headers):
                    return self.__headers[section]
                else:
                    return "not implemented"
                
    def data(self, index, role):                                        # this method takes care of how the information is displayed

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:                               # how to display each cell
            value = ''
            row = index.row()
            column = index.column()
            if column == 0:
                value = self.__cves[row]['name']
            elif column == 1:
                value = self.__cves[row]['severity']
            elif column == 2:
                value = self.__cves[row]['product']
            elif column == 3:
                value = self.__cves[row]['version']
            elif column == 4:
                value = self.__cves[row]['url']
            elif column == 5:
                value = self.__cves[row]['source']
            elif column == 6:
                value = self.__cves[row]['exploitId']
            elif column == 7:
                value = self.__cves[row]['exploit']
            elif column == 8:
                value = self.__cves[row]['exploitUrl']
            return value
                    

    def sort(self, Ncol, order):
        self.layoutAboutToBeChanged.emit()
        array=[]
        
        if Ncol == 0:            
            for i in range(len(self.__cves)):
                array.append(self.__cves[i]['name'])
        elif Ncol == 1:
            for i in range(len(self.__cves)):
                array.append(self.__cves[i]['severity'])
        elif Ncol == 2:
            for i in range(len(self.__cves)):
                array.append(self.__cves[i]['product'])
        elif Ncol == 3:
            for i in range(len(self.__cves)):
                array.append(self.__cves[i]['version'])
        elif Ncol == 4:
            for i in range(len(self.__cves)):
                array.append(self.__cves[i]['url'])
        elif Ncol == 5:
            for i in range(len(self.__cves)):
                array.append(self.__cves[i]['source'])
        elif Ncol == 6:
            for i in range(len(self.__cves)):
                array.append(self.__cves[i]['exploitId'])
        elif Ncol == 7:
            for i in range(len(self.__cves)):
                array.append(self.__cves[i]['exploit'])
        elif Ncol == 8:
            for i in range(len(self.__cves)):
                array.append(self.__cves[i]['exploitUrl'])

        sortArrayWithArray(array, self.__cves)                       # sort the services based on the values in the array

        if order == Qt.AscendingOrder:                                  # reverse if needed
            self.__cves.reverse()
            
        self.layoutChanged.emit()

    def flags(self, index):                                             # method that allows views to know how to treat each item, eg: if it should be enabled, editable, selectable etc
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    ### getter functions ###

    def getCveDBIdForRow(self, row):
        return self.__cves[row]['name']

    def getCveForRow(self, row):
        return self.__cves[row]
    
    def getRowForDBId(self, id):
        for i in range(len(self.__cves)):
            if self.__cves[i]['name'] == id:
                return i
