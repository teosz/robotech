checkCompiler:
	if [ ! -f ./.binaries/nbc ]; then sh install.sh; fi

checkUploader:
	if [ ! -f ./.binaries/t2n ]; then sh install.sh;fi

build: checkCompiler
	mkdir -p ./.build/
	./.binaries/nbc main.nxc -O=./.build/main.rxe

upload: checkUploader build
	sudo ./.binaries/t2n -put ./.build/main.rxe -v
