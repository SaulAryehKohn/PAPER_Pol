#!/usr/global/paper/bin/python
"""
Models visibilities for various catalog sources and creates a new Miriad UV
file containing either the simulated data, or the residual when the model
is removed from measured data.

Author: Aaron Parsons
"""
import numpy as n, aipy as a, optparse, os, sys, ephem

o = optparse.OptionParser()
o.set_usage('mdlvis.py [options] *.uv')
o.set_description(__doc__)
a.scripting.add_standard_options(o, ant=True, cal=True, src=True)
o.add_option('-m','--mode', dest='mode', default='sim',
    help='Operation mode.  Can be "sim" (output simulated data), "sub" (subtract from input data), or "add" (add to input data).  Default is "sim"')
o.add_option('-f', '--flag', dest='flag', action='store_true',
    help='If outputting a simulated data set, mimic the data flagging of the original dataset.')
o.add_option('-n', '--noiselev', dest='noiselev', default=0., type='float',
    help='RMS amplitude of noise (Jy) added to each UV sample of simulation.')
o.add_option('--nchan', dest='nchan', default=256, type='int',
    help='Number of channels in simulated data if no input data to mimic.  Default is 256')
o.add_option('--sfreq', dest='sfreq', default=.075, type='float',
    help='Start frequency (GHz) in simulated data if no input data to mimic.  Default is 0.075')
o.add_option('--sdf', dest='sdf', default=.150/256, type='float',
    help='Channel spacing (GHz) in simulated data if no input data to mimic.  Default is .150/256')
o.add_option('--inttime', dest='inttime', default=10, type='float',
    help='Integration time (s) in simulated data if no input data to mimic.  Default is 10')
o.add_option('--startjd', dest='startjd', default=2454600., type='float',
    help='Julian Date to start observation if no input data to mimic.  Default is 2454600')
o.add_option('--endjd', dest='endjd', default=2454601., type='float',
    help='Julian Date to end observation if no input data to mimic.  Default is 2454601')
o.add_option('--pol', dest='pol', 
    help='Polarizations to simulate (xx,yy,xy,yx) if starting file from scratch.')
opts, args = o.parse_args(sys.argv[1:])

assert(len(args) > 0 or (opts.mode == 'sim' and not opts.flag and not (opts.pol is None)))
# Parse command-line options
if len(args) > 0:
    uv = a.miriad.UV(args[0])
    aa = a.cal.get_aa(opts.cal, uv['sdf'], uv['sfreq'], uv['nchan'])
    p,d,f = uv.read(raw=True)
    no_flags = n.zeros_like(f)
    del(uv)
else:
    aa = a.cal.get_aa(opts.cal, opts.sdf, opts.sfreq, opts.nchan)
    no_data = n.zeros(opts.nchan, dtype=n.complex64)
    no_flags = n.zeros(opts.nchan, dtype=n.int32)

# Generate a model of the sky with point sources and a pixel map

# Initialize point sources
srclist,cutoff,catalogs = a.scripting.parse_srcs(opts.src, opts.cat)
cat = a.cal.get_catalog(opts.cal, srclist, cutoff, catalogs)
mfq = cat.get('mfreq')
a1s,a2s,ths = cat.get('srcshape')
dras, ddecs = cat.get('ionref')


## Initialize pixel map

# A pipe for applying the model
curtime = None
def mdl(uv, p, d, f):
    global curtime, eqs
    uvw, t, (i,j) = p
    print 'p=',p
    pol = a.miriad.pol2str[uv['pol']]
    if i == j: return p, d, f
    if curtime != t:
    	print 'curtime=',curtime,'t=',t
        curtime = t
        aa.set_jultime(t)
        cat.compute(aa)
        eqs = cat.get_crds('eq', ncrd=3)
        print 'eqs=',eqs
        flx = cat.get_jys()
        print 'flx=',flx
        aa.sim_cache(eqs, flx, mfreqs=mfq,ionrefs=(dras,ddecs), srcshapes=(a1s,a2s,ths))
    aa.set_active_pol(pol)
    sd = aa.sim(i, j)
    print 'SD=',sd
    if opts.mode.startswith('sim'):
        d = sd
        if not opts.flag: f = no_flags
    elif opts.mode.startswith('sub'):
        d -= sd
    elif opts.mode.startswith('add'):
        d += sd
    else:
        raise ValueError('Mode "%s" not supported.' % opts.mode)
    if opts.noiselev != 0:
        # Add on some noise for a more realistic experience
        noise_amp = n.random.random(d.shape) * opts.noiselev
        noise_phs = n.random.random(d.shape) * 2*n.pi * 1j
        noise = noise_amp * n.exp(noise_phs)
        d += noise * aa.passband(i,j)
    return p, n.where(f, 0, d), f

