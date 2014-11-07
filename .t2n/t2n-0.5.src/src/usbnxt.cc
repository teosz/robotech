
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
 * module   : usbnxt.cc 
 *
 * date     : 2007-03-07 
 * auteurs  : Pascal Raymond
 *--------------------------------------------------------------------------
 * nature   : Classe dérivée de UsbHandle, spécialement dédiée à la brique nxt.
 *--------------------------------------------------------------------------
 * Modifs   :
 * -----------------------------------------------------------------------*/

#include <string.h>
#include <stdio.h>
#include <libgen.h>
#include <errno.h>
#include "errors.h"
#include "errormng.h"
#include "usb.h"
#include "usbmisc.h"
#include "usbnxt.h"

//Les identifiants universels de la brique ...
#define LEGO_VENDOR_ID   0x0694
#define LEGO_NXT_PRODUCT_ID  0x0002

//Les codes connus et exploités ... 
#define NXT_WRITE_EP 0x01
#define NXT_READ_EP 0x82
#define NXT_WRITE_TIMEOUT 1000
#define NXT_READ_TIMEOUT 1000
#define DIRECT_COMMAND 0x00
#define SYSTEM_COMMAND 0x01
#define GET_BATTERY_LEVEL 0x0B
#define GET_DEVICE_INFO 0x9B
#define OPEN_READ 0x80
#define READ_COMMAND 0x82
#define WRITE_COMMAND 0x83
#define CLOSE_COMMAND 0x84
#define DELETE_FILE 0x85
#define FIND_FIRST_FILE 0x86
#define FIND_NEXT_FILE 0x87
#define GET_FIRMWARE_VERSION 0x88

//#define OPEN_WRITE 0x8B
//#define OPEN_WRITE 0x89
#define OPEN_WRITE 0x81

// Pour récupérer proprement
// les message d'erreurs de la libusb ...
static ErrorMng _usbnxt_error("usbnxt: ");

const char* usbnxt_error(){
   return _usbnxt_error.get();
}

UsbNxt::UsbNxt(){}

int UsbNxt::init(){
	int r = UsbHandle::init(LEGO_VENDOR_ID, LEGO_NXT_PRODUCT_ID);
	if(r < 0) {
		_usbnxt_error.set(usbmisc_error());
		return r;
	}
	UsbHandle::init_bulk(
		NXT_WRITE_EP, NXT_WRITE_TIMEOUT,
		NXT_READ_EP, NXT_READ_TIMEOUT
	);

	return r;
}

int UsbNxt::_fails(const char* msg){
	_usbnxt_error.set("%s - %s", usbmisc_error(), (char*)msg);
	return -1;
}

int UsbNxt::battery_level(){
	//commande ...
	int res;
	char reply, command, status;
	char fmsg[] = "battery_level failed";

	//Commande :
	res = send( "UsbNxt::battery_level", //prologue pour le verbose 
			InC(DIRECT_COMMAND),
			InC(GET_BATTERY_LEVEL)
	);
	if (res) return _fails(fmsg);

	int mV;

	// on récupère 3 chars, 1 short = 5 bytes
	res = receive (
		OutC(&reply),
		OutC(&command),
		OutC(&status),
		OutS(&mV)
	);
	if (res) return _fails(fmsg);

	Verbose(1, "battery_level reply=0x%02x command=0x%02x status=0x%02x mV=%d\n",
		reply, command, status, mV 
	); 

	return mV;

}

int UsbNxt::print_infos(){
	int res;

	char fmsg[] = "print_infos failed";

	//---------------
	//Firmware infos ...
	//---------------
	res = send( "UsbNxt::print_infos",
		InC(SYSTEM_COMMAND),
		InC(GET_FIRMWARE_VERSION)
	);
	if (res) return _fails(fmsg);

	// on récupère 3 + 4 bytes = 7
	char reply, command, status;
	char pmv, pMv, fmv, fMv;
	res = receive (
		OutC(&reply),
		OutC(&command),
		OutC(&status),
		OutC(&pmv),
		OutC(&pMv),
		OutC(&fmv),
		OutC(&fMv)
	);
	if (res) return _fails(fmsg);

	printf("#### NXT INFOS ###############\n");
	printf("protocol version=%d.%d firmware version=%d.%d\n", pMv, pmv, fMv, fmv); 

	//---------------
	//Device infos ...
	//---------------
	res = send( "UsbNxt::print_infos",
		InC(SYSTEM_COMMAND),
		InC(GET_DEVICE_INFO)
	);
	if (res) return _fails(fmsg);

	char nme[15];
	char bt[6];
	int btsignal;
	int freeflash;
	res = receive (
		OutC(&reply),
		OutC(&command),
		OutC(&status),
		OutRAW(16, &nme[0]),
		OutRAW(6, &bt[0]),
		OutL(&btsignal),
		OutL(&freeflash)
	);
	if (res) return _fails(fmsg);

	printf("NXT Name: %s\n", nme);
	printf("Blutooth address: ");
	int k;
	for(k=0; k<6; k++){
		if(k) printf(":");
		printf("%02x", bt[k]);
	}
	printf("\n");
	printf("Blutooth signal: %d\n", btsignal);
	printf("Free user flash: %d\n", freeflash);

	return 0; 
}

