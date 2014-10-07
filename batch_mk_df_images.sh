#$ -S /bin/bash
#$ -V
#$ -cwd
#$ -j y
#$ -N FINE_IMG
#$ -o grid_output/
#$ -l h_vmem=1G

source /usr/global/paper/bin/virtualenvwrapper.sh
workon sak-test

#export PATH = $PATH:/data2/home/saulkohn/githubs/PAPER_Pol
#LD_LIBRARY_PATH = $LD_LIBRARY_PATH:where the lib is
#export LD_LIBRARY_PATH 

CAL=psa819_v007
FILES=`/data2/home/saulkohn/githubs/PAPER_Pol/pull_args.py $*`

FSTART=120
FSTOP=170
NCHAN=$(($FSTOP-$FSTART))
df=$(($NCHAN/32))

for FILE in $FILES; do
    echo ===============================
    for i in `seq 0 31`; do
        echo =========
        f0=$(($i*$df+$FSTART))
        f1=$(($f0+$df))
    
        for pol in xx xy yx yy; do
            echo mk_img.py -C ${CAL} -s zen --size=500 --res=0.3 -c ${f0}_${f1} -a cross -p ${pol} ${FILE} \
                --fmt=${FILE}_FB${i}${pol}_%04d
            mk_img.py -C ${CAL} -s zen --size=500 --res=1. -c ${f0}_${f1} -a cross -p ${pol} ${FILE} \
                --fmt=${FILE}_FB${i}${pol}_%04d
        
        done    
    done
done
