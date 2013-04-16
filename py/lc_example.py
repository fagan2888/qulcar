import numpy as np
import matplotlib.pyplot as plt
import copy as cp
import SLTimeDelayChallenge as tdc

"""
NAME:
  lc_example

PURPOSE:

  Script to Walk through some of the functionality of the lightcurve
  class and tdc/py/ functions.  This script should execute without
  errors as long the tdc/ folder is in your python path.  NOTE:
  disable "ion" in matplotlib to get the most out of these examples.
  Required modules are:
    scipy
    numpy
    pyfits
    matplotlib

CALLING SEQUENCE:
  none - e.g., >>> execfile('lc_example.py')

INPUTS:
  none

OPTIONAL INPUTS:

KEYWORDS:

OUTPUTS:
  none

OPTIONAL OUTPUTS:

EXAMPLES:

COMMENTS:

REVISION HISTORY:
  2013/02/20 - Written by Greg Dobler (KITP/UCSB)

------------------------------------------------------------
"""

# -------- set up some parameters that can be used as inputs of the
# -------- lightcurve class (see lc_lightcurve.py for documentation)
    
seed    = 111    # required input to lightcurve class
seed_n  = 222    # required input to lightcurve class

meanmag = 21.2   #
mag0    = 22.5   #
tau     = 350.   # optional inputs
sigma   = 7.5e-3 #
amp_n   = 0.01   #



print
print "  Let's initialize a lightcurve instance using defaults defined in "
print "  the lc_example.py script which you are running."
print "    lc = tdc.lightcurve(seed, seed_n, meanmag=meanmag, mag0=mag0, \ "
print "                            tau=tau, sigma=sigma, amp_n=amp_n)"

lc = tdc.lightcurve(seed, seed_n, meanmag=meanmag, mag0=mag0, tau=tau, \
                        sigma=sigma, amp_n=amp_n)

print
print "  The light curve instance has been initialized.  Here's what's "
print "  inside the class:"
print "    print lc.names"
print
print lc.names

print
print "  The initialization process produces an initial light curve that "
print "  is sampled with a daily cadence:"
print "    print lc.time.size, lc.lc.size, lc.time[1] - lc.time[0]"
print
print lc.time.size, lc.lc.size, lc.time[1] - lc.time[0]

print
print "  This initialization is just for illustrative purposes.  You "
print "  certainly want a light curve with >1 day intrinsic resolution "
print "  so use lc.car_gen().  By default this will produce a light curve "
print "  (and reset lc.time and lc.lc) with a resolution of 0.01 day."
print "  This generation takes about 30min.  For this example, we'll use "
print "  medium resolution which should take about a minute... hang on."
print "    lc.car_gen(medres=1)"
print
lc.car_gen(medres=1)

print
print "  Now you can plot the intrinsic light curve."
print
plt.figure()
plt.plot(lc.time, lc.lc)
plt.title('An example light curve with seed = {0}'.format(seed),fontsize=15)
plt.xlabel('time [day]', fontsize=15)
plt.ylabel('magnitude', fontsize=15)
plt.show()


print
print "  Next step is to sample the light curve.  There are various flags "
print "  to modify the sampling (see lc_sample.py)."
print "    lc.sample(weekly=1, season=1)"
print
lc.sample(weekly=1, season=1)

print
print "  This process also generates a noise realization lc.noise.  Thus, "
print "  for the full data realization you want to add the sampled light "
print "  curve to the noise.  e.g. lc.lc_samp + lc.noise"


print
print "  You can now overplot the sampled points on your light curve."
print "  Note: the intrinsic light lightcurve lc.lc is not destroyed, "
print "  the sampling is put into lc.time_samp and lc.lc_samp.  Also note "
print "  that, if you zoom in, you can see the effect of the noise added in "
print "  as described above."
plt.plot(lc.time, lc.lc)
plt.title('An example light curve with seed = {0}'.format(seed),fontsize=15)
plt.xlabel('time [day]', fontsize=15)
plt.ylabel('magnitude', fontsize=15)
plt.plot(lc.time_samp, lc.lc_samp+lc.noise, 'o')
plt.show()


