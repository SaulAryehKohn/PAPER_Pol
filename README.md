IQUV image pipeline
=====================
batch_mk_df_images.sh:

	- 4 snapshots per frequency
	- 1 snapshot per time -- a combination of I, Q and U
	
lin2stokes.py:

	- keeps track of different weights for different beams
	- rotates all frames into same basis for easy working
	- 4 snapshots -> 4 *corrected* snapshots
	
QUrot.py:

	- As the sky passes overhead, an original Q will rotate into U and vice-versa
	- this corrects for LST changes, outputting Q, U, P=Q+U and a polarization-angle map
	
mk_snap_map.py:

	- creates a "mosaic" healpix map
	
hpm_extract_facet.py:

	- make a cutout from the healpix map in a sine projection


Some compressed imaging data: 

	- /data4/raw_data/Sep2011/psa819, 820
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
