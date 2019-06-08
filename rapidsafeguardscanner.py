#!/usr/bin/env python

'''
Company name : Rapidsafeguard
Author  : Punit Darji
Linked-in : punit-darji-5500
Twitter  : rapidsafeguard
instagram : Rapidsafeguard
Blog : www.easyhack.in
'''

from utilities.stenoLogging import *
log = get_logger('RSGScanner', path="./log/startup.log")
log.setLevel(logging.INFO)

# check for dependencies first (make sure all non-standard dependencies are checked for here)
try:
    from sqlalchemy.orm.scoping import ScopedSession as scoped_session
except ImportError as e:
    log.info("Import failed. SQL Alchemy library not found. If on Ubuntu or similar try: apt-get install python3-sqlalchemy*")
    log.info(e)
    exit(1)
    
try:
    from PyQt5 import QtWidgets, QtGui, QtCore
except ImportError as e:
    log.info("Import failed. PyQt5 library not found. If on Ubuntu or similar try: agt-get install python3-pyqt5")
    log.info(e)
    exit(1)

try:
    import quamash
    import asyncio 
except ImportError as e:
    log.info("Import failed. Quamash or asyncio not found.")
    log.info(e)
    exit(1)

try:
    import sys
    from colorama import init
    init(strip=not sys.stdout.isatty())
    from termcolor import cprint
    from pyfiglet import figlet_format
except ImportError as e:
    log.info("Import failed. One or more of the terminal drawing libraries not found.")
    log.info(e)
    exit(1)
    
from app.logic import *
from ui.gui import *
from ui.view import *
from controller.controller import *

# this class is used to catch events such as arrow key presses or close window (X)
class MyEventFilter(QObject):
    def eventFilter(self, receiver, event):
        # catch up/down arrow key presses in hoststable
        if(event.type() == QEvent.KeyPress and (receiver == view.ui.HostsTableView or receiver == view.ui.ServiceNamesTableView or receiver == view.ui.ToolsTableView or receiver == view.ui.ToolHostsTableView or receiver == view.ui.ScriptsTableView or receiver == view.ui.ServicesTableView or receiver == view.settingsWidget.toolForHostsTableWidget or receiver == view.settingsWidget.toolForServiceTableWidget or receiver == view.settingsWidget.toolForTerminalTableWidget)):
            key = event.key()
            if not receiver.selectionModel().selectedRows():
                return True
            index = receiver.selectionModel().selectedRows()[0].row()
            
            if key == QtCore.Qt.Key_Down:
                newindex = index + 1
                receiver.selectRow(newindex)
                receiver.clicked.emit(receiver.selectionModel().selectedRows()[0])

            elif key == QtCore.Qt.Key_Up:
                newindex = index - 1
                receiver.selectRow(newindex)
                receiver.clicked.emit(receiver.selectionModel().selectedRows()[0])

            elif QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier and key == QtCore.Qt.Key_C:    
                selected = receiver.selectionModel().currentIndex()
                clipboard = QtWidgets.QApplication.clipboard()
                clipboard.setText(selected.data().toString())

            return True
            
        elif(event.type() == QEvent.Close and receiver == MainWindow):
            event.ignore()
            view.appExit()
            return True
            
        else:      
            return super(MyEventFilter,self).eventFilter(receiver, event)   # normal event processing


# Main application declaration and loop
if __name__ == "__main__":
    
    cprint(figlet_format('RSG', font='starwars'), 'yellow', 'on_red', attrs=['bold'])

    app = QApplication(sys.argv)
    loop = quamash.QEventLoop(app)
    asyncio.set_event_loop(loop)

    myFilter = MyEventFilter()                      # to capture events
    app.installEventFilter(myFilter)
    MainWindow = QtWidgets.QMainWindow()
    #app.setWindowIcon(QIcon('./images/icons/Legion-N_128x128.svg'))
    app.setWindowIcon(QIcon('./images/icons/RSG.svg'))

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    try:
        qss_file = open('./ui/legion.qss').read()
    except IOError as e:
        log.info("The legion.qss file is missing. Your installation seems to be corrupted. Try downloading the latest version.")
        exit(0)

    MainWindow.setStyleSheet(qss_file)

    logic = Logic()                                 # Model prep (logic, db and models)
    view = View(ui, MainWindow)                     # View prep (gui)
    controller = Controller(view, logic)            # Controller prep (communication between model and view)
    view.qss = qss_file

    # Center the application in screen
    x = app.desktop().screenGeometry().center().x()
    y = app.desktop().screenGeometry().center().y()
    MainWindow.move(x - MainWindow.geometry().width()/2, y - MainWindow.geometry().height()/2)

    # Show main window
    MainWindow.show()

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    app.deleteLater()
    loop.close()
    sys.exit()
