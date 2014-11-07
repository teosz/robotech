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
   module   : errormng.cc
   date     : 30/08/2005
   auteurs  : Pascal Raymond

   modif    : 
----------------------------------------------------------------------------
Juste une petite couche pour récupérer propement
les messages d'erreurs système ...
--------------------------------------------------------------------------*/

#include "errormng.h"


ErrorMng::ErrorMng(const char* c){
	int l = sprintf(&_buff[0], "%s", c);
	_msg = &_buff[l];
}

void ErrorMng::set(const char* fmt ...){
	va_list args;
	va_start(args,fmt);
	vsprintf(_msg, fmt, args);
}

const char* ErrorMng::get(){
	return &_buff[0];
}
