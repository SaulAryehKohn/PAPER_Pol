import aipy
import numpy as np
import sys, os, getopt

def mapchan(infile,outfile):
	uv = aipy.miriad.UV(infile)
	f0 = uv['freq']
	df = uv['sdf']*1000
	n = uv['nchan']
	freqs = np.arange(n,dtype='float')*df + f0
	
	f = open(outfile,'w')
	print >> f, '# Channel(no.) Frequency(MHz)'
	
	for i in range(n):
		print >> f, i, freqs[i]
	
	f.close()

def main(argv):
	try: opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print 'python channel2freq.py -i <inputfile> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opts == '-h': 
			print 'python channel2freq.py -i <inputfile> -o <outputfile>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
	print 'Input file: ', inputfile
	print 'Output file: ',outputfile
	mapchan(inputfile, outputfile)

if __name__ == "__main__":
    main(sys.argv[1:])
