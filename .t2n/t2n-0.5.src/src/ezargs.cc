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
   module   : ezargs.cc
   date     : 30/08/2005
   auteurs  : Pascal Raymond
----------------------------------------------------------------------------
   nature :  Classe EzArgss, pour faciliter la gestion des arguments
      de commande (argc, argv). 
--------------------------------------------------------------------------*/
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <sys/types.h>
#include <unistd.h>
#include <libgen.h>

#include "errors.h"
#include "ezargs.h"

//LES LISTES NE SE CONSTRUISENT QUE PAR
//DES APPEND !!
class EzArgsToken {
protected:
	const char* _key;
	const char* _param;
	const char* _man;
	EzArgsToken* _next;
	EzArgsToken* _last_known;
	EzArgsToken* last(){
		while(_last_known->_next){
			_last_known = _last_known->_last_known;
		}
		return _last_known;
	}
public:
	EzArgsToken* next(){ return _next; }
	EzArgsToken(
		const char* key,
		const char* par,
		const char* man
	){
		_key = key;
		_param = par;
		_man = man;
		_next = NULL;
		_last_known = this;
	}
	EzArgsToken* append(EzArgsToken* a){
		if(this){
			last()->_next = a;
			_last_known = a;
			return this;
		} else {
			return a;
		}
	}
	virtual const char** local_accept(const char** av){
		Error("EzArgsToken::local_accept purely virtual");
		return NULL;
	}
	//accept récursif en commencant par le début
	const char** accept(const char** av){
		const char** res = local_accept(av);
		if (res) return res;
		else if(_next) return _next->accept(av);
		else return NULL;
	}
	void dump(){
		int prec = -10+strlen(_key);
		if(prec > 0) prec = 0;
		printf("  %s %*s : %s\n", _key, prec,
			(_param)? _param : (char*)"",
			(_man)? _man : (char*)""	
		);
		if(_next) _next->dump();
	}
   //juste les params sur la même ligne ...
   void dump_param(){
      if(! this) return;
      if(_param) printf("%s ", _param);
      if(_next) _next->dump_param();
   }
};

class EzArgsTokenBool: public EzArgsToken {
	bool* _ptr;
public:
	EzArgsTokenBool(const char* key, const char* man,bool* r)
		:EzArgsToken(key,NULL,man)
	{
		_ptr = r;
		*r = false;
	}
	const char** local_accept(const char** av){
		if(! av) return NULL;
		if(!strcmp(*av, _key)){
			*_ptr = true;	
			return av;
		} else {
			return NULL;
		} 
	}
};

class EzArgsTokenString: public EzArgsToken {
	const char** _ptr;
public:
	EzArgsTokenString(
		const char* key,
		const char* par,
		const char* man,
		const char** r,
		const char* dflt) : EzArgsToken(key,par,man)
	{
		_ptr = r;
		*_ptr = dflt;
	}
	const char** local_accept(const char** av){
		if(! av) return NULL;
		if(!strcmp(*av, _key)){
			av++;
			if(*av ) {
				*_ptr = *av;
				return av;
			}
			Error("EzArgs: string expected after '%s' option\n", _key);
			return NULL;
		} else {
			return NULL;
		} 
	}
};

typedef const char* cstring;

//Les "extra" stockent des args sans clé
class EzArgsExtra : public EzArgsToken {
	const char** _ptr;
	bool _used;
public:
	EzArgsExtra(
		const char* par,
		const char* man,
		//const char** r,
		const char** r,
		const char* dflt
	) :EzArgsToken("", par, man)
	{
		_ptr = r;
		*r = dflt;
		_used = false;
	}
	//accepte uniquement s'il est le premier libre !
	const char** local_accept(const char** av){
		if(!av) return NULL;
		if(_used) return NULL;
		else {
			*_ptr = *av;
			_used = true;
			return av;
		}
	}
};
inline bool myatoi(const char* src, int* ptr){
	long x;
	char* e;
	x = strtol(src, &e, 10);
	*ptr = (int)x;
	return (*e == '\0');
}

