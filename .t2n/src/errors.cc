
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
-------------------------------------------------------------------------*/
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <unistd.h>
#include "errors.h"

/********************************************************************
	Error, Warning, Verbose
*********************************************************************/

static int VERBOSE = 0;
static int PIPE = 0;
static char TOOL_NAME_DFLT[] = " ";
static const char* TOOL_NAME = TOOL_NAME_DFLT;

void set_verbose_mode(){ VERBOSE = 1; }
void set_pipe_mode(){ PIPE = 1; }
void set_verbose_mode(int i){ VERBOSE = i; }

void set_errors_tool_name(const char* tn){ TOOL_NAME = tn;}

int Verbose(const char* fmt ...){
	va_list args;
	va_start(args,fmt);

	if(VERBOSE){
		if ( PIPE && (fmt[0] == '\r')){
			fprintf(stderr, " \n^R" );
			vfprintf(stderr, &fmt[1], args);
		} else if ( PIPE && (fmt[0] == '\b' )){
			fprintf(stderr, "\n^B" );
			vfprintf(stderr, &fmt[1], args);
		} else {
			vfprintf(stderr,fmt,args);
		}
		fflush(stderr);
	}
	return VERBOSE;
}

int Verbose(int i, const char* fmt ...){
	va_list args;
	va_start(args,fmt);

	if(i <= VERBOSE){
		if ( PIPE && (fmt[0] == '\r')){
			fprintf(stderr, " \n^R" );
			vfprintf(stderr, &fmt[1], args);
		} else if ( PIPE && (fmt[0] == '\b' )){
			fprintf(stderr, "\n^B" );
			vfprintf(stderr, &fmt[1], args);
		} else {
			vfprintf(stderr,fmt,args);
		}
		fflush(stderr);
	}
	return VERBOSE;
}

int Verbose(){
	return VERBOSE;
}

/********************************************************************
	A "turning wheel" which makes a quarter cycle each "step" time
teh proc is called (only in verbose mode)
*********************************************************************/
static char WHEEL[] = { '|', '/', '-', '\\' };
static int WHEEL_INDEX = 0;
static int WHEEL_STEP = 1;
int VerboseWheel(int step){
	if((VERBOSE) && isatty(2)){
		if(WHEEL_STEP >= step){
			WHEEL_STEP = 0;
			fprintf(stderr,"%c\b", WHEEL[WHEEL_INDEX]);
			fflush(stderr);	
			WHEEL_INDEX = (WHEEL_INDEX+1)%4;
		} else {
			WHEEL_STEP++;
		}
	}
	return VERBOSE;
}

void IError(const char* fmt ...){
	va_list args;
	va_start(args,fmt);
	
	fprintf(stderr,"Sorry, Internal Error :\n");
	vfprintf(stderr,fmt,args);
	fprintf(stderr,"\n");
	
	exit(1);
}

void Error(const char* fmt ...){
	va_list args;
	va_start(args,fmt);
	
	fprintf(stderr,"%s Error :\n", TOOL_NAME);
	vfprintf(stderr,fmt,args);
	fprintf(stderr,"\n");
	
	exit(1);
}

void Warning(const char* fmt ...){
	va_list args;
	va_start(args,fmt);

	fprintf(stderr,"%s Warning :\n", TOOL_NAME);
	vfprintf(stderr,fmt,args);
	fprintf(stderr,"\n");

}

int AskYesNo(const char* fmt ...){
	va_list args;
	va_start(args,fmt);
	char prompt[1024];

	vsprintf(&prompt[0],fmt,args);
	char* b;
	size_t bsz;

	//char c;
	int r = 0;
	int s = 1;
	do {
		fprintf(stderr, "%s (y/n) ? ", prompt);
		fflush(stdout);
		b=NULL;
		bsz=0;
		int bl = getline(&b, &bsz, stdin);
		//remove ending "spaces" (thus newline) 
		char* p = &b[bl];
		do {
			p--;
		} while ((p != b) && (isspace(*p)));
		*(++p) = '\0';
//printf("\n\"%s\"\n%d\n\"", b, bl);
		r = -1;
		if(! strcmp(b, "y")) r = 1;
		else if (! strcmp(b, "n")) r = 0;
		else fprintf(stderr, "please answer y or n\n");
	} while ((s != 1) || (r == -1));

	return r;
}

static int nb_global_error = 0;

void GErrorRecover(){ 
	if(nb_global_error){
		fprintf(stderr,"*** %d Errors stop\n", nb_global_error);
		exit(1);
	}
}

int GErrors(){
	return nb_global_error;
}

void GError(const char* fmt ...){
	va_list args;
	va_start(args,fmt);

	vfprintf(stderr,fmt,args);
	nb_global_error++;
	
}

