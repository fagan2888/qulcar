import numpy as np
import pyfits as fits
from lc_car_gen import *
from lc_sample import *
from lc_spline import *
from lc_noise import *
from lc_add_tdelay import *
from lc_write import *

class lightcurve():

    """
      Light curve class includes the following data.
        intrinsic parameters  : seed, meanmag, mag0, tau, sigma
        intrinsic light curve : time, lc
        sampled light curve   : time_samp, lc_samp, noise
        spline of lc_samp     : time_sp, lc_sp
        sampling flags        : daily, weekly, season, usrind
        noise parameters      : seed_n, amp_n
        time delay utils      : tdelay, lc_buff
        identifier data       : dtype, names
    """

# -------- initialize the light curve parameters
    def __init__(self, seed, seed_n, meanmag=None, mag0=None, tau=None, \
                     sigma=None, amp_n=None, filename=None, path=None):

        """ Initialize the light curve parameters """

        # read in the light curve from a file
        if filename:
            input = (path if path else '') + filename
            tbl   = fits.getdata(input)

            self.seed      = tbl.seed[0]
            self.meanmag   = tbl.meanmag[0]
            self.mag0      = tbl.mag0[0]
            self.tau       = tbl.tau[0]
            self.sigma     = tbl.sigma[0]
            self.time      = tbl.time[0]
            self.lc        = tbl.lc[0]
            self.time_samp = tbl.time_samp[0]
            self.lc_samp   = tbl.lc_samp[0]
            self.noise     = tbl.noise[0]
            self.time_sp   = tbl.time_sp[0]
            self.lc_sp     = tbl.lc_sp[0]
            self.daily     = tbl.daily[0]
            self.weekly    = tbl.weekly[0]
            self.season    = tbl.season[0]
            self.usrind    = tbl.usrind[0]
            self.seed_n    = tbl.seed_n[0]
            self.amp_n     = tbl.amp_n[0]
            self.tdelay    = tbl.tdelay[0]
            self.lc_buff   = tbl.lc_buff[0]
            self.dtype     = 'lightcurve'
            self.names     = tbl.names

            return

        # initialize data type and names
        self.dtype = 'lightcurve'
        self.names = ['seed', 'meanmag', 'mag0', 'tau', 'sigma', 'time', \
                           'lc', 'time_samp', 'lc_samp', 'noise', 'time_sp', \
                           'lc_sp', 'daily', 'weekly', 'season', 'usrind', \
                           'seed_n', 'amp_n', 'tdelay', 'lc_buff']

        # initialize intrinsic lightcurve parameters
        self.seed    = seed
        self.meanmag = meanmag if meanmag else 20.0
        self.mag0    = mag0 if mag0 else self.meanmag
        self.tau     = tau if tau else 10.**2.5 # [day]
        self.sigma   = sigma if sigma else 8.0e-3 # [mag day^-1/2]

        # generate the lightcurve at low resolution
        self.time, self.lc = lc_car_gen(self.seed, meanmag=self.meanmag, \
                                            mag0=self.mag0, tau=self.tau, \
                                            sigma=self.sigma, lores=1, \
                                            year=12.)

        # initialize the buffer for time delay
        self.lc_buff = self.lc[self.time < 730.]
        self.lc      = self.lc[self.time >= 730.]
        self.time    = self.time[self.time < 3650.]
        self.tdelay  = 0.0

        # initialize the sampled lightcurve, noise, and spline model
        self.time_samp = self.time
        self.lc_samp   = self.lc
        self.noise     = np.zeros(self.lc_samp.size)
        self.time_sp   = np.zeros(self.time.size)
        self.lc_sp     = np.zeros(self.lc.size)

        # intialize the sampling parameter flags
        self.daily = self.weekly = self.season = 0
        self.usrind = np.zeros(self.time.size, dtype='byte')

        # initialize the noise parameters
        self.seed_n = seed_n
        self.amp_n  = amp_n if amp_n else 0.03 # noise amp in flux units


