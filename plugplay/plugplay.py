# -*- Mode: python; coding: utf-8; 
#
# Copyright (C) 2014 - t3pleni9
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA.


import socket,os
import sys,signal
import dbus


from threading import Thread
from gi.repository import GObject, RB, Peas
class PlugPlay (GObject.Object, Peas.Activatable):
    object = GObject.property(type=GObject.Object)

    def __init__(self):
        super(PlugPlay, self).__init__()
        

    def do_activate(self):        
        self.shell = self.object
        self.db = self.shell.props.db
        self.player = self.shell.props.shell_player
        self.player.do_next()
                
        self.t = MyThread(self.shell)
        self.t.daemon = True
        self.t.start()
        
    def do_deactivate(self):      

        self.player = None
        self.shell = None
        self.db = None
        #del self.str
        del self.t
        
class MyThread(Thread):
    def __init__(self, RBShell):
        super(MyThread, self).__init__()
        self.s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.shell = RBShell
        self.player = RBShell.props.shell_player
        self.db = self.shell.props.db
        self.s.connect("/var/run/acpid.socket")
        
    def run(self):
        while(1):            
            try:
                self.buff = self.s.recv(4096)                
                print "Received: ",self.buff
                if "HEADPHONE plug" in self.buff:
                    if self.player.get_playing_entry():
                        print("In If")
                        self.player.play()
                    else:                               #First time play. Start by play pause.
                        self.player.playpause(True)
                elif "HEADPHONE unplug" in self.buff:
                    print( self.player.get_playing_entry())
                    self.player.pause()
            except Exception, e:
                print "Receiving failed! Assuming disconnection.", str(e)
                break
