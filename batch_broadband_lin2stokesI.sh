#$ -S /bin/bash
#$ -V
#$ -cwd
#$ -j y
#$ -N BB_2STKS
#$ -o grid_output/
#$ -l h_vmem=2G
#$ -t 1:15

echo 'here we go!'
source /usr/global/paper/CanopyVirtualEnvs/PAPER_Polar/bin/activate

CAL=psa819_v008
FILES=`/data4/paper/sak/Polar_gits/PAPER_Pol/pull_args.py $*`
#call files as psa819/*BB0xx_0000.dim.fits

for FILE in $FILES; do
	NAME=${FILE:7:17}
	echo =================
	echo $NAME
	echo python broadband_lin2stokesI.py -C ${CAL} -f ${f} psa819/${NAME}.uvcRREs_BB${i}xx_0000.dim.fits \
		psa819/${NAME}.uvcRREs_BB${i}yy_0000.dim.fits

	python broadband_lin2stokesI.py -C ${CAL} -f ${f} psa819/${NAME}.uvcRREs_BB${i}xx_0000.dim.fits \
		psa819/${NAME}.uvcRREs_BB${i}yy_0000.dim.fits
done