//utile : récupère un descripteur de fichier

int UsbNxt::_unpack_filedesc(
	const char* fmsg,
	char* pstatus,  //important: dernier si <> 0
	char* pcmdhdl,  //important: handle de l'iterateur 
	char* pfnme,
	int* pfsz
){
	int res;
	// retour : 3 + 1 + 20 + 1x4 = 28
	// on récupère les 3 bytes habituels ...
	char reply, command;
	res = receive (
		OutC(&reply),
		OutC(&command),
		OutC(pstatus),
		OutC(pcmdhdl),   // le byte "handle"
		OutRAW(20, pfnme), // nom de fichier sur 21 char (y compris le '\0')
		OutL(pfsz)       // taille du fichier sur un long 
	);
	if (res) return -1;

	return 0;
}

int UsbNxt::list_files(){
	int res;

	char fmsg[] = "list_files failed";

	//---------------
	//On recherche le premier ...
	//---------------
	res = send( "UsbNxt::list_files (first file)",
		InC(SYSTEM_COMMAND),
		InC(FIND_FIRST_FILE),
		InNTS(20, "*.*")
	);
	if (res) return _fails(fmsg);

	char fnme[20];
	int fsz;
	char status, cmdhdl;
	
	if(_unpack_filedesc(fmsg, &status, &cmdhdl, &fnme[0], &fsz) < 0)
		return _fails(fmsg);
	Verbose(2, "list_files command handler=%d\n", (int)cmdhdl);

	// affichons ...
	printf("FILE:\"%s\" SIZE:%d\n", fnme, fsz);

	//----------------
	//puis les suivants ...
	//----------------
	while(status == 0){
		res = send( "UsbNxt::list_files (next file)",
			InC(SYSTEM_COMMAND),
			InC(FIND_NEXT_FILE),
			InC((int)cmdhdl)
		);
		if (res) return _fails(fmsg);

		if(_unpack_filedesc(fmsg, &status, &cmdhdl, &fnme[0], &fsz) < 0)
			return _fails(fmsg);
		Verbose(2, "list_files command handler=%d\n", cmdhdl);

		printf("FILE:\"%s\" SIZE:%d\n", fnme, fsz);
	}
	//----------------
	//puis on ferme la commande 
	//----------------
	res = send( "UsbNxt::print_infos",
		InC(SYSTEM_COMMAND),
		InC(CLOSE_COMMAND),
		InC((int)cmdhdl)
	);
	if (res) return _fails(fmsg);

	return 0; 
}

int filesize(const char* fname){
	// Un peu bourrin, mais évite de faire appel
	// à des lib systèmes (portage vers windows) 
	FILE* inf = fopen(fname, "r");
	if(! inf) return -1;
	int fno = fileno(inf);

	//on lit à fond la caisse ... 
	int n, size;
	char* buff[1024];
	size = 0; 
	do {
		n = read(fno, &buff[0], 1024); 
		if(n > 0) size += n;
	} while(n > 0);
	fclose(inf);
	if(n < 0) return -1;
	return size;
}

