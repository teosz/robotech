
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
   module   : errormng.h
   date     : 30/08/2005
   auteurs  : Pascal Raymond

   modif    : 
----------------------------------------------------------------------------
Juste une petite couche pour récupérer propement
les messages d'erreurs système ...
--------------------------------------------------------------------------*/

#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>

#define ErrorMngBuffSize 512

class ErrorMng {
	char _buff[ErrorMngBuffSize];
	char* _msg; 
	int _msgsz;
	char* _class;
public:
	ErrorMng(const char* c);
	void set(const char* fmt ...);
	const char* get();
};


