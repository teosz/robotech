
/* ----- Copyright 2007 CNRS (VERIMAG) -------------------------------------
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
 * Projet Talk to NXT
 * -------------------------------------------------------------------------
 * module   : t2n.cc 
 *
 * date     : 2007-03-07 
 * auteurs  : Pascal Raymond
 *--------------------------------------------------------------------------
 * nature   : command-line pour accéder au port USB de la brique NXT 
 *            utilise la librairie libusb (http://libusb.sourceforge.net)
 *--------------------------------------------------------------------------
 * Modifs   :
 * -----------------------------------------------------------------------*/

#include <string.h>
#include <stdio.h>
#include "version.h"
#include "errors.h"
#include "ezargs.h"
#include "errormng.h"
#include "usb.h"
#include "usbmisc.h"
#include "usbnxt.h"

int main(int argc, const char* argv[]){

	//set_verbose_mode(2);

	//Récup des arguments ...
	EzArgs myargs(VERSION);
	bool do_battery, do_info, do_ls;
	bool v1, v2, v3;
	const char* ulfname;
	const char* dlfname;
	const char* rmfname;
	myargs.add_bool("-b", "check battery level", &do_battery);
	myargs.add_bool("-i", "print nxt info", &do_info);
	myargs.add_bool("-ls", "list files", &do_ls);
	myargs.add_string("-put", "<file.rxe>", "upload file", &ulfname, NULL);
	myargs.add_string("-get", "<file.rxe>", "download file", &dlfname, NULL);
	myargs.add_string("-rm", "<file>", "remove remote file", &rmfname, NULL);

	myargs.add_bool("-v", "set verbose mode", &v1);
	myargs.add_bool("-vv", "even more verbose", &v2);
	myargs.add_bool("-vvv", "gossip", &v3);
	myargs.parse(argc, argv);
	if(v1) set_verbose_mode();
	if(v2) set_verbose_mode(2);
	if(v3) set_verbose_mode(3);

	// Init brique 	
	UsbNxt zebrick;
	if (zebrick.init() != 0){
		Error(usbnxt_error());
	}
	Verbose("nxt brick found, usb initialized\n");

	if (do_battery) {
		int b = zebrick.battery_level();
		if (b < 0) Error(usbnxt_error());	
		printf("battery level = %dmV\n", b);
	}
	if (do_info) {
		int r = zebrick.print_infos();
		if (r < 0) Error(usbnxt_error());
	}
	if (do_ls) {
		int r = zebrick.list_files();
		if (r < 0) Error(usbnxt_error());
	}
	if (ulfname) {
		int r = zebrick.upload(ulfname);
		if (r < 0) Error(usbnxt_error());
	}
	if (dlfname) {
		int r = zebrick.download(dlfname);
		if (r < 0) Error(usbnxt_error());
	}
	if (rmfname) {
		int r = zebrick.remove(rmfname);
		if (r < 0) Error(usbnxt_error());
	}

	Verbose("that's all folks...\n");

}
