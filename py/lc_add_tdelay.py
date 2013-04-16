import numpy as np

def lc_add_tdelay(time, lc, tdelay, buffer=None):

    """
    NAME:
      lc_add_tdelay

    PURPOSE:
      Delay a light curve by an input time delay.  np.roll() is used to shift 
      the light curve and the "buffer" keyword can be used to avoid wrapping 
      values from the end of the light curve.
      *NOTE* - This procedure assumes uniform time spacing.  I.e., only 
      "intrinsic" light curves should be used, NOT sampled light curves.

    CALLING SEQUENCE:
      lc_add_tdelay(time, lc, tdelay, buffer=)

    INPUTS:
      time   - time in units of days
      lc     - input light curve (modified by function)
      tdelay - time delay in days

    OPTIONAL INPUTS:
      buffer - lc segment to prepend before shifting (modified by function)

    KEYWORDS:

    OUTPUTS:

    OPTIONAL OUTPUTS:

    EXAMPLES:

    COMMENTS:

    REVISION HISTORY:
      2013/02/18 - Written by Greg Dobler (KITP/UCSB)

    ------------------------------------------------------------
    """

# -------- check for sufficient time resolution
    dt    = time[1] - time[0]
    shift = tdelay/dt

    if round(shift,2) % 1 > 1e-5:
        print "LC_ADD_TDELAY: Insufficient input time resolution"
        print "LC_ADD_TDELAY:    input time resolution [dy] = ", dt
        print "LC_ADD_TDELAY:    desired time delay [dy]    = ", tdelay
        return

    shift = long(shift)



# -------- shift light curve (with buffer if input) and return
    if buffer==None:
        lc[:] = np.roll(lc,shift)
    else:
        bufflc    = np.concatenate([buffer, lc])
        lc[:]     = np.roll(bufflc, shift)[buffer.size:]
        buffer[:] = np.roll(bufflc, shift)[:buffer.size]

    return
