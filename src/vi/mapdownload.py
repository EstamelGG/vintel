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

import requests

from vi.cache.cache import Cache
from PyQt4.QtCore import QThread
from vi import evegate
from six.moves import queue
from PyQt4 import QtGui
import logging
from vi import dotlan

class DownloadManage(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.ui = parent
        self.DOTLAN_BASIC_URL = u"http://evemaps.dotlan.net/svg/{0}.svg"
        self.Regions = ["Aridia", "Black Rise", "The Bleak Lands", "Branch", "Cache", "Catch", "The Citadel",
                        "Cloud Ring", "Cobalt Edge", "Curse", "Deklein", "Delve", "Derelik", "Detorid", "Devoid",
                        "Domain", "Esoteria", "Essence", "Etherium Reach", "Everyshore", "Fade", "Feythabolis",
                        "The Forge", "Fountain", "Geminate", "Genesis", "Great Wildlands", "Heimatar", "Immensea",
                        "Impass",
                        "Insmother", "Kador", "The Kalevala Expanse", "Khanid", "Kor-Azor", "Lonetrek", "Malpais",
                        "Metropolis",
                        "Molden Heath", "Oasa", "Omist", "Outer Passage", "Outer Ring", "Paragon Soul",
                        "Period Basis",
                        "Perrigen Falls", "Placid", "Pochven", "Providence", "Pure Blind", "Querious",
                        "Scalding Pass",
                        "Sinq Laison", "Solitude", "The Spire", "Stain", "Syndicate", "Tash-Murkon", "Tenal",
                        "Tenerifis", "Tribute", "Vale of the Silent", "Venal", "Verge Vendor", "Wicked Creek"]
        self._downloadThread = self.DownloadThread(self)
        self._downloadThread.start()

    def quit(self):
        self._downloadThread.quit()

    def downloadMap(self):
        for region in self.Regions:
            self._downloadThread.queue.put((region))
        results = []
        global active
        while True:
            if active:
                if self._downloadThread.result_queue.qsize() > len(results):
                    result = self._downloadThread.result_queue.get()
                    result_succ = result.split(":")[1]
                    self.ui.downloadMapProgressBar.setValue(100 * len(results) / len(self.Regions))
                    if result_succ == "1":
                        self.ui.mapdownloadtextBrowser.append(u"Downloaded Map of Region: {0}".format(result.split(":")[0]))
                    elif result_succ == "0":
                        self.ui.mapdownloadtextBrowser.append(u"Fail download Map of Region: {0}".format(result.split(":")[0]))
                    QtGui.QApplication.processEvents()
                    if len(result) > 0:
                        results.append(result)
                    if len(results) == len(self.Regions):
                        break
                else:
                    QtGui.QApplication.processEvents()
            else:
                break

    class DownloadThread(QThread):
        queue = None
        active = 1
        def __init__(self, parent):
            QThread.__init__(self)
            QtGui.QDialog.__init__(self, parent)
            self.ui = parent
            self.queue = queue.Queue()
            self.result_queue = queue.Queue()
            global active
            active = 1

        def run(self):
            global active
            while True:
                if active:
                    region = self.queue.get()
                    if region is not None:
                        self.ui.ui.mapdownloadlabel.setText(u"Downloading Map of: {0}".format(region))
                        self.download(region)
                else:
                    break
            QThread.quit(self)
        def quit(self):
            global active
            active = 0
            self.queue.put(None)
            QThread.quit(self)

        def download(self, region):
            cache = Cache()
            DOTLAN_BASIC_URL = u"http://evemaps.dotlan.net/svg/{0}.svg"
            content = ""
            region = dotlan.convertRegionName(region)
            url = DOTLAN_BASIC_URL.format(region)
            logging.info("Downloading svg from {0}".format(url))
            try:
                content = requests.get(url, verify=False).text
                self.result_queue.put(region + ":1")
            except:
                logging.critical("Fail download Map of Region: {0}".format(region))
                self.result_queue.put(region + ":0")
                content = None
            if content:
                cache.putIntoCache("map_" + region, content, evegate.secondsTillDowntime() + 60 * 60)

