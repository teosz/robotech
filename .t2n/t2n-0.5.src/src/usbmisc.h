
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
 * module   : usbmisc.h
 *
 * date     : 2007-03-07 
 * auteurs  : Pascal Raymond
 *--------------------------------------------------------------------------
 * nature   : Couche orienté-objet au dessus le de la libusb
 *  
 *--------------------------------------------------------------------------
 * Modifs   :
 * -----------------------------------------------------------------------*/

//  Message d'erreurs de la lib ...
extern const char* usbmisc_error();


//--------------------------------------------------------------
//Codage des params (s,v) pour l'écriture ds buffer
//--------------------------------------------------------------
//s > 0 => v est un pointeur char*
//         NTS MODE
//         si "s=2n" -> v est une "null-terminated string,
//                     qui sera forcée à n caractères
//         RAW MODE
//         si "s=2n+1"   -> v est un tableau brut de taille exactement n
//s < 0 => v est une valeur immédiate sur 's' bytes little-endian
//s = 0 => fini
//(Remarque : les char sont traités comme des entiers) 
// macros pour le send monobloc
//--------------------------------------------------------------
#define InC(x)    -1, (void*)x
#define InS(x)    -2, (void*)x
#define InL(x)    -4, (void*)x
#define InNTS(s,x)   (s<<1), (void*)x
#define InRAW(s,x)   ((s<<1)|1), (void*)x

//--------------------------------------------------------------
//Codage des params (s,p) pour la lecture ds buffer
//--------------------------------------------------------------
//s > 0 => v est un char* sur 's' bytes
//s < 0 => v est un pointeur sur sur 's' bytes little-endian
//s = 0 => fini
// Remarque : les char sont traités comme des tableaux de longueur 1
// Remarque : pas de cas NTS -> que des tableaux bruts
// macros pour le get monobloc
//--------------------------------------------------------------
#define OutS(x)    -2, (void*)x
#define OutL(x)    -4, (void*)x
#define OutC(x)     1, (void*)x
#define OutRAW(s,x)   s, (void*)x


class UsbBulkBuff; 

class UsbHandle {
	struct usb_device* _dev;
	struct usb_dev_handle* _handle;
	UsbBulkBuff* _bbuff;

	static struct usb_device* _find_usb_dev(
		u_int16_t vendor, u_int16_t product	
	);

	void _init();
public:
	UsbHandle(){ _init(); }
	int init(u_int16_t vendor, u_int16_t product);
	void init_bulk(int wep, int wto, int rep, int rto);
	//taille max buffer in
	int max_buff_sz();
	
	~UsbHandle();

	// send monobloc => utiliser les macros InXX
	// ex : send(InC('a'), InS(42), InZ(10, "hello"));
	int send(
		const char* vprolog, //verbose prologue
	   int s0 = 0, void* v0 = 0,
		int s1 = 0, void* v1 = 0,
		int s2 = 0, void* v2 = 0,
		int s3 = 0, void* v3 = 0,
		int s4 = 0, void* v4 = 0
	);
	// receive monobloc => utiliser les macros OutXX
	// ex : send(OuC(&c), InS(&n), InZ(10, ptr));
	int receive(
	   int s0 = 0, void* p0 = NULL,
		int s1 = 0, void* p1 = NULL,
		int s2 = 0, void* p2 = NULL,
		int s3 = 0, void* p3 = NULL,
		int s4 = 0, void* p4 = NULL,
		int s5 = 0, void* p5 = NULL,
		int s6 = 0, void* p6 = NULL
	);
};

// buffer pour communication ``bulk''
#define BFSZ 64
class Buff {
	unsigned char _data[BFSZ];
	int _len;
	int _rindex;
public:

	void dump(FILE* os);
	void reset(){
		memset((void*)_data, '\0', BFSZ);
		_len=0;
		_rindex = 0;	
	}
	Buff(){ reset(); } 
	//force la longeur ...
	void set_len(int l) { _len = l; }
	//accès : de l'extérieur 
	// il vaut mieux voir un char* ...
	char* data(){ return (char*)(&_data[0]); }
	int len(){ return _len; }
	static int maxsz(){ return BFSZ; }
	//écriture ...
	int put(char c){
		if(_len < BFSZ) {
			_data[_len] = c;
			_len++;
			return 1;
		} else {
			return 0;
		}
	}
	int get(char* r){
		if(_rindex >= _len) return -1;
		*r = _data[_rindex++];	
		return 1;
	}
};

class UsbBulkBuff {

	struct usb_dev_handle* _devh;
	unsigned int _write_ep;
	unsigned int _write_to;
	unsigned int _read_ep;
	unsigned int _read_to;

	Buff _read_buff;
	Buff _write_buff;
	void _init();

friend class UsbHandle;
protected:

	//Création, initialisations
	UsbBulkBuff();
	inline void init(struct usb_dev_handle* dh, int wep, int wto, int rep, int rto);

	//reset des buffers
	void reset();

	//put basique (s,v) => voir macros send monobloc
	int put(int s, void* v);

	//écrit le buffer in, lit dans le  buffer out
	int write_read( const char* vprolog);

	//get basique (s,p) => voir macros receive monobloc
	int get(int s, void* v);

	// Erreurs de la classe ...
	static ErrorMng error;

	//taille max buffer in
	static int maxsz(){ return Buff::maxsz(); }

};

inline void UsbBulkBuff::reset(){
	_read_buff.reset();
	_write_buff.reset();
}

inline void UsbBulkBuff::_init(){
   _devh = NULL;
   _write_ep = _write_to = _read_ep = _read_to = 0;
	reset();
}

inline void UsbBulkBuff::init(struct usb_dev_handle* dh, int wep, int wto, int rep, int rto){
	_devh = dh;
	_write_ep = wep; 
	_write_to = wto; 
	_read_ep = rep; 
	_read_to = rto; 
	reset();
}

inline int UsbHandle::max_buff_sz(){ return _bbuff->maxsz(); }
