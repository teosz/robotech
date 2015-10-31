DIR="$(pwd)"

rm -rf /tmp/nbc
rm -rf /tmp/t2n
mkdir -p /tmp/nbc
mkdir -p /tmp/t2n
mkdir -p .binaries
if [ ! -f ./.binaries/nbc ]; then
    wget http://heanet.dl.sourceforge.net/project/bricxcc/NBC_NXC/NBC%20release%201.2.1%20r4/nbc-1.2.1.r4.tgz -O /tmp/nbc.tgz
    tar xzvf nbc-1.2.1.r4.tgz -C /tmp/nbc
    cp /tmp/nbc/NXT/nbc ./.binaries/nbc
fi


if [ ! -f ./.binaries/t2n ]; then
  wget http://www-verimag.imag.fr/~raymond/edu/lego/t2n/files/t2n-0.6.src.tgz -O /tmp/t2n.tgz
  tar xzvf t2n-0.6.src.tgz  -C /tmp/t2n
  cd /tmp/t2n/t2n-0.6.src/
  make
  cd $DIR
  cp -rf /tmp/t2n/t2n-0.6.src/obj ./.binaries/.t2n_source
  ln ./.binaries/.t2n_source/t2n ./.binaries/t2n
fi
