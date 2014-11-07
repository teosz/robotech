/*-------------------------------------------------------------------------
Copyright 2005 CNRS (VERIMAG) 
--------------------------------------------------------------------------------
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
--------------------------------------------------------------------------------

VERIMAG - Synchrone TOOLBOX
---------------------------------------------------------------------------
   module   : usbscan.cc
   date     : 30/08/2005
   auteurs  : Pascal Raymond

   modif    : 
----------------------------------------------------------------------------
test de scan sur un port usb ...
--------------------------------------------------------------------------*/
#include "usb.h"
#include <string.h>
#include <stdio.h>

// USB Générique : recherche d'un device particulier
struct usb_device* find_usb_dev(
	u_int16_t vendor,
	u_int16_t product
){
	struct usb_bus *busses, *bus;
	struct usb_device *devs, *d;
	u_int16_t v, p;

	usb_init();
	usb_find_busses();
	usb_find_devices();
	busses = usb_get_busses();
	for(bus = busses; bus;  bus = bus->next){
		printf("bus dirname=%s\n", bus->dirname);
		devs = bus->devices;
		for(d=devs; d; d=d->next){
			v = d->descriptor.idVendor;
			p = d->descriptor.idProduct;
			printf("  dev filename=%s, vendor=0x%04x, product=0x%04x\n",
				d->filename, v, p
			);
			if((v == vendor) && (p==product)) return d;
		}
	}
	return NULL;
}

int main(){
	struct usb_device *d;
	d = find_usb_dev(-1,-1);
	return 0;
}
