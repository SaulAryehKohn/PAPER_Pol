IQUV image pipeline
=====================
batch_mk_df_images.sh: "qsub -l paper batch_mk_images.sh /path/to/*.uvcRRE"

	- right now it runs a calibration before imaging. This can be disabled.
	- 4 snapshots per frequency, per time
	- for a given time: xx, xy, yx, yy in <N> frequency bands
	
lin2stokes.py: "python lin2stokes.py -f <freq_of_band> -C <calfile> xx.fits xy.fits yx.fits yy.fits"
 
	- keeps track of different weights for different beams
	- 4 new files per frequency, per time
	- for a given time: I, Q, U, V in <N> frequency bands
	
QUrot.py: "python QUrot.py Q.fits U.fits"

	- As the sky passes overhead, an original Q will rotate into U and vice-versa
	- this corrects for LST changes, outputting Q, U, P=Q+U and X="polarization-angle map" (in P?)
	
mk_snap_map.py:

	- creates a "mosaic" healpix map
	- TODO: needs to treat polarizations a la aipy 2.0!
	- TODO: add pol option to optparse
	
hpm_extract_facet.py:

	- make a cutout from the healpix map in a sine projection


Some compressed imaging data: 

	- /data4/raw_data/Sep2011/psa819, 820
	- /data4/raw_data/Jul2011/psa74*
		-- these two together should provide the entire Southern Hemisphere!
	- Preliminary calibrations in capo/dfm


TAKE CARE:

	- images are highly affected by the shape of the beam 
	- leakage terms in gain operator ("d terms") are very important.
		-- are these implemented?
	
READ:

	- TMS (edition 2+) chapters on geometry, chapters 3 and 6 (generally)
	- Hamaker, Bregman and Sault: 5 papers on "understanding radio polarimetry"... PAPER breaks most of their assumptions 
	- DFMs polarization papers
	- Perley & Smirnoff: MeqTree shows how useful polarization calibration can be
