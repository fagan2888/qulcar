import numpy as np

def lc_noise(lc, seed_n, amp_n=None):

    """
    NAME:
      lc_noise

    PURPOSE:
      Generate a noise realization for a light curve.
      Note: Does not add the nosie realization to the input lightcurve.  I.e., 
      output is noise in Delta magnitudes NOT lc + noise.

    CALLING SEQUENCE:
      noise = lc_noise(lc, seed_n, amp_n=)

    INPUTS:
      lc     - light curve with arbitrary time sampling
      seed_n - seed for the random number generator

    OPTIONAL INPUTS:
      amp_n - percent errors in flux units (default is 3%)

    KEYWORDS:

    OUTPUTS:
      noise - noise realization at each time sampling in Delta magnitudes

    OPTIONAL OUTPUTS:

    EXAMPLES:

    COMMENTS:

    REVISION HISTORY:
      02/16/2013 - Written by Greg Dobler (KITP/UCSB)

    ------------------------------------------------------------
    """

# -------- defaults
    amp_n = 0.03 if amp_n==None else amp_n

    print "LC_NOISE: generating {0}% errors with seed={1}".format(amp_n*100., \
                                                                    seed_n)



# -------- convert to flux units
    flux = 10**(-0.4*lc)



# -------- generate random noise
    np.random.seed(seed_n)

    noise = np.random.randn(flux.size)*flux*amp_n



# -------- return noise in Delta magnitudes
    return -2.5*np.log10(noise+flux) - lc
