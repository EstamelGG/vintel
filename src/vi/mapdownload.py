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
import time

from vi.cache.cache import Cache
from PyQt4.QtCore import QThread
from vi import evegate
from six.moves import queue

import logging

class DownloadManage():
    _downloadThread = None
    def __init__(self):
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
        self._downloadThread = self.DownloadThread()
        self._downloadThread.start()
    def downloadMap(self, region):
        self._downloadThread.queue.put((region))
    class DownloadThread(QThread):
        queue = None
        def __init__(self):
            QThread.__init__(self)
            self.queue = queue.Queue()
            self.active = True

        def run(self):
            region = self.queue.get()
            self.download(region)

        def download(self, region):
            cache = Cache()
            DOTLAN_BASIC_URL = u"http://evemaps.dotlan.net/svg/{0}.svg"
            url = DOTLAN_BASIC_URL.format(region)
            try:
                logging.info("Download svg from {0}".format(url))
                content = requests.get(url, verify=False).text
                self.mapdownloadtextBrowser.append(u"Downloaded Map of Region: {0}".format(region))
            except:
                logging.critical("Fail download Map of Region: {0}".format(region))
                self.mapdownloadtextBrowser.append(u"Fail download Map of Region: {0}".format(region))
                return False
            if content:
                cache.putIntoCache("map_" + region, content, evegate.secondsTillDowntime() + 60 * 60)
            time.sleep(0.1)