# -------- generate the intrinsic light curve at high (default) or
#          medium resolution
    def car_gen(self, seed=None, meanmag=None, mag0=None, tau=None, \
                    sigma=None, medres=None):

        """ Generate the intrinsic light curve at high (default) or 
            medium resolution """

        # utilities
        resstr = 'HIRES' if medres==None else 'MEDRES'

        print "LC_LGHTCRV: GENERATING {0} LC WITH CAR...".format(resstr)

        # reset lightcurve parameters if input
        if seed:    self.seed    = seed
        if meanmag: self.meanmag = meanmag
        if mag0:    self.mag0    = mag0
        if tau:     self.tau     = tau
        if sigma:   self.sigma   = sigma

        # generate light curve at higher res (medium or high)
        self.time, self.lc = lc_car_gen(self.seed, meanmag=self.meanmag, \
                                            mag0=self.mag0, tau=self.tau, \
                                            sigma=self.sigma, year=12., \
                                            medres=medres)

        # initialize the buffer for time delay
        self.lc_buff = self.lc[self.time < 730.]
        self.lc      = self.lc[self.time >= 730.]
        self.time    = self.time[self.time < 3650.]
        self.tdelay  = 0.0

        # reset sampled and splined curves
        self.time_samp = self.time
        self.lc_samp   = self.lc
        self.noise     = np.zeros(self.lc_samp.size)

        self.time_sp = np.zeros(self.time.size)
        self.lc_sp   = np.zeros(self.lc.size)

        # intialize the sampling parameter flags
        self.daily = self.weekly = self.season = 0
        self.usrind = np.zeros(self.time.size, dtype='byte')


# -------- sample the light curve and add a noise realization
    def sample(self, daily=None, weekly=None, season=None, index=None, \
                   amp_n=None, seed_n=None):

        """ Sample the light curve and add a noise realization """

        # sample the light curve
        self.time_samp, self.lc_samp = lc_sample(self.time, self.lc, \
                                                     daily=daily, \
                                                     weekly=weekly,\
                                                     season=season, \
                                                     index=index)

        # generate a noise realization
        if amp_n:  self.amp_n  = amp_n
        if seed_n: self.seed_n = seed_n

        self.noise = lc_noise(self.lc_samp, self.seed_n, amp_n=self.amp_n)

        # set the sampling flags appropriately
        self.daily  = 1 if daily else 0
        self.weekly = 1 if weekly else 0
        self.season = 1 if season else 0
        self.usrind = np.zeros(self.time.size, dtype='byte')

        # reset spline since it no longer applies
        self.time_sp = np.zeros(self.time.size)
        self.lc_sp   = np.zeros(self.lc.size)


# -------- generate a spline model for the sampled light curve
    def spline(self, xr=None, nx=None, wgt=None):

        """ Generate a spline model for the sampled light curve """

        # utilities
        nx = self.time.size
        xr = [self.time.min(),self.time.max()]

        # fit a spling model to the sampled light curve
        self.time_sp, self.lc_sp = lc_spline(self.time_samp, self.lc_samp + \
                                                 self.noise, xr=xr, nx=nx, \
                                                 wgt=self.noise)


# -------- add a time delay to the intrinsic light curve (successive
#          calls are possible)
    def add_tdelay(self, tdelay):

        """ Add a time delay to the intrinsic light curve (successive calls
            are possible) """

        # set the time delay
        self.tdelay = tdelay

        # add the time delay (self.lc and self.lc_buff are modified)
        lc_add_tdelay(self.time, self.lc, self.tdelay, buffer=self.lc_buff)

        # reset sampled and splined curves
        self.time_samp = self.time
        self.lc_samp   = self.lc
        self.noise     = np.zeros(self.lc_samp.size)

        self.time_sp = np.zeros(self.time.size)
        self.lc_sp   = np.zeros(self.lc.size)


# -------- write this instance to a file
    def write(self, filename, path=None, clobber=None):

        """ Write this instance to a file (evil only) """
        # write to file
        lc_write([], self, 'evil', filename, path=path, clobber=clobber)


# -------- return an item by its name
    def __getitem__(self, key):

        """ Return an item by its name. """

        data = { \
                'seed'      : self.seed, \
                'meanmag'   : self.meanmag, \
                'mag0'      : self.mag0, \
                'tau'       : self.tau, \
                'sigma'     : self.sigma, \
                'time'      : self.time, \
                'lc'        : self.lc, \
                'time_samp' : self.time_samp, \
                'lc_samp'   : self.lc_samp, \
                'noise'     : self.noise, \
                'time_sp'   : self.time_sp, \
                'lc_sp'     : self.lc_sp, \
                'daily'     : self.daily, \
                'weekly'    : self.weekly, \
                'season'    : self.season, \
                'usrind'    : self.usrind, \
                'seed_n'    : self.seed_n, \
                'amp_n'     : self.amp_n, \
                'tdelay'    : self.tdelay, \
                'lc_buff'   : self.lc_buff, \
                'dtype'     : self.dtype, \
                'names'     : self.names \
                }

        return data[key]