int UsbNxt::download(const char* fname){
	char fmsg[] = "download failed";
	int res;

	if(strlen(fname) >= 20){
		_usbnxt_error.set("download: filename must be less than 15 chars");
		return -1;
	}
	//---------------
	//Le fichier existe-t-il ?
	//---------------
	res = send( "UsbNxt::dowload (search remote file)",
		InC(SYSTEM_COMMAND),
		InC(FIND_FIRST_FILE),
		InNTS(20, fname)
	);
	if (res) return _fails(fmsg);
	char dummy[20];
	int fsz;
	char status, cmdhdl;
	if(_unpack_filedesc(fmsg, &status, &cmdhdl, &dummy[0], &fsz) < 0) return _fails(fmsg);
	if(status) {
		_usbnxt_error.set("download: can't find remote file (status=0x%02x)", status);
		return -1;
	}
	res = send( "UsbNxt::download",
		InC(SYSTEM_COMMAND),
		InC(CLOSE_COMMAND),
		InC((int)cmdhdl)
	);
	if (res) return _fails(fmsg);

	//---------------
	//Ouverture du local 
	//---------------
	FILE* localf = fopen(fname, "w");
	if(! localf) {
		_usbnxt_error.set("download: can't open local file (%s)", strerror(errno));
		return -1;
	}
	int fno = fileno(localf);

	//---------------
	//Ouverture du remote 
	//---------------
	res = send( "UsbNxt::dowload (search remote file)",
		InC(SYSTEM_COMMAND),
		InC(OPEN_READ),
		InNTS(20, fname)
	);
	if (res) return _fails(fmsg);

	char reply, command, fhandler;
	int fsize;

	res = receive (
		OutC(&reply),
		OutC(&command),
		OutC(&status),
		OutC(&fhandler),
		OutS(&fsize)
	);
	if (res) return _fails(fmsg);

	if (status){
		_usbnxt_error.set("download: can't open remote file (status=0x%02x)", status);
		return -1;
	}

	//------------
	// lecture par gros paquets
	// max buff -4 bytes -1*2 (short)
	//------------
	int maxpiece = max_buff_sz() - 6;
	char buff[maxpiece];

	Verbose("start to download %s (%d bytes)\n", fname, fsize);

	int remain = fsize;
	while (remain) {

		int to_do = (remain >= maxpiece)?  maxpiece : remain;

		int res = send( "UsbNxt::download",
			InC(SYSTEM_COMMAND),
			InC(READ_COMMAND),
			InC((int)fhandler),
			InS(to_do)
		);
		if (res) return _fails(fmsg);

		int nbread;
		res = receive(
			OutC(&reply),
			OutC(&command),
			OutC(&status),
			OutC(&fhandler),
			OutS(&nbread),
			OutRAW(to_do, buff)
		);
		if (res) return _fails(fmsg);

		res = write(fno, &buff[0], nbread);
		if (res != nbread) {
			_usbnxt_error.set("download: write local file failed (%s)", strerror(errno));
			return -1;
		}

		remain -= nbread;
	}

	fclose(localf);
	//----------------
	//puis on ferme la commande 
	//----------------
	res = send( "UsbNxt::download(close)",
		InC(SYSTEM_COMMAND),
		InC(CLOSE_COMMAND),
		InC((int)fhandler)
	);

	if(status) {
		_usbnxt_error.set("download: error while writing (status=%02x)", status);
		return -1;
	}

	return 0;	

}

//Teste si un fichier existe dans la brique ...
bool UsbNxt::_file_exists(const char* nme){
	//---------------
	//Le fichier existe déjà ?
	//---------------
	char fmsg[] = "file_exists failed";
	Verbose("testing for existing file \"%s\"\n", nme);
	int res = send( "_file_exists",
		InC(SYSTEM_COMMAND),
		InC(FIND_FIRST_FILE),
		InNTS(20, nme)
	);
	if (res) return _fails(fmsg);

	char fnme[20];
	int fsz;
	char status, cmdhdl;
	if(_unpack_filedesc(fmsg, &status, &cmdhdl, &fnme[0], &fsz) < 0)
		return _fails(fmsg);

	//Un nom de fichier vide -> il n'existe pas
	return (fnme[0] != '\0');
}

int UsbNxt::_file_delete(const char* nme){
	//Commande simple : on lui passe le nom
	char fmsg[] = "file_delete failed";
	Verbose("deleting for existing file \"%s\"\n", nme);
	int res = send( "_file_delete",
		InC(SYSTEM_COMMAND),
		InC(DELETE_FILE),
		InNTS(20, nme)
	);
	if (res) return _fails(fmsg);
	//Retour simple : juste le status
	char reply, command, status ;
	res = receive (
		OutC(&reply),
		OutC(&command),
		OutC(&status)
	);
	if (res) return _fails(fmsg);

	return 0;
}

int UsbNxt::remove(const char* fname){
	//char fmsg[] = "remove failed";
	//int res;

	if (_file_exists(fname)){
		if ( AskYesNo("delete file \"%s\"", fname)){
			//Fermer le fichier ? 
			//Détruire le fichier ...
			if (_file_delete(fname))
				return -1;
		} else {
			Verbose("delete aborted by user\n");
			return 0;
		}
	} else {
		return -1;
	}
	return 0;	

}

int UsbNxt::upload(const char* fname){
	char fmsg[] = "upload failed";

	int res;

	//--------
	// Vérif du nom
	//--------
	char *dirc, *basec, *bname, *dname;
	dirc = strdup(fname);
	basec = strdup(fname);
	dname = dirname(dirc);
	bname = basename(basec);
	char* ext = strrchr(bname, '.');
	Verbose(2,"upload dir=%s file=%s ext=%s\n", dname, bname, ext);
/*
	if(strcmp(ext, ".rxe")){
		_usbnxt_error.set("upload: .rxe extention required");
		return -1;	
	}
*/
	if(strlen(bname) >= 20){
		_usbnxt_error.set("upload: filename must be less than 15 chars");
		return -1;	
	}

	//---------------
	//Le fichier existe déjà ?
	//---------------
	if (_file_exists(bname)){
		if ( AskYesNo("overwrite existing file \"%s\"", bname)){
			//Fermer le fichier ? 
			//Détruire le fichier ...
			if (_file_delete(bname))
				return -1;
		} else {
			Verbose("upload aborted by user\n");
			return 0;
		}
	}

	//--------
	// Portable : on compte le nbre de bits ....
	//--------
	int fsize = filesize(fname);
	if(fsize < 0){ 
		_usbnxt_error.set("upload: can't load file (%s)", strerror(errno));
		return -1;	
	}
	Verbose("upload %s (%d bytes) from %s\n", bname, fsize, dname);

	//----
	// Ouverture de la session d'écriture
	// !! c'est le basename qui donne le nom local !!
	// sc + ow + bname (20) + fsz (4)
	//----

	res = send( "UsbNxt::upload (open)",
		InC(SYSTEM_COMMAND),
		InC(OPEN_WRITE),
		InNTS(20, bname),
		InL(fsize)
	);
	if (res) return _fails(fmsg);

	char reply = '\0';
	char command = '\0'; 
	char status = '\0'; 
	char fhandler = '\0'; 

	res = receive (
		OutC(&reply),
		OutC(&command),
		OutC(&status),
		OutC(&fhandler)
	);
	if (res) return _fails(fmsg);
	if (status){
		printf( "usb_strerror = %s\n", usb_strerror( ));
		_usbnxt_error.set(
			"upload: can'y initiate upload (reply=0x%02x,status=0x%02x,error=0x%04x)",
				reply, status, res);
		return -1;
	}
	
	//---------------------
	// Ecriture par paquets max :
	// max buff -3 bytes de début
	//---------------------
	int maxpiece = max_buff_sz() - 3; 
	char buff[maxpiece];
	
	FILE* inf = fopen(fname,"r");
	int fno = fileno(inf);
	int nbb;

	int berr=false; //erreur interne
	do {
		nbb = read(fno, &buff[0], maxpiece);
		if (nbb) {
			berr = send( "UsbNxt::upload(sending block)",
				InC(SYSTEM_COMMAND),
				InC(WRITE_COMMAND),
				InC((int)fhandler),
				InRAW(nbb, &buff[0])
			);

			int sbytes;
			berr = receive (
				OutC(&reply),
				OutC(&command),
				OutC(&status),
				OutC(&fhandler),
				OutS(&sbytes)
			);
		}
	} while (nbb && !berr && !status);

	fclose(inf);
	if(berr) return _fails(fmsg);

	//----------------
	//puis on ferme la commande 
	//----------------
	res = send( "UsbNxt::upload(close)",
		InC(SYSTEM_COMMAND),
		InC(CLOSE_COMMAND),
		InC((int)fhandler)
	);

	if(status) {
		_usbnxt_error.set("upload: error while writing (status=%02x)", status);
		return -1;
	}

	return 0;
}

/*
int nxt_battery(usb_dev_handle* dev){
	int r;
	buffer com;
	buffer res;
	char reply_c;
	char command_c;
	char status_c;
	unsigned int mV;

	com[0] = DIRECT_COMMAND;
	com[1] = GET_BATTERY_LEVEL;

	r = do_nxt_command(dev, &com[0], 2, &res[0]);

	// retour : byte, byte, byte, short (le)
	if (r != 5) {
		fprintf(stderr, "nxt_battery: bad response (%d bytes)\n", r);
		return -1;
	}
	reply_c = res[0];		
	command_c = res[1];		
	status_c = res[2];		
	mV = ((unsigned int)res[3] << 8) & (unsigned int)res[4];

	return (int)mV;
}

int main(){
	struct usb_dev_handle *nxt;

	nxt = find_nxt();
	if(nxt) {
		printf ("TROUVÉ !!!\n");
	} else {
		printf ("pas trouvé ...\n");
		return 1;
	}
	usb_reset(nxt);

CleanReturn:

	if(nxt) {
		usb_close(nxt);
	}
}
*/
