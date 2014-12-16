#$ -S /bin/bash
#$ -V
#$ -cwd
#$ -j y
#$ -N FINE_IMG
#$ -o grid_output/
#$ -l h_vmem=2G
#$ -t 1:20
echo 'here we go!'
source /usr/global/paper/CanopyVirtualEnvs/PAPER_Polar/bin/activate

CAL=psa819_v008
FILES=`/data2/home/saulkohn/Polar_gits/PAPER_Pol/pull_args.py $*`

FSTART=60
FSTOP=160
NCHAN=$(($FSTOP-$FSTART))
df=$(($NCHAN/10))

echo $FSTART $FSTOP $NCHAN $df

for FILE in $FILES; do
    echo $FILE
    echo ===============================
    for i in `seq 0 9`; do
        echo =========
        f0=$(($i*$df+$FSTART))
        f1=$(($f0+$df))
    
        for pol in xx xy yx yy; do
            echo mk_img.py -C ${CAL} -s zen --size=500 --res=0.32 -c ${f0}_${f1} -a cross -p ${pol} ${FILE} \
                --fmt=${FILE}_FB${i}${pol}_%04d --minuv=35
            mk_img.py -C ${CAL} -s zen --size=500 --res=0.32 -c ${f0}_${f1} -a cross -p ${pol} ${FILE} \
                --fmt=${FILE}_FB${i}${pol}_%04d --minuv=35
        
        done    
    done
done