class EzArgsTokenInt: public EzArgsToken {
	int* _ptr;
	bool* _sptr;
public:
	EzArgsTokenInt(
		const char* key,
		const char* par,
		const char* man,
		int* r, bool* rset, int dflt
	) : EzArgsToken(key,par,man)
	{
		_ptr = r;
		_sptr = rset;
		if(_sptr) *_sptr = false;
		*r = dflt;
	}
	const char** local_accept(const char** av){
		if(! av) return NULL;
		if(!strcmp(*av, _key)){
			av++;
			if(*av && myatoi(*av, _ptr)) {
				if(_sptr) *_sptr = true;
				return av;
			}
			Error("EzArgs: integer expected after '%s' option\n", _key);
			return NULL;
		} else {
			return NULL;
		} 
	}
};


bool EzArgs::add_bool(const char* key, const char* man, bool* r){
	_tokens = _tokens->append(new EzArgsTokenBool(key, man, r)); 
	return true;
}
bool EzArgs::add_int(const char* key, const char* par, const char* man, int* r, int dflt){
	_tokens = _tokens->append(new EzArgsTokenInt(key, par, man, r, NULL, dflt));
	return true;
}
bool EzArgs::add_int(const char* key, const char* par, const char* man, int* r, bool* rset){
	_tokens = _tokens->append(new EzArgsTokenInt(key, par, man, r, rset, 0)); 
	return true;
}
bool EzArgs::add_string(
	const char* key,
	const char* par,
	const char* man,
	const char** r,
	const char* dflt
){
	_tokens = _tokens->append(new EzArgsTokenString(key, par, man, r, dflt));
	return true;
}
	//Les extra string sont dans une liste à part !
bool EzArgs::add_extra(const char* par, const char* man, const char** r, const char* dflt){
	_extras = _extras->append(new EzArgsExtra(par, man, r, dflt));
	_nb_extras++;
	return true;
}

//usage par défaut ...
void EzArgs::usage(){
   char* tn = basename((char*)_toolname);
   printf("%s version %s\n", tn, _version);
   printf("usage: %s [options] ", tn);
   _extras->dump_param();
   printf("| %s -help\n", tn);
}

void EzArgs::giveoptions(){
	printf("recognized options:\n");
	_tokens->dump();
}

const char* EzArgs::version(){ return _version; }
const char* EzArgs::toolname(){ return basename((char*)_toolname); }

EzArgs::EzArgs(const char* vers){
	_version = vers;
	_nb_extras = 0;
	_tokens = NULL;
	_extras = NULL;

}

bool EzArgs::parse(int ac, const char* av[]){

	//PROLOGUE: options prédéfinies
	add_bool("-help", "print help and return", &_givehelp);
	add_bool("-version", "print version and return", &_giveversion);

	//PROLOGUE: gestions des extras
	//on les mets dans une table et dans le bon ordre ...
	EzArgsToken* extras_tab[_nb_extras];
	int k = _nb_extras;
	EzArgsToken* l = _extras;
	while(k--) {
		extras_tab[k] = l;
		l = l->next();
	}

	_argc = ac;
	//on décale les args et ont met
	//un NULL à la  fin
	_argv = new const char*[ac];
	_toolname = av[0];	
	int i;
	for(i=1; i< ac; i++){
		_argv[i-1] = av[i];	
	}
	const char** a; 
	for(a = &_argv[0]; *a; a++){
		const char** nwa = _tokens->accept(a);
		//option avec clé ?
		if(nwa) {
			a = nwa;
		} else {
			//on le met dans les extra s'il reste de la place !!
			if((_extras) && (_extras->accept(a))){
				//ok ..
			} else {
				Error("EzArgs: unrecognized option '%s'", *a);
			}
		}
	}

	if(_givehelp){ givehelp(); exit(0); }
	if(_giveversion){ printf("%s", version()); exit(0); }

	return true;
}
