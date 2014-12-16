#!/bin/bash
echo 'rm -rf /data2/home/saulkohn/Polar_gits/PAPER_Pol/psa819/zen.2455819.55853.uvcRREs'
rm -rf /data2/home/saulkohn/Polar_gits/PAPER_Pol/psa819/zen.2455819.55853.uvcRREs
echo 'mdlvis.py -C psa819_v008_SK -s <STUFF> --pol=xx -m sub -f /data2/home/saulkohn/Polar_gits/PAPER_Pol/psa819/zen.2455819.55853.uvcRRE'
mdlvis.py -C psa819_v008_SK -s forone,fortwo,forcore,forcan1,forcan2,forcan3,forcan4,forcan5,forcan6,forcan7,forcan8,forcan9,forcan10,forcan11,forcan12,forcan13,forcan14,forcan15,source1 --pol=xx -m sub -f /data2/home/saulkohn/Polar_gits/PAPER_Pol/psa819/zen.2455819.55853.uvcRRE
echo 'mk_img.py -C psa819_v008_SK -s zen --size=500 --res=0.3 -c 61_143 -a cross -p xx ./psa819/zen.2455819.55853.uvcRREs --fmt=imagewcore%04d --minuv=45 --no_w'
mk_img.py -C psa819_v008_SK -s zen --size=500 --res=0.3 -c 61_143 -a cross -p xx ./psa819/zen.2455819.55853.uvcRREs --fmt=imagewcore%04d --minuv=45 --no_w