print
print "  Now imagine we have two images."
print "  We can add a time delay to the intrinsic light curve (so long as the "
print "  resolution of that time delay does not exceed the resolution of "
print "  our intrinsic light curve.  Several of important points: "
print "    1. the time delay is added by tacking lc_buff onto lc and shifting"
print "    2. the implication of 1. is that the max time delay=2 yr (buff sz)"
print "    3. ***both lc.lc and lc.lc_buff are modified when adding a delay***"
print
print "    lcA = cp.deepcopy(lc)"
print "    lcB = cp.deepcopy(lc)"
print "    lcB.add_tdelay(14.7)"
print
print "  And plot them."
lcA = cp.deepcopy(lc)
lcB = cp.deepcopy(lc)
lcB.add_tdelay(14.7)

plt.plot(lcA.time, lcA.lc)
plt.plot(lcB.time, lcB.lc)
plt.title(r'Example: seed = {0}, $\Delta t_B = 14.7$ day'.format(seed), \
              fontsize=15)
plt.xlabel('time [day]', fontsize=15)
plt.ylabel('magnitude', fontsize=15)
plt.show()


print
print "  lcB sampled light curve has been reset to the intrinsic curve:"
print "    print lcB.lc_samp - lcB.lc"
print lcB.lc_samp - lcB.lc
print
print "  Re-sample lcB with a different noise realization..."
print "    lcB.sample(seed_n=54)"
lcB.sample(weekly=1, season=1,seed_n=54)

print
print "  ...and plot."
plt.plot(lcA.time_samp, lcA.lc_samp+lcA.noise, 'o')
plt.plot(lcB.time_samp, lcB.lc_samp+lcB.noise, '*')
plt.title(r'Example: seed = {0}, $\Delta t_B = 14.7$ day'.format(seed), \
              fontsize=15)
plt.xlabel('time [day]', fontsize=15)
plt.ylabel('magnitude', fontsize=15)
plt.show()


print
print "  Lastly, the lightcurve class includes a spline interpolator for "
print "  the sampled light curve.  It does not take into account the season "
print "  gaps and so is (of course) highly inaccurate where there is "
print "  missing data.  E.g., :"
print "    lcA.spline()"
print "    lcB.spline()"
lcA.spline()
lcB.spline()

print
print "  ...and make the plot."
plt.plot(lcA.time_samp, lcA.lc_samp+lcA.noise, 'o')
plt.plot(lcB.time_samp, lcB.lc_samp+lcB.noise, '*')
plt.plot(lcA.time_sp, lcA.lc_sp)
plt.plot(lcB.time_sp, lcB.lc_sp)
plt.title(r'Example: seed = {0}, $\Delta t_B = 14.7$ day'.format(seed), \
              fontsize=15)
plt.xlabel('time [day]', fontsize=15)
plt.ylabel('magnitude', fontsize=15)
plt.ylim([20.75,21.75])
plt.show()


print
print "  Last thing to do is write out some files.  'Evil' files are files "
print "  containing lightcurve instances (i.e., including all the meta data) "
print "  and 'good' files only contain sampled light curves (and the "
print "  associated times.  First we write evil files containing lightcurve "
print "  instances lcA and lcB.  Note: these will be written to the "
print "  current directory; for other directories use the 'path' keyword."
print "    lcA.write('evil_file_lcA.fits', clobber=1) "
print "    lcB.write('evil_file_lcB.fits', clobber=1) "
lcA.write('evil_file_lcA.fits', clobber=1)
lcB.write('evil_file_lcB.fits', clobber=1)

print
print "  Evil files containing lightcurve instances can be read in directly "
print "  by initializing a lightcurve instance with the 'filename' keyword. "
print "  For example:"
print "    lcA_copy = tdc.lightcurve(-1,-1,filename='evil_file_lcA.fits') "
lcA_copy = tdc.lightcurve(-1,-1,filename='evil_file_lcA.fits')

print
print "  Finally, the lightcurve class presently does not contain a method "
print "  for writing good files (to avoid confusion).  Instead, the function "
print "  lc_write() should be used; as in "
print "    tdc.lc_write(lcA.time_samp, [lcA.lc_samp+lcA.noise, \ "
print "                                 lcB.lc_samp+lcB.noise], \ "
print "                      'good', 'good_file_lcAB.fits', \ "
print "                      errlcs=[amp_n, amp_n], clobber=1)"
tdc.lc_write(lcA.time_samp, [lcA.lc_samp+lcA.noise, lcB.lc_samp+lcB.noise], \
                 'good', 'good_file_lcAB.fits', errlcs=[amp_n,amp_n], \
                 clobber=1)
