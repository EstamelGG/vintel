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

import datetime
import logging
import os
import time
import six
import re
if six.PY2:
    from io import open

from bs4 import BeautifulSoup
from vi import states
from PyQt4.QtGui import QMessageBox

from .parser_functions import parseStatus
from .parser_functions import parseUrls, parseShips, parseSystems

# Names the local chatlogs could start with (depends on l10n of the client)
LOCAL_NAMES = ("Local", "Lokal", six.text_type("\u041B\u043E\u043A\u0430\u043B\u044C\u043D\u044B\u0439"))


class ChatParser(object):
    """ ChatParser will analyze every new line that was found inside the Chatlogs.
    """

    def __init__(self, path, pathToGamelogs, rooms, high_values, systems):
        """ path = the path with the logs
            rooms = the rooms to parse"""
        self.path = path  # the path with the chatlog
        self.pathToGamelogs = pathToGamelogs  # the path with the chatlog
        self.rooms = rooms  # the rooms to watch (excl. local)
        self.high_values = high_values
        self.systems = systems  # the known systems as dict name: system
        self.fileData = {}  # informations about the files in the directory
        self.highValueData = {}  # informations about the files in the directory
        self.knownMessages = []  # message we allready analyzed
        self.locations = {}  # informations about the location of a char
        self.ignoredPaths = []
        self._collectInitFileData(path, pathToGamelogs)

    def _collectInitFileData(self, path, pathToGamelogs):
        currentTime = time.time()
        maxDiff = 60 * 60 * 24  # what is 1 day in seconds
        for filename in os.listdir(path):
            fullPath = os.path.join(path, filename)
            fileTime = os.path.getmtime(fullPath)
            if currentTime - fileTime < maxDiff:
                self.addFile(fullPath)

        for filename in os.listdir(pathToGamelogs):
            fullPath = os.path.join(pathToGamelogs, filename)
            fileTime = os.path.getmtime(fullPath)
            if currentTime - fileTime < maxDiff:
                self.addFile(fullPath)

    def addFile(self, path):  # read Local chat log
        lines = None
        content = ""
        filename = os.path.basename(path)
        if "logs\\Chatlogs" in path:
            roomname = ""
            if "_" in filename and len(filename.split("_")) >= 4:
                roomname = filename[::-1].split("_", 3)[3][::-1]  # GG edit, find roomname
            elif "_" in filename and len(filename.split("_")) == 3:
                roomname = filename[::-1].split("_", 2)[2][::-1]
            try:
                with open(path, "r", encoding='utf-16-le') as f:
                    content = f.read()
            except Exception as e:
                self.ignoredPaths.append(path)
                QMessageBox.warning(None, "Read a log file failed!", "File: {0} - problem: {1}".format(path, six.text_type(e)), "OK")
                return None

            lines = content.split("\n")
            if path not in self.fileData or (roomname in LOCAL_NAMES and "charname" not in self.fileData.get(path, [])):
                self.fileData[path] = {}
                if roomname in LOCAL_NAMES:
                    charname = None
                    sessionStart = None
                    # for local-chats we need more infos
                    for line in lines:
                        if "Listener:" in line:
                            charname = line[line.find(":") + 1:].strip()
                        elif "Session started:" in line:
                            sessionStr = line[line.find(":") + 1:].strip()
                            sessionStart = datetime.datetime.strptime(sessionStr, "%Y.%m.%d %H:%M:%S")
                        if charname and sessionStart:
                            self.fileData[path]["charname"] = charname
                            self.fileData[path]["sessionstart"] = sessionStart
                            break
            self.fileData[path]["lines"] = len(lines)
        elif "logs\\Gamelogs" in path:
            try:
                with open(path, "r", encoding='utf-8') as f:  # CCP create Gamelogs with utf-8 while chatlogs use utf-16
                    content = f.read()
            except Exception as e:
                self.ignoredPaths.append(path)
                QMessageBox.warning(None, "Read a log file failed!",
                                    "File: {0} - problem: {1}".format(path, six.text_type(e)), "OK")
                return None

            lines = content.split("\n")
            if path not in self.highValueData:
                self.highValueData[path] = {}
                charname = None
                sessionStart = None
                for line in lines:
                    if "Listener:" in line:
                        charname = line[line.find(":") + 1:].strip()
                    elif "Session started:" in line:
                        sessionStr = line[line.find(":") + 1:].strip()
                        sessionStart = datetime.datetime.strptime(sessionStr, "%Y.%m.%d %H:%M:%S")
                    if charname and sessionStart:
                        self.highValueData[path]["charname"] = charname
                        self.highValueData[path]["sessionstart"] = sessionStart
                        break
            self.highValueData[path]["lines"] = len(lines)
        return lines

    def GamelogTomessage(self,line):
        try:
            timeStart = line.find("[") + 1
            timeEnds = line.find("]")
            timeStr = line[timeStart:timeEnds].strip()
            timestamp = datetime.datetime.strptime(timeStr, "%Y.%m.%d %H:%M:%S")
            originalText = re.sub(u'\<.*?\>', '', line)
            message = Message("", "", timestamp, "", "", "", originalText, "")
        except:
            message = None
        if message:
            return message
    def _lineToMessage(self, line, roomname):
        # finding the timestamp
        timeStart = line.find("[") + 1
        timeEnds = line.find("]")
        timeStr = line[timeStart:timeEnds].strip()
        try:
            timestamp = datetime.datetime.strptime(timeStr, "%Y.%m.%d %H:%M:%S")
        except ValueError:
            return None
        # finding the username of the poster
        userEnds = line.find(">")
        username = line[timeEnds + 1:userEnds].strip()
        # finding the pure message
        text = line[userEnds + 1:].strip()  # text will the text to work an
        originalText = text
        formatedText = u"<rtext>{0}</rtext>".format(text)
        soup = BeautifulSoup(formatedText, 'html.parser')
        rtext = soup.select("rtext")[0]
        systems = set()
        upperText = text.upper()

        # KOS request
        if upperText.startswith("XXX "):
            return Message(roomname, text, timestamp, username, systems, upperText, status=states.KOS_STATUS_REQUEST)
        elif roomname.startswith("="):
            return Message(roomname, "xxx " + text, timestamp, username, systems, "XXX " + upperText, status=states.KOS_STATUS_REQUEST)
        elif upperText.startswith("VINTELSOUND_TEST"):
            return Message(roomname, text, timestamp, username, systems, upperText, status=states.SOUND_TEST)
        if roomname not in self.rooms:
            return None


        message = Message(roomname, "", timestamp, username, systems, text, originalText)
        # May happen if someone plays > 1 account
        if message in self.knownMessages:
            message.status = states.IGNORE
            return message

        while parseShips(rtext):
            continue
        while parseUrls(rtext):
            continue
        while parseSystems(self.systems, rtext, systems):
            continue
        parsedStatus = parseStatus(rtext)
        status = parsedStatus if parsedStatus is not None else states.ALARM

        # If message says clear and no system? Maybe an answer to a request?
        if status == states.CLEAR and not systems:
            maxSearch = 2  # we search only max_search messages in the room
            for count, oldMessage in enumerate(oldMessage for oldMessage in self.knownMessages[-1::-1] if oldMessage.room == roomname):
                if oldMessage.systems and oldMessage.status == states.REQUEST:
                    for system in oldMessage.systems:
                        systems.add(system)
                    break
                if count > maxSearch:
                    break
        message.message = six.text_type(rtext)
        message.status = status
        self.knownMessages.append(message)
        if systems:
            for system in systems:
                system.messages.append(message)
        return message

    def _parseLocal(self, path, line):
        message = []
        """ Parsing a line from the local chat. Can contain the system of the char
        """
        charname = self.fileData[path]["charname"]
        if charname not in self.locations:
            self.locations[charname] = {"system": "?", "timestamp": datetime.datetime(1970, 1, 1, 0, 0, 0, 0)}

        # Finding the timestamp
        timeStart = line.find("[") + 1
        timeEnds = line.find("]")
        timeStr = line[timeStart:timeEnds].strip()
        timestamp = None
        if time.strptime(timeStr, "%Y.%m.%d %H:%M:%S"):  # GG edit
            timestamp = datetime.datetime.strptime(timeStr, "%Y.%m.%d %H:%M:%S")
        else:
            try:
                timestamp = datetime.datetime.strptime(timeStr, "%Y.%m.%d %H:%M:%S")
            except Exception as e:
                return

        # Finding the username of the poster
        userEnds = line.find(">")
        username = line[timeEnds + 1:userEnds].strip()

        # Finding the pure message
        text = line[userEnds + 1:].strip()  # text will the text to work an
        if username in ("EVE-System", "EVE System"):
            if ":" in text:
                system = text.split(":")[1].strip().replace("*", "").upper()
                status = states.LOCATION
            else:
                # We could not determine if the message was system-change related
                system = "?"
                status = states.IGNORE
            if timestamp > self.locations[charname]["timestamp"]:
                self.locations[charname]["system"] = system
                self.locations[charname]["timestamp"] = timestamp
                message = Message("", "", timestamp, charname, [system, ], "", "", status)
        return message

    def fileModified(self, path):
        messages = []
        if path in self.ignoredPaths:
            return []
        if "logs\\Chatlogs" in path:
            # Checking if we must do anything with the changed file.
            # We only need those which name is in the rooms-list
            # EvE names the file like room_20140913_200737.txt, so we don't need
            # the last 20 chars
            filename = os.path.basename(path)
            roomname = ""
            if "_" in filename and len(filename.split("_")) >= 4:
                roomname = filename[::-1].split("_", 3)[3][::-1]  # GG edit, find roomname
            elif "_" in filename and len(filename.split("_")) ==3:
                roomname = filename[::-1].split("_", 2)[2][::-1]
            if path not in self.fileData:
                # seems eve created a new file. New Files have 12 lines header
                self.fileData[path] = {"lines": 13}
            oldLength = self.fileData[path]["lines"]
            lines = self.addFile(path)
            if path in self.ignoredPaths:
                return []
            for line in lines[oldLength - 1:]:
                line = line.strip()
                if len(line) > 2:
                    message = None
                    if roomname in LOCAL_NAMES:
                        message = self._parseLocal(path, line)
                    else:
                        message = self._lineToMessage(line, roomname)
                    if message:
                        messages.append(message)
        elif "logs\\Gamelogs" in path:
            if path not in self.highValueData:
                # seems eve created a new file. New Files have 5 lines header
                self.highValueData[path] = {"lines": 6}
            oldLength = self.highValueData[path]["lines"]
            lines = self.addFile(path)
            if path in self.ignoredPaths:
                return []
            for line in lines[oldLength - 1:]:
                line = line.strip()
                if "(combat)" in line[:36]:  #  only combat log
                    if isinstance(self.high_values,list) and len(self.high_values) > 0:
                        if "from" or "to" in line:
                            message = self.GamelogTomessage(line)
                            #message = None
                            #message = re.sub(u'\<.*?\>','',line)
                            if message:
                                messages.append(message)

        return messages


class Message(object):
    def __init__(self, room, message, timestamp, user, systems, upperText, plainText="", status=states.ALARM):
        self.room = room  # chatroom the message was posted
        self.message = message  # the messages text
        self.timestamp = timestamp  # time stamp of the massage
        self.user = user  # user who posted the message
        self.systems = systems  # list of systems mentioned in the message
        self.status = status  # status related to the message
        self.upperText = upperText  # the text in UPPER CASE
        self.plainText = plainText  # plain text of the message, as posted
        # if you add the message to a widget, please add it to widgets
        self.widgets = []

    def __key(self):
        return (self.room, self.plainText, self.timestamp, self.user)

    def __eq__(x, y):
        return x.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())
