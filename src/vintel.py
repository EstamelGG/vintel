#!/usr/bin/env python
###########################################################################
#  Vintel - Visual Intel Chat Analyzer									  #
#  Copyright (C) 2014-15 Sebastian Meyer (sparrow.242.de+eve@gmail.com )  #
#																		  #
#  This program is free software: you can redistribute it and/or modify	  #
#  it under the terms of the GNU General Public License as published by	  #
#  the Free Software Foundation, either version 3 of the License, or	  #
#  (at your option) any later version.									  #
#																		  #
#  This program is distributed in the hope that it will be useful,		  #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of		  #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the		  #
#  GNU General Public License for more details.							  #
#																		  #
#																		  #
#  You should have received a copy of the GNU General Public License	  #
#  along with this program.	 If not, see <http://www.gnu.org/licenses/>.  #
###########################################################################

import sys
import os
import logging
import traceback

from logging.handlers import RotatingFileHandler
from logging import StreamHandler

from PyQt4 import QtGui
from vi import version
from vi.ui import viui, systemtray
from vi.cache import cache
from vi.resources import resourcePath
from vi.cache.cache import Cache
from PyQt4.QtGui import QApplication, QMessageBox


def exceptHook(exceptionType, exceptionValue, tracebackObject):
    """
        Global function to catch unhandled exceptions.
    """
    try:
        logging.critical("-- Unhandled Exception --")
        logging.critical(''.join(traceback.format_tb(tracebackObject)))
        logging.critical('{0}: {1}'.format(exceptionType, exceptionValue))
        logging.critical("-- ------------------- --")
    except Exception:
        pass

sys.excepthook = exceptHook
backGroundColor = "#c6d9ec"


class Application(QApplication):

    def __init__(self, args):
        super(Application, self).__init__(args)

        # Set up paths
        chatLogDirectory = ""
        gameLogDirectory = ""
        if len(sys.argv) > 2:
            chatLogDirectory = sys.argv[1]
            gameLogDirectory = sys.argv[2]

        if not os.path.exists(chatLogDirectory) or not os.path.exists(gameLogDirectory):
            if sys.platform.startswith("darwin"):
                chatLogDirectory = os.path.join(os.path.expanduser("~"), "Documents", "EVE", "logs", "Chatlogs")
                gameLogDirectory = os.path.join(os.path.expanduser("~"), "Documents", "EVE", "logs", "Gamelogs")
                if not os.path.exists(chatLogDirectory):
                    chatLogDirectory = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "Eve Online", "p_drive", "User", "My Documents", "EVE", "logs", "Chatlogs")
                    gameLogDirectory = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "Eve Online", "p_drive", "User", "My Documents", "EVE", "logs", "Gamelogs")
            elif sys.platform.startswith("linux"):
                chatLogDirectory = os.path.join(os.path.expanduser("~"), "EVE", "logs", "Chatlogs")
                gameLogDirectory = os.path.join(os.path.expanduser("~"), "EVE", "logs", "Gamelogs")
            elif sys.platform.startswith("win32") or sys.platform.startswith("cygwin"):
                import ctypes.wintypes
                buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
                ctypes.windll.shell32.SHGetFolderPathW(0, 5, 0, 0, buf)
                documentsPath = buf.value
                chatLogDirectory = os.path.join(documentsPath, "EVE", "logs", "Chatlogs")
                gameLogDirectory = os.path.join(documentsPath, "EVE", "logs", "Gamelogs")
        if not os.path.exists(chatLogDirectory) or not os.path.exists(gameLogDirectory) :
            # None of the paths for logs exist, bailing out
            QMessageBox.critical(None, "No path to Logs", "No logs found at: " + chatLogDirectory, "Quit")
            QMessageBox.critical(None, "No path to Logs", "No logs found at: " + gameLogDirectory, "Quit")
            sys.exit(1)

        # Setting local directory for cache and logging
        vintelDirectory = os.path.join(os.path.dirname(os.path.dirname(chatLogDirectory)), "vintel")
        if not os.path.exists(vintelDirectory):
            os.mkdir(vintelDirectory)
        cache.Cache.PATH_TO_CACHE = os.path.join(vintelDirectory, "cache-2.sqlite3")

        vintelLogDirectory = os.path.join(vintelDirectory, "logs")
        if not os.path.exists(vintelLogDirectory):
            os.mkdir(vintelLogDirectory)

        splash = QtGui.QSplashScreen(QtGui.QPixmap(resourcePath("vi/ui/res/logo.png")))

        vintelCache = Cache()
        logLevel = vintelCache.getFromCache("logging_level")
        if not logLevel:
            #logLevel = logging.WARN
            logLevel = logging.INFO
        backGroundColor = vintelCache.getFromCache("background_color")
        if backGroundColor:
            self.setStyleSheet("QWidget { background-color: %s; }" % backGroundColor)

        splash.show()
        self.processEvents()

        # Setup logging for console and rotated log files
        formatter = logging.Formatter('%(asctime)s| (%(levelname)s) |%(message)s', datefmt='%m/%d %I:%M:%S')
        rootLogger = logging.getLogger()
        rootLogger.setLevel(level=logLevel)

        logFilename = vintelLogDirectory + "/output.log"
        fileHandler = RotatingFileHandler(maxBytes=(1048576*5), backupCount=7, filename=logFilename, mode='a')
        fileHandler.setFormatter(formatter)
        rootLogger.addHandler(fileHandler)

        consoleHandler = StreamHandler()
        consoleHandler.setFormatter(formatter)
        rootLogger.addHandler(consoleHandler)

        logging.critical("")
        logging.critical("------------------- Vintel %s starting up -------------------", version.VERSION)
        logging.critical("")
        logging.debug("Looking for chat logs at: %s", chatLogDirectory)
        logging.debug("Looking for game logs at: %s", gameLogDirectory)
        logging.debug("Cache maintained here: %s", cache.Cache.PATH_TO_CACHE)
        logging.debug("Writing logs to: %s", vintelLogDirectory)

        trayIcon = systemtray.TrayIcon(self)
        trayIcon.show()
        self.mainWindow = viui.MainWindow(chatLogDirectory, gameLogDirectory, trayIcon, backGroundColor)
        self.mainWindow.show()
        self.mainWindow.raise_()
        splash.finish(self.mainWindow)


# The main application
if __name__ == "__main__":

    app = Application(sys.argv)
    sys.exit(app.exec_())

