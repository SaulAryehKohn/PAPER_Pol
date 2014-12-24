import glob


#this ONLY WORKS because I have < 11 freq bins and they're indexed
#from zero, so no double digits

freqbin_list = range(10)
pol_list = ['xx','xy','yx','yy']
zen_name_list = []
for name in glob.glob('psa819/*FB0xx_0000.dim.fits'):
    #zen_name = name[7:-27]
    #freqbin = name[34:-16]
    #pol = name[35:-14]
    zen_name_list.append(name[7:-27])

FILE = open('lin2stokescommands.txt','w')

for name in zen_name_list:
    print name
    for f in freqbin_list:
        GHzFreq = (132 + 5*f)/1000.
        print >> FILE, 'python lin2stokes.py -f '+str(GHzFreq)+' -C psa819_v008 psa819/'+name+'.uvcRRE_FB'+str(f)+'xx_0000.dim.fits psa819/'+name+'.uvcRRE_FB'+str(f)+'xy_0000.dim.fits psa819/'+name+'.uvcRRE_FB'+str(f)+'yx_0000.dim.fits psa819/'+name+'.uvcRRE_FB'+str(f)+'yy_0000.dim.fits '
FILE.close()
