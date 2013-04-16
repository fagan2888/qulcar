import pyfits as fits
from lc_lightcurve import *

def lc_read(filename, path=None):

    """
    NAME:
      lc_read

    PURPOSE:
      Read a lightcurve instance from a file.

    CALLING SEQUENCE:
      lc = lc_read(filename, path=)

    INPUTS:
      filename - name of fits (binary table) file

    OPTIONAL INPUTS:
      path - path for the filename (default is present directory)

    KEYWORDS:

    OUTPUTS:
      lc - a lightcurve instance

    OPTIONAL OUTPUTS:

    EXAMPLES:

    COMMENTS:

    REVISION HISTORY:
      2013/02/18 - Written by Greg Dobler (KITP/UCSB)

    ------------------------------------------------------------
    """

# -------- utilties
    input = (path if path else '') + filename
    lc    = lightcurve(1,1) # initialize lightcurve



# -------- read in the data
    tbl = fits.getdata(input)



# -------- unpack and put into lc
    lc.seed      = tbl.seed[0]
    lc.meanmag   = tbl.meanmag[0]
    lc.mag0      = tbl.mag0[0]
    lc.tau       = tbl.tau[0]
    lc.sigma     = tbl.sigma[0]
    lc.time      = tbl.time[0]
    lc.lc        = tbl.lc[0]
    lc.time_samp = tbl.time_samp[0]
    lc.lc_samp   = tbl.lc_samp[0]
    lc.noise     = tbl.noise[0]
    lc.time_sp   = tbl.time_sp[0]
    lc.lc_sp     = tbl.lc_sp[0]
    lc.daily     = tbl.daily[0]
    lc.weekly    = tbl.weekly[0]
    lc.season    = tbl.season[0]
    lc.usrind    = tbl.usrind[0]
    lc.seed_n    = tbl.seed_n[0]
    lc.amp_n     = tbl.amp_n[0]
    lc.tdelay    = tbl.tdelay[0]
    lc.lc_buff   = tbl.lc_buff[0]

    return lc
