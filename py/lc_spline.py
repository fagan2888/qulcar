import numpy as np
from scipy import interpolate

def lc_spline(x, y, xr=None, nx=None, wgt=None):

    """
    NAME:
      lc_spline

    PURPOSE:
      1D spline interpolate through input data.  A wrapper for the
      scipy.interpolate spine functions.

    CALLING SEQUENCE:
      x_sp, y_sp = spline_interp(x, y, xr=, nx=, wgt=)

    INPUTS:
      x - independent data
      y - dependent data

    OPTIONAL INPUTS:
      xr  - range for the splined xvalues, x_sp (default is x.max - x.min)
      nx  - number of x_sp points over xr (default is 100)
      wgt - weights for the interpolation (no default; i.e., uniform wgts)

    KEYWORDS:

    OUTPUTS:
      x_sp - splined xvalues
      y_sp - spline interpolated yvalues

    OPTIONAL OUTPUTS:

    EXAMPLES:

    COMMENTS:

    REVISION HISTORY:
      2013/02/15 - Written by Greg Dobler (KITP/UCSB)

    ------------------------------------------------------------
    """

# -------- defaults
    xr = [x.min(), x.max()] if xr==None else xr
    nx = 100L if nx==None else nx



# -------- utilities
    dx   = (xr[1]-xr[0])/float(nx)
    x_sp = np.arange(xr[0],xr[1]+dx,dx)



# -------- spline interpolate and return
    tck  = interpolate.splrep(x, y, wgt, s=0)
    y_sp = interpolate.splev(x_sp , tck, der=0)

    return x_sp, y_sp
