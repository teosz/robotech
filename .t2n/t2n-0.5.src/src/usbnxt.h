
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
 * module   : usbnxt.h 
 *
 * date     : 2007-03-07 
 * auteurs  : Pascal Raymond
 *--------------------------------------------------------------------------
 * nature   : Classe dérivée de UsbHandle, spécialement dédiée à la brique nxt.
 *--------------------------------------------------------------------------
 * Modifs   :
 * -----------------------------------------------------------------------*/

//  Message d'erreurs de la lib ...
extern const char* usbnxt_error();

class UsbNxt : public UsbHandle {
	int _fails(const char* c);
	//utile : récupère un descripteur de fichier
	int _unpack_filedesc(
		const char* fmsg,
   	char* pstatus,
   	char* pcmdhdl,
		char* pfnme, int* pfsz
	);
	//utile: teste l'existence d'un fichier
	bool _file_exists(const char* nme);
	int _file_delete(const char* nme);
public :
	UsbNxt();
	int init();

// Informations :
	int battery_level();
	int print_infos();
	int list_files();
	int upload(const char* fname);
	int download(const char* fname);
	int remove(const char* fname);
};
