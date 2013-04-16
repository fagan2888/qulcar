import numpy as np

def lc_sample(time, lc, daily=None, weekly=None, season=None, index=None):
    
    """
    NAME:
      sample_lc

    PURPOSE: 
      Sample an input light curve with the appropriate cadence.
      NOTE: only intrinsic time resolutions of 0.01 dy or 1 dy are
      recognized.

    CALLING SEQUENCE:
      sample_lc(time, lc, daily=, weekly=, season=, index=):

    INPUTS:
      time - time vector in days
      lc   - intrinsic light curve

    OPTIONAL INPUTS:
      index - user defined indices at which the light curve is to be sampled

    KEYWORDS:
      daily  - daily sampling
      weekly - weekly (7 dy) sampling
      season - include season gap

    OUTPUTS:
      time_samp - input time vector sampled at appropriate points
      lc_samp   - input light curve sampled at appropriate points

    OPTIONAL OUTPUTS:

    EXAMPLES:

    COMMENTS:

    REVISION HISTORY:
      2013/02/14 - Written by Greg Dobler (KITP/UCSB)

    ------------------------------------------------------------
    """

# -------- user defined sampling
    if index!=None:
        return time[index], lc[index]



# -------- initialize sampled light curve
    time_samp, lc_samp = time, lc



# -------- sampling
    if daily:
        index = np.where((time*1e5).round() % 1.0e5 == 0)
    elif weekly:
        index = np.where((time*1e5).round() % 7.0e5 == 0)

    time_samp, lc_samp = time[index], lc[index]



# -------- create season gap (seasons are 120 days on 365-120=245 days off)
    if season:
        tstart = 365.*np.arange(10.)
        tend   = tstart + 120.
        nsea   = tstart.size

        for isea in np.arange(nsea):
            tind  = np.where((time_samp >= tstart[isea]) & \
                                 (time_samp < tend[isea]))[0]
            index = tind if isea==0 else np.concatenate([index,tind])

        time_samp, lc_samp = time_samp[index], lc_samp[index]


    return time_samp, lc_samp
