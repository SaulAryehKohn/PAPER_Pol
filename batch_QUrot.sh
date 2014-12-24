#$ -S /bin/bash
#$ -V
#$ -cwd
#$ -j y
#$ -N HELPMEIM
#$ -o grid_output/
#$ -l h_vmem=2G
#$ -t 1:20

echo 'here we go!'
source /usr/global/paper/CanopyVirtualEnvs/PAPER_Polar/bin/activate

CAL=psa819_v008
FILES=`/data4/paper/sak/Polar_gits/PAPER_Pol/pull_args.py $*`
step=0.005
FSTART=0.132
#call files as psa819/*FB0xx_0000.dim.fits

for FILE in $FILES; do
	NAME=${FILE:7:17}
	echo =================
	echo $NAME
	echo =================
	for (( i=0; $i<$(bc<<<"10"); i++ )); do
		python QUrot.py psa819/${NAME}.uvcRRE_FB${i}Q_0000.dim.fits psa819/${NAME}.uvcRRE_FB${i}U_0000.dim.fits
	done
done
