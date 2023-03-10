#
# Copyright (c) 2010 Mandriva
# Copyright (c) 2022 Siveo, http://siveo.net
#
# This file is part of python-systemd-dbus.
#
# python-systemd-dbus is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of
# the License, or (at your option) any later version.
#
# python-systemd-dbus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import dbus
import dbus.mainloop.glib
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

from systemd_dbus.property import Property
from systemd_dbus.exceptions import SystemdError

class Job(object):
    """Abstraction class to org.freedesktop.systemd1.Job interface"""
    def __init__(self, job_path):
        self.__bus = dbus.SystemBus()
        self.__proxy = self.__bus.get_object(
            'org.freedesktop.systemd1',
            job_path,
        )
        self.__interface = dbus.Interface(
            self.__proxy,
            'org.freedesktop.systemd1.Job',
        )

        self.__properties_interface = dbus.Interface(
            self.__proxy,
            'org.freedesktop.DBus.Properties')

        self.__properties_interface.connect_to_signal(
            'PropertiesChanged',
            self.__on_properties_changed)

        self.__properties()

    def __on_properties_changed(self, *args, **kargs):
        self.__properties()

    def __properties(self):
        properties = self.__properties_interface.GetAll(
            self.__interface.dbus_interface)
        attr_property =  Property()
        for key, value in properties.items():
            setattr(attr_property, key, value)
        setattr(self, 'properties', attr_property)

    def cancel(self):
        try:
            self.__interface.Cancel()
        except dbus.exceptions.DBusException as error:
            raise SystemdError(error)
