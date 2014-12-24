#!/bin/bash

CAL=psa819_v008
FILES=`/data4/paper/sak/Polar_gits/PAPER_Pol/pull_args.py $*`

for FILE in $FILES; do
	echo $FILE
	echo ==========
	
	for pol in xx yy; do
	
		echo mk_img.py -C ${CAL} -s zen --size=500 --res=0.3 -c 60_160 -a cross -p ${pol} ${FILE} \
			--fmt=${FILE}_BB${pol}_%02d --minuv=35
		mk_img.py -C ${CAL} -s zen --size=500 --res=0.3 -c 60_160 -a cross -p ${pol} ${FILE} \
			--fmt=${FILE}_BB${pol}_%02d --minuv=35
	
	done
	echo ==========
done
