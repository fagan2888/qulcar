import numpy as np
import sys

def lc_car_gen(seed, meanmag=None, mag0=None, year=None, tau=None, \
                   sigma=None, lores=None, medres=None):
    """
    NAME:
      lc_car_gen
    
     PURPOSE:
      Generate a mock light curve using a 1/frequency^2 power spectrum
      (see Kelly et al 2009, ApJ, 698, 895)
      (note: error in Kelly et al FIG 1 label [mag^2 day^-1] -> [mag^2 day])
    
     CALLING SEQUENCE:
      lc = lc_car_gen(seed, meanmag=, mag0=, year=, tau=, sigma=, lores=)
    
     INPUTS:
      seed - the seed for the random phase
    
     OPTIONAL INPUTS:
      meanmag - mean magnitude of the light curve (default 20)
      mag0    - magnitude at t=0 (default meanmag)
      year    - number of years to run the light curve (default 10)
      tau     - characteristic time scale (default 10^2.5 day)
      sigma   - characteristic fluctuation amp (default 8d-3 mag day^-1/2) 
    
     KEYWORDS:
      lores  - use 1.0 dy sampling instead of 0.01 dy
      medres - use 0.1 dy sampling instead of 0.01 dy
    
     OUTPUTS:
      time - in days
      lc   - light curve as a function of time [mag]
    
     OPTIONAL OUTPUTS:
    
     EXAMPLES:
    
     COMMENTS:
      Uses the continuous auto regressive, CAR(1), method outlined in
      Kelly et al (2009)
    
     REVISION HISTORY:
      2013/01/17 - converted from IDL by Greg Dobler (KITP/UCSB)
      2013/02/14 - modfied for hires run by default
    
    ------------------------------------------------------------
    """

# -------- Defaults
    print 'LC_CAR_GEN: Using seed = ', seed

    if not meanmag : meanmag = 20.0
    if not mag0    : mag0    = meanmag
    if not year    : year    = 10L
    if not tau     : tau     = 10.**2.5 # [day]
    if not sigma   : sigma   = 8e-3 # [mag day^-1/2]



# -------- Define the time vector for the lightcurve and initialize
    resfac = 1L if lores else 10L if medres else 100L

    duration = long(365L*resfac*year) # [day/resfac]
    time     = np.arange(0,duration,1.0)
    lc       = np.zeros(time.size)



# -------- Convert tau and sigma
    tau   *= float(resfac) # [day/resfac]
    sigma /= np.sqrt(float(resfac)) # [mag (day/resfac)^1/2]



# -------- Make the using equation (A3)
    np.random.seed(seed)

    dt  = time[1] - time[0]
    dBs = dt*np.random.randn(duration)
    dtj = np.arange(duration-1,0,-1.)
    rf  = sigma*dBs

    lc  = mag0*np.exp(-time/tau) + meanmag*(1.0 - np.exp(-time/tau))

    for itime in range(1,duration-1,1):
        if itime % 1000 == 0 : 
            print 'LC_CAR_GEN: {0} steps out of {1}\r'.format(itime,duration),
            sys.stdout.flush()

        lc[itime] += np.add.reduce(rf[0:itime] * \
                                np.exp(-dtj[duration-1-itime:duration-1]/tau))
    print



# -------- set time vector appropriately and return
    time /= float(resfac)

    return time, lc
