#!/bin/bash


FILES=`/data4/paper/sak/Polar_gits/PAPER_Pol/pull_args.py $*`

for pol in I Qrot Urot V; do
	for f in `seq 0 24`; do
		mk_map.py -m map_FB${f}_${pol}.fits --nside=256 $FILES
		
