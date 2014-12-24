#$ -S /bin/bash
#$ -V
#$ -cwd
#$ -j y
#$ -N MDLVISIB
#$ -o grid_output/
#$ -l h_vmem=2G
#$ -t 1:20
echo 'here we go!'
echo 'NOTE: this only effects the xx and yy visibilities.'
source /usr/global/paper/CanopyVirtualEnvs/PAPER_Polar/bin/activate

CAL=psa819_v008
FILES=`/data4/paper/sak/Polar_gits/PAPER_Pol/pull_args.py $*`

for FILE in $FILES; do
    echo $FILE
    echo ===============================
    echo mdlvis.py -C ${CAL} -s all --pol=xx,yy -m add -f ${FILE}
    mdlvis.py -C ${CAL} -s all --pol=xx,yy -m add -f ${FILE}    
done
