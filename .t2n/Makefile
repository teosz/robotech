# Talk2Ntx (t2n) 
# 
# 1) libusb is required (http://libusb.sourceforge.net/)
#    install it and check the USBROOT var
# 2) define CPU var if several architecture are targeted
#    (e.g. linux, sparc, cygwin etc ...) 
#
# N.B. tested on :
#      - pc/linux with g++ 3.4
#      - sparc/solaris with g++ 3.4
#

include /usr/share/hardening-includes/hardening.make

MAIN=t2n

OBJDIR=./obj$(CPU)
SRCDIR=./src

# ou trouver les .h et les lib usb/usbpp 
USBROOT=$(HOME)

all : $(OBJDIR) $(OBJDIR)/$(MAIN)  $(OBJDIR)/usbscan
static : $(OBJDIR)/$(MAIN).static

hard:
	DEB_BUILD_HARDENING=1 make

CC=g++
LK=g++
#CFLAGS=-I$(USBROOT)/include -I$(SRCDIR) -I$(OBJDIR) -g
#LFLAGS=-L$(USBROOT)/lib
CFLAGS= -I$(SRCDIR) -I$(OBJDIR) -g -Wall

#	-Wformat -Wformat-security -Werror=format-security \

LFLAGS=
LIBS=-lusb -lstdc++

OBJS=$(OBJDIR)/$(MAIN).o \
     $(OBJDIR)/usbmisc.o \
     $(OBJDIR)/usbnxt.o \
     $(OBJDIR)/errors.o \
     $(OBJDIR)/errormng.o \
     $(OBJDIR)/ezargs.o 

$(OBJDIR)/usbscan: $(SRCDIR)/usbscan.c
	gcc $(CFLAGS) $(LFLAGS) $(SRCDIR)/usbscan.c $(LIBS) -o $(OBJDIR)/usbscan

$(OBJDIR)/$(MAIN) : $(OBJS)
	$(LK) $(LFLAGS) $(OBJS) $(LIBS) -o $(OBJDIR)/$(MAIN)

$(OBJDIR)/$(MAIN).static : $(OBJS)
	$(LK) -static $(LFLAGS) $(OBJS) $(LIBS) -o $(OBJDIR)/$(MAIN).static

$(OBJDIR)/%.o : $(SRCDIR)/%.cc 
	$(CC) -c $(CFLAGS) $(SRCDIR)/$*.cc -o $(OBJDIR)/$*.o


$(OBJDIR)/usbmisc.o : $(SRCDIR)/usbmisc.h $(SRCDIR)/errormng.h $(SRCDIR)/errors.h

$(OBJDIR)/usbnxt.o : $(SRCDIR)/usbnxt.h $(SRCDIR)/usbmisc.h $(SRCDIR)/errormng.h \
                     $(SRCDIR)/errors.h

$(OBJDIR)/$(MAIN).o : $(SRCDIR)/usbnxt.h $(SRCDIR)/usbmisc.h $(SRCDIR)/errormng.h \
                      $(SRCDIR)/errors.h $(SRCDIR)/ezargs.h $(SRCDIR)/version.h

$(OBJDIR) :
	mkdir $(OBJDIR)

clean:
	rm -f $(OBJDIR)/*.o

distclean:
	rm -rf $(OBJDIR)

distrib: all static
	ddir=t2n-`$(OBJDIR)/$(MAIN) -version` ; \
	echo $$ddir ; \
	if [ ! -d $$ddir ] ; then mkdir $$ddir ; fi ; \
	cp $(OBJDIR)/$(MAIN) $$ddir ; strip $(OBJDIR)/$(MAIN) ; \
	cp $(OBJDIR)/$(MAIN).static $$ddir ; strip $(OBJDIR)/$(MAIN).static ; \
	cp -r hotplug $$ddir ; \
	cp -r udev $$ddir ; \
	tar zcvf $$ddir.tgz $$ddir ; mv $$ddir.tgz publish ; \
	sddir=t2n-`$(OBJDIR)/$(MAIN) -version`.src ; \
	echo $$sddir ; \
	if [ ! -d $$sddir ] ; then mkdir $$sddir ; fi ; \
	cp README $$sddir ; \
	cp COPYING $$sddir ; \
	cp COPYING.LESSER $$sddir ; \
	cp $(SRCDIR)/Makefile $$sddir ; \
	cp -r $(SRCDIR) $$sddir ; \
	cp -r udev $$sddir ; \
	cat publish/in.index.html | sed -e s/BINDIST/$$ddir.tgz/g | sed -e s/SRCDIST/$$sddir.tgz/g > publish/index.html ; \
	tar zcvf $$sddir.tgz $$sddir ; mv $$sddir.tgz publish
	cp -r publish/* /import/www/PEOPLE/raymond/edu/lego/t2n/ 
