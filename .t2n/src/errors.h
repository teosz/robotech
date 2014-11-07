/*-------------------------------------------------------------------------
Copyright 1996,2005 CNRS (VERIMAG)
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
  	module   : errors.h
   date     : 25/11/1996 
   auteurs  : Pascal Raymond
----------------------------------------------------------------------------
   nature :  Gestion des erreurs et des messages (sur stderr) :
----------------------------------------------------------------------------
	(C = constructeur, M = methode, F = fonction)
-----------------------------------------------------
F  set_errors_tool_name(char*)     Definit un prefixe aux messages d'erreur
F  IError(char* fmt, ...)          'internal error' et exit  
F  Error(char* fmt, ...)           'error' et exit  
F  GError(char* fmt, ...)          'error' sans exit
F  GErrors()                       Le nombre d'appel de GError
F  GErrorRecover()                 Exit si GError avant 
F  Warning(char* fmt, ...)         'warning' (sans exit)
F  set_verbose_mode()              Passe en mode verbeux niveau 1
F  set_verbose_mode(int i)         Passe en mode verbeux niveau i
                                      (0 pour non-verbeux)
F  int Verbose()                   Le mode verbeux courant
F  Verbose(char* fmt, ...)         Affiche message si mode verbeux >= 1
F  Verbose(int i, char* fmt, ...)  Affiche message si mode verbeux >= i 
----------------------------------------------------------------------------
   modifs :

--------------------------------------------------------------------------*/


#ifndef __PR_ERRORS_H
#define __PR_ERRORS_H

extern void IError(const char* fmt, ...);
extern void Error(const char* fmt, ...);
extern void GError(const char* fmt, ...);
extern int GErrors();
extern void GErrorRecover();
extern void Warning(const char* fmt, ...);
extern void set_errors_tool_name(const char* tn);
extern void set_verbose_mode();
extern void set_pipe_mode();
extern void set_verbose_mode(int i);
extern int Verbose(const char* fmt, ...);
extern int Verbose(int i, const char* fmt, ...);
extern int Verbose();
extern int AskYesNo(const char* fmt, ...);
#define VERBOSE(X,Y) {if(Verbose() >= X) { Y; }}

extern int VerboseWheel(int step);

#endif
