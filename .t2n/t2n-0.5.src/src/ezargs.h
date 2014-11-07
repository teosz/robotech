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
   module   : ezargs.h
   date     : 30/08/2005
   auteurs  : Pascal Raymond

   modif    : 
----------------------------------------------------------------------------
   nature :  Classe EzArgs, pour faciliter la gestion des arguments
      de commande (argc, argv). 

   - gère un numéro de version (fourni par l'utilisateur)
   - gère un nom d'outil (déduit du argv[0] standard)
	- gère les options avec clés classiques du style :
         . <key>
         . <key> <int>
         . <key> <string>
     (n.b. les clés peuvent ne pas commencer par -)
   - gère aussi les arguments extras, non introduit par une clé
     dans ce cas, c'est l'ordre d'apparition qui est significatif
   - imprime des messages d'usage standard
   - gère des options par défaut :
     -help, -version 
----------------------------------------------------------------------------
   (C = constructeur, M = methode, F = fonction)
-----------------------------------------------------
On peut utiliser directement la classe EzArgs ou, plus
proprement, dériver sa propre classe. Voir plus bas
"MyArgs" pour un exemple simple de dérivation.

Sion, l'utilisation directe se fait en 3 temps :

1- création

   C) EzArgs::EzArgs(char* vers)

2- déclaration des options

   M) add_bool(char* key, char* man, bool* r)
   M) add_int(char* key, char* par, char* man, int* r, int dflt)
   M) add_int(char* key, char* par, char* man, int* r, bool* rset)
   M) add_string(char* key, char* par, char* man, char** r, char* dflt)
   M) add_extra(char* par, char* man, char** r, char* dflt)

   key   : la clé (sauf pour extra)
   param : un texte explicatif pour l'argument
           (sauf pour les bool) 
   man   : un texte explicatif  
   r     : pointeur sur le résultat
           (suivant le type attendu)
   dflt  : valeur par défaut pour *r
   rset  : pointeur sur un booléen qui indique si
             l'option à été parsée (int uniquement)

3- parsing

M) parse(int argc, char* argv[])

   argc, argv: paramètres de la ligne de commande,
               Y COMPRIS le nom de la commande (argv[0])

   Les arguments argv[1..argc-1] sont parsés selon les
   déclaration précédentes.
   Si une option apparaît plusieurs fois, c'est la dernière
   qui "gagne".
   Les extras sont traités dans l'ordre où ils ont été déclarés :
   la première chaîne sans clés est associée au premier extra déclaré,
   le deuxième au deuxième etc.
   S'il y a plus de chaînes sans clé que d'extra déclaré, on lève
   une erreur. 
----------------------------------------------------------------------------
Exemple de classe dérivée :

class MesArgs:public EzArgs {
	bool _t;
	int _opt;
	char* _outfile;
	char* _infile;
	char* _mainproc;
public:
	MesArgs(int argc, char* argv[]):EzArgs("0.0"){
		add_bool("-t", "test only", &_t);
		add_int("-opt", "<int>", "optimisation level", &_opt, -1);
		add_string("-o", "<fname>", "set output name", &_outfile, NULL);
		add_extra("<file>", "input file", &_infile, NULL);
		add_extra("<main>", "main procedure", &_mainproc, NULL);
		parse(argc, argv);
	}
};

int main(int argc, char* argv[]){
	MesArgs* args = new MesArgs(argc, argv);
}


--------------------------------------------------------------------------*/

#ifndef __PR_EZARGS_H
#define __PR_EZARGS_H

typedef const char* cstring;

//restons abstrait !
class EzArgsToken ;

class EzArgs {
	int _argc;
	const char** _argv;
	int _cur_arg;
	const char* _toolname;
	const char* _version;
	//option predefs :
	bool _givehelp;
	bool _giveversion;
protected:
	//les tokens avec clé...
	EzArgsToken* _tokens;
	//les xtras (sans clé);
	int _nb_extras;
	EzArgsToken* _extras;
public:
	EzArgs(const char* ver);

	bool add_bool(cstring key, cstring man, bool* r);
	bool add_int(cstring key, cstring par, cstring man, int* r, int dflt);
	bool add_int(cstring key, cstring par, cstring man, int* r, bool* rset);
	bool add_string(cstring key, cstring par, cstring man, cstring* r, cstring dflt);
	bool add_extra(cstring par, cstring man, cstring* r, cstring dflt);

	bool parse(int ac, cstring av[]);

	//usage par défaut ...
	void usage();

	//Les options prédéfinies
	cstring version();
	cstring toolname();
	void giveoptions();
	void givehelp(){ usage(); giveoptions(); }
};

#endif
