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


MAIN=t2n

OBJDIR=./obj$(CPU)
SRCDIR=./src

# ou trouver les .h et les lib usb/usbpp 
USBROOT=$(HOME)

all : $(OBJDIR) $(OBJDIR)/$(MAIN)  $(OBJDIR)/usbscan
static : $(OBJDIR)/$(MAIN).static

CC=g++
LK=g++
CFLAGS=-I$(USBROOT)/include -I$(SRCDIR) -I$(OBJDIR) -g
LFLAGS=-L$(USBROOT)/lib
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

$(OBJDIR)/version.h : talk2nxt.prj
	(grep Project-Version talk2nxt.prj | sed -e \
   "s/(\([^ ]*\) \([^ ]*\) \([^ ]*\) \([^ ]*\))/\/\/\1\n#define TOOLNAME \"\2\"\n#define MAJOR \"\3\"\n#define MINOR \"\4\"\n#define VERSION \"\3.\4\"/" \
   > $(OBJDIR)/version.h) 

$(OBJDIR)/usbmisc.o : $(SRCDIR)/usbmisc.h $(SRCDIR)/errormng.h $(SRCDIR)/errors.h

$(OBJDIR)/usbnxt.o : $(SRCDIR)/usbnxt.h $(SRCDIR)/usbmisc.h $(SRCDIR)/errormng.h \
                     $(SRCDIR)/errors.h

$(OBJDIR)/$(MAIN).o : $(SRCDIR)/usbnxt.h $(SRCDIR)/usbmisc.h $(SRCDIR)/errormng.h \
                      $(SRCDIR)/errors.h $(SRCDIR)/ezargs.h $(OBJDIR)/version.h

$(OBJDIR) :
	mkdir $(OBJDIR)

clean:
	rm -f $(OBJDIR)/*.o

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
	cp ALIRE $$sddir ; \
	cp COPYING $$sddir ; \
	cp COPYING.LESSER $$sddir ; \
	cp talk2nxt.prj $$sddir ; \
	cp $(SRCDIR)/Makefile $$sddir ; \
	cp -r $(SRCDIR) $$sddir ; \
	cp -r hotplug $$sddir ; \
	cp -r udev $$sddir ; \
	cat publish/in.index.html | sed -e s/BINDIST/$$ddir.tgz/g | sed -e s/SRCDIST/$$sddir.tgz/g > publish/index.html ; \
	tar zcvf $$sddir.tgz $$sddir ; mv $$sddir.tgz publish
	cp -r publish/* /usr/local/www/PEOPLE/raymond/edu/lego/t2n/ 