if len(args) > 0:
    # Run mdl on all files
    for filename in args:
        uvofile = filename + 's'
        print filename,'->',uvofile
        if os.path.exists(uvofile):
            print 'File exists: skipping'
            continue
        uvi = a.miriad.UV(filename)
        a.scripting.uv_selector(uvi, opts.ant)
        uvo = a.miriad.UV(uvofile, status='new')
        uvo.init_from_uv(uvi)
        uvo.pipe(uvi, mfunc=mdl, raw=True, append2hist="MDLVIS: " + ' '.join(sys.argv) + '\n')
else:
    # Initialize a new UV file
    pols = opts.pol.split(',')
    uv = a.miriad.UV('new.uv', status='new')
    uv._wrhd('obstype','mixed-auto-cross')
    uv._wrhd('history','MDLVIS: created file.\nMDLVIS: ' + ' '.join(sys.argv) + '\n')
    uv.add_var('telescop','a'); uv['telescop'] = 'AIPY'
    uv.add_var('operator','a'); uv['operator'] = 'AIPY'
    uv.add_var('version' ,'a'); uv['version'] = '0.0.1'
    uv.add_var('epoch'   ,'r'); uv['epoch'] = 2000.
    uv.add_var('source'  ,'a'); uv['source'] = 'zenith'
    uv.add_var('latitud' ,'d'); uv['latitud'] = aa.lat
    uv.add_var('dec'     ,'d'); uv['dec'] = aa.lat
    uv.add_var('obsdec'  ,'d'); uv['obsdec'] = aa.lat
    uv.add_var('longitu' ,'d'); uv['longitu'] = aa.long
    uv.add_var('npol'    ,'i'); uv['npol'] = len(pols)
    uv.add_var('nspect'  ,'i'); uv['nspect'] = 1
    uv.add_var('nants'   ,'i'); uv['nants'] = len(aa)
    uv.add_var('antpos'  ,'d')
    antpos = n.array([ant.pos for ant in aa], dtype=n.double)
    uv['antpos'] = antpos.transpose().flatten()
    uv.add_var('sfreq'   ,'d'); uv['sfreq'] = opts.sfreq
    uv.add_var('freq'    ,'d'); uv['freq'] = opts.sfreq
    uv.add_var('restfreq','d'); uv['restfreq'] = opts.sfreq
    uv.add_var('sdf'     ,'d'); uv['sdf'] = opts.sdf
    uv.add_var('nchan'   ,'i'); uv['nchan'] = opts.nchan
    uv.add_var('nschan'  ,'i'); uv['nschan'] = opts.nchan
    uv.add_var('inttime' ,'r'); uv['inttime'] = float(opts.inttime)
    # These variables just set to dummy values
    uv.add_var('vsource' ,'r'); uv['vsource'] = 0.
    uv.add_var('ischan'  ,'i'); uv['ischan'] = 1
    uv.add_var('tscale'  ,'r'); uv['tscale'] = 0.
    uv.add_var('veldop'  ,'r'); uv['veldop'] = 0.
    # These variables will get updated every spectrum
    uv.add_var('coord'   ,'d')
    uv.add_var('time'    ,'d')
    uv.add_var('lst'     ,'d')
    uv.add_var('ra'      ,'d')
    uv.add_var('obsra'   ,'d')
    uv.add_var('baseline','r')
    uv.add_var('pol'     ,'i')

    # Now start generating data
    times = n.arange(opts.startjd, opts.endjd, opts.inttime/a.const.s_per_day)
    for cnt,t in enumerate(times):
        print 'Timestep %d / %d' % (cnt+1, len(times))
        aa.set_jultime(t)
        uv['lst'] = aa.sidereal_time()
        uv['ra'] = aa.sidereal_time()
        uv['obsra'] = aa.sidereal_time()
        # XXX should really honor opts.ants for which antennas to simulate here.
        for i,ai in enumerate(aa):
            for j,aj in enumerate(aa):
                try:
                    if ai.pol+aj.pol not in pols: continue
                    i,j = ai.num,aj.num
                except(AttributeError): pass
                if j < i: continue
                crd = aa.get_baseline(i,j)
                preamble = (crd, t, (i,j))
                for pol in pols:
                    uv['pol'] = a.miriad.str2pol[pol]
                    preamble,data,flags = mdl(uv, preamble, None, None)
                    if data is None:
                        data = no_data
                        flags = no_flags
                    uv.write(preamble, data, flags)
    del(uv)