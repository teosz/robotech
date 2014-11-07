
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
 * module   : usbmisc.cc 
 *
 * date     : 2007-03-07 
 * auteurs  : Pascal Raymond
 *--------------------------------------------------------------------------
 * nature   : Couche orienté-objet au dessus le de la libusb
 *
 *--------------------------------------------------------------------------
 * Modifs   :
 * -----------------------------------------------------------------------*/

#include <string.h>
#include <stdio.h>
#include <ctype.h>
#include "errors.h"
#include "errormng.h"
#include "usb.h"
#include "usbmisc.h"

//toujours vrai ???
#define USB_INTERFACE 0
#define USB_CONFIG 1

//Messages d'erreur de la lib.

static ErrorMng _usbmisc_error("usbmisc: ");

const char* usbmisc_error(){
	return _usbmisc_error.get();
}

void UsbHandle::_init(){
	_dev = NULL;
	_handle = NULL;
	_bbuff = NULL;
}

//extern int print_device(struct usb_device *dev, int level);

int UsbHandle::init(u_int16_t vendor, u_int16_t product){
	_dev = UsbHandle::_find_usb_dev(vendor, product);
	if(_dev == NULL) {
		_usbmisc_error.set("no usb device found (vendor=0x%04x product=0x%04x)",
			vendor, product
		);
		return -1;
	}

//print_device(_dev, 0);

   _handle = usb_open(_dev);
	if (!_handle) {
		_usbmisc_error.set("fails to open device handle (vendor=0x%04x product=0x%04x)",
			vendor, product
		);
		return -1;
	}
	//reset ?
	usb_reset(_handle);

	int err;
	//set config 
	err = usb_set_configuration(_handle, USB_CONFIG);
	if(err != 0){
//printf( "usb_strerror = %s\n", usb_strerror( )); 
		_usbmisc_error.set(
			"fails to set config, errno=%d, usberr=\"%s\" (cf=%d vendor=0x%04x product=0x%04x)",
			err, usb_strerror(), USB_CONFIG, vendor, product
		);
		return -1;
	}
	//demande d'interface ...
	err = usb_claim_interface(_handle, USB_INTERFACE);
	if(err != 0){
		_usbmisc_error.set(
			"fails to optain usb interface (erno=%d id=%d vendor=0x%04x product=0x%04x)",
			err, USB_INTERFACE, vendor, product
		);
		return -1;
	}
	return 0;
}

UsbHandle::~UsbHandle(){
	//fermeture propre ...
	if(_handle) usb_close(_handle);
}


struct usb_device* UsbHandle::_find_usb_dev(
	u_int16_t vendor,
	u_int16_t product
){
	struct usb_bus *busses, *bus;
	struct usb_device *devs, *d;
	u_int16_t v, p;

	usb_init();
	usb_find_busses();
	usb_find_devices();
	busses = usb_get_busses();
	for(bus = busses; bus;  bus = bus->next){
		Verbose(2, "(usb scan) bus dirname=%s\n", bus->dirname);
		devs = bus->devices;
		for(d=devs; d; d=d->next){
			v = d->descriptor.idVendor;
			p = d->descriptor.idProduct;
			Verbose(2, "(usb scan) dev filename=%s, vendor=0x%04x, product=0x%04x\n",
				d->filename, v, p
			);
			if((v == vendor) && (p==product)) return d;
		}
	}
	return NULL;
}

void UsbHandle::init_bulk(int wep, int wto, int rep, int rto){
	if (_bbuff == NULL) _bbuff = new UsbBulkBuff();
	_bbuff->init(_handle, wep, wto, rep, rto);
	
}

UsbBulkBuff::UsbBulkBuff(){
	_init();
}

// -----------------------------------------
// écriture de base dans un buffer (s,v) 
// règles :
// s < 0 : v est un entier immédiat sur (-s) octets 
//         qu'on écrit en le
// s > 0 : v est un char* qui pointe
//       NULL-TERM-STRING 
//         si s=2n : sur une null-terminated string
//         auquel cas on écrit la chaîne en la
//         tronquant ou en l'étendant avec des 0
//         si besoin.
//       RAW-COPY
//       - si s=2n+1 : sur un tableau brut d'octets
//         qu'on écrit tel-quel
// -----------------------------------------
int UsbBulkBuff::put(int s, void* v){
	if(s ==0) return 0;
	if(s < 0) {
		//DIRECT, little-endian
		int nbytes = -s;  //corrige la taille
		unsigned char *p = (unsigned char *) &v;
		for(int cpt=0; cpt<nbytes; cpt++){
			if(_write_buff.put (*(p + cpt)) != 1) {
				_usbmisc_error.set("UsbBulkBuff::put failed");
				return -1;
			} 
		}
		return 0;
	} else {
		//INDIRECT => chaîne de caractère
		int nbytes = s >> 1;
		int rawcopy = s & 1;
		//écrit s, tronque/complète avec des '\0' si besoin
		char* p = (char*)v;
		char c = -1;
		int cpt;
		for(cpt=0; cpt < nbytes; cpt++){
			if(c || rawcopy) c = *p++;
			if(_write_buff.put (c) != 1) {
				_usbmisc_error.set("UsbBulkBuff::put failed");
				return -1;
			}
		}
		return 0;
	}
}

// -----------------------------------------
// lecture de base dans un buffer (s,p) 
// -----------------------------------------
int UsbBulkBuff::get(int s, void* p){
	if(s == 0) return 0;
	if(s < 0) {
		//entier little endian
		unsigned int* r = (unsigned int*)p;
		char c;
		*r = 0;	
		int cpt;
		int nbytes = -s;
		for(cpt=0; cpt<nbytes; cpt++){
			if(_read_buff.get(&c) != 1){
				_usbmisc_error.set("UsbBulkBuff::get failed"); 
				return -1;
			}
			*r |= ((int)c & 0xFF) << (cpt<<3);
		}
		return 0; 
	} else {
		//chaîne de caractères
		char* z = (char*)p;
		int cpt = s;
		for(cpt=0; cpt < s; cpt++){
			if(_read_buff.get(z++) != 1) {
				_usbmisc_error.set("UsbBulkBuff::get failed"); 
				return -1;
			}
		}
		return 0; 
	}
}

void Buff::dump(FILE* os){
	fprintf(os,"Buff::dump, size=%d\n", len());
	int k;
	for(k=0; k<len(); k++){
		if(k && ((k % 16) == 0)) fprintf(os,"\n"); 
		if(isprint(_data[k])) fprintf(os,"  %c", _data[k]);
		else fprintf(os," %02x", _data[k]);
	}
	fprintf(os,"\n"); 
}

int UsbBulkBuff::write_read(
const char* vprolog
){

	int r;
	if(_write_buff.len() == 0) {
		return 0;
	}
	if(Verbose() >= 3){
		Verbose(3,"UsbBulkBuff::usb_bulk_write(0x%02x, 0x%02x, 0x%x, %d, %d)\n",
				_devh, _write_ep, _write_buff.data(), _write_buff.len(), _write_to);
		_write_buff.dump(stderr);
	}
	r = usb_bulk_write(_devh, _write_ep, _write_buff.data(), _write_buff.len(), _write_to);
	Verbose(2, "%s usb_bulk_write %d bytes on %d bytes\n",
		(vprolog)?vprolog:"", r, _write_buff.len());
	if(r != _write_buff.len()) {
		_usbmisc_error.set("usb_bulk_write failed (%d bytes instead of %d)\n",
			r, _write_buff.len()
		);
		return -1;
	}
	r = usb_bulk_read(_devh, _read_ep, _read_buff.data(), _read_buff.maxsz(), _read_to);
	Verbose(2, "%s usb_bulk_read -> %d bytes\n",
		(vprolog)?vprolog:"", r);
	if(r < 0) {
		_usbmisc_error.set("usb_bulk_read failed\n");
		return -1;
	}
	_read_buff.set_len(r);
	return 0;
}

// Send monobloc
int UsbHandle::send(
	const char* vprolog,
	int s0, void *v0,
	int s1, void *v1,
	int s2, void *v2,
	int s3, void *v3,
	int s4, void *v4
) {
	_bbuff->reset();

	if(_bbuff->put(s0, v0)) goto BUFF_ERROR;
	if(_bbuff->put(s1, v1)) goto BUFF_ERROR;
	if(_bbuff->put(s2, v2)) goto BUFF_ERROR;
	if(_bbuff->put(s3, v3)) goto BUFF_ERROR;
	if(_bbuff->put(s4, v4)) goto BUFF_ERROR;

	if(_bbuff->write_read(vprolog)) goto SEND_ERROR;

	return 0;

	BUFF_ERROR :
		_usbmisc_error.set("internal buffer error");
		return -1;	

	SEND_ERROR :
		//message déjà mis ...
		return -1;
}

// Receive monobloc (7 items max)
int UsbHandle::receive(
   int s0, void* p0,
   int s1, void* p1,
   int s2, void* p2,
   int s3, void* p3,
   int s4, void* p4,
   int s5, void* p5,
   int s6, void* p6
) {
	if(_bbuff->get(s0, p0)) goto BUFF_ERROR;
	if(_bbuff->get(s1, p1)) goto BUFF_ERROR;
	if(_bbuff->get(s2, p2)) goto BUFF_ERROR;
	if(_bbuff->get(s3, p3)) goto BUFF_ERROR;
	if(_bbuff->get(s4, p4)) goto BUFF_ERROR;
	if(_bbuff->get(s5, p5)) goto BUFF_ERROR;
	if(_bbuff->get(s6, p6)) goto BUFF_ERROR;

	return 0;

	BUFF_ERROR :
		printf( "usb_strerror = %s\n", usb_strerror( ));
		_usbmisc_error.set("internal buffer error");
		return -1;	
} 


