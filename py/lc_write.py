import numpy as np
import pyfits as fits

def lc_write(time, lcs, type, filename, errlcs=None, path=None, clobber=None, \
                 ascii=None):

    """
    NAME:
      lc_write

    PURPOSE:
      Write lightcurve instance (type=evil) or sampled lightcurves (type=good) 
      to a fits binary table.  Input lightcurves must be in AB magnitudes, 
      errors are in % of flux.

    CALLING SEQUENCE:
      lc_write(time, lcs, type, filname, path=)

    INPUTS:
      time     - time vector in days
      lcs      - either a single lightcurve instance or >= 1 lightcurves [mag]
      type     - 'evil' (write lc instance) or 'good' (write lightcurves)
      filename - name of fits file to write

    OPTIONAL INPUTS:
      errlcs - error on the input lightcurves (vector, default is 3% in flux)
      path   - path where file should be written (default is present directory)

    KEYWORDS:
      clobber - flag to overwrite existing file
      ascii   - flag to write ascii instead of fits

    OUTPUTS:

    OPTIONAL OUTPUTS:

    EXAMPLES:

    COMMENTS:

    REVISION HISTORY:
      2013/02/18 - Written by Greg Dobler (KITP/UCSB)
      2013/03/12 - Modified "good" output to AB maggies (Dobler)
      2013/04/16 - Modified to add "good" ascii file functionality (Dobler)

    ------------------------------------------------------------
    """

# -------- utilities
    out = (path if path else '') + filename



# -------- write fits file by type
    if type=='good':
        print "LC_WRITE: Writing light curves to file ", out
        print "LC_WRITE:   ...using 'good' file convention"

        # utilities
        if not isinstance(lcs, list): 
            if str(lcs.dtype)=='lightcurve':
                print "\nLC_WRITE ERROR: 'good' convention does not " + \
                "accept lightcurve instances as input."
                return
            lcs = [lcs]

        if (errlcs) and (len(lcs)!=len(errlcs)):
            print "\nLC_WRITE ERROR: # of lcs must equal # of errlcs"
            return

        nlc   = len(lcs)
        npts  = lcs[0].size
        label = ['A','B','C','D']

        # check the number of output images
        if nlc > 4:
            print "\nLC_WRITE_ERROR: number of lightcurves per system " + \
                "cannot exceed four."
            return

        # if desired (...oof) write ascii
        if ascii!=None:
            print "LC_WRITE:     ...writing ascii"

            # open file
            fout = open(out,'w')

            # write header
            fout.write("## Time Delay Challenge light curves\n")
            fout.write("##\n")
            fout.write("## [time]=days, [lc]=[err]=flux in nanomaggies\n")
            fout.write("##\n")
            fout.write("##")
            fout.write("time".rjust(11))
            for ilc in range(nlc):
                fout.write(('lc_'+label[ilc]).rjust(11))
                fout.write(('err_'+label[ilc]).rjust(11))
            fout.write("\n")
            fout.write("##")
            fout.write("-----------")
            for ilc in range(nlc): fout.write("----------------------")
            fout.write("\n")

            # write light curves and errors
            ntime = time.size

            for itime in range(ntime):
                fout.write("  ")
                fout.write("{0:11.5f}".format(time[itime]))

                for ilc in range(nlc):
                    lc_nm  = 10.**(-0.4*(lcs[ilc]-22.5)) # nanomaggies
                    err_nm = lc_nm * errlcs[ilc] # nanomaggies

                    fout.write("{0:11.5f}{1:11.5f}".format(lc_nm[itime], \
                                                             err_nm[itime]))

                fout.write("\n")

            fout.close()
            return


        # create table columns
        col = [fits.Column(name='time', format=str(npts)+'E', unit='day', \
                               array=time.reshape(1,npts))]

        for ilc in range(nlc):
            colname = 'lc_' + label[ilc]
            coldata = 10.**(-0.4*(lcs[ilc]-22.5)) # nanomaggies

            col.append(fits.Column(name=colname, format=str(npts)+'E', \
                                       unit='nanomaggies', \
                                       array=coldata.reshape(1,npts)))
        
        # create errors
        if errlcs==None: errlcs = [0.03,0.03,0.03,0.03]

        for ilc in range(nlc):
            colname = 'err_' + label[ilc]
            coldata = 10.**(-0.4*(lcs[ilc]-22.5))*errlcs[ilc] # nanomaggies

            col.append(fits.Column(name=colname, \
                                       format=str(npts)+'E', \
                                       unit='nanomaggies', \
                                       array= coldata.reshape(1,npts)))

        # create headers
        table_hdu      = fits.new_table(col)
        table_hdu.name = "TDC Challenge Light Curves"
        phdu           = fits.PrimaryHDU()
        hdulist        = fits.HDUList([phdu, table_hdu])

        # write to file
        hdulist.writeto(out, clobber=clobber)

    elif type=='evil':
        print "LC_WRITE: Writing lightcurve instance to file ", out
        print "LC_WRITE:   ...using 'evil' file convention"

        if str(lcs.dtype)!='lightcurve':
            print "LC_WRITE:   'evil' convention only accepts " + \
                "lightcurve instances as input."
            return

        # create table columns
        t1sz = lcs.time.size
        t2sz = lcs.time_samp.size
        t3sz = lcs.time_sp.size
        b1sz = lcs.lc_buff.size
        i1sz = lcs.usrind.size

        form_fl1 = str(t1sz) + 'E'
        form_fl2 = str(t2sz) + 'E'
        form_fl3 = str(t3sz) + 'E'
        form_fl4 = str(b1sz) + 'E'
        form_in1 = str(i1sz) + 'J'

        col = [ \
            fits.Column(name='seed',      format='J',      unit='none',           array=[lcs.seed]), \
            fits.Column(name='meanmag',   format='E',      unit='mag',            array=[lcs.meanmag]), \
            fits.Column(name='mag0',      format='E',      unit='mag',            array=[lcs.mag0]), \
            fits.Column(name='tau',       format='E',      unit='day',            array=[lcs.tau]), \
            fits.Column(name='sigma',     format='E',      unit='mag day^(-1/2)', array=[lcs.sigma]), \
            fits.Column(name='time',      format=form_fl1, unit='day',            array=lcs.time.reshape(1,t1sz)), \
            fits.Column(name='lc',        format=form_fl1, unit='mag',            array=lcs.lc.reshape(1,t1sz)), \
            fits.Column(name='time_samp', format=form_fl2, unit='day',            array=lcs.time_samp.reshape(1,t2sz)), \
            fits.Column(name='lc_samp',   format=form_fl2, unit='mag',            array=lcs.lc_samp.reshape(1,t2sz)), \
            fits.Column(name='noise',     format=form_fl2, unit='Delta mag',      array=lcs.noise.reshape(1,t2sz)), \
            fits.Column(name='time_sp',   format=form_fl3, unit='day',            array=lcs.time_sp.reshape(1,t3sz)), \
            fits.Column(name='lc_sp',     format=form_fl3, unit='mag',            array=lcs.lc_sp.reshape(1,t3sz)), \
            fits.Column(name='daily',     format='J',      unit='none',           array=[lcs.daily]), \
            fits.Column(name='weekly',    format='J',      unit='none',           array=[lcs.weekly]), \
            fits.Column(name='season',    format='J',      unit='none',           array=[lcs.season]), \
            fits.Column(name='usrind',    format=form_in1, unit='none',           array=lcs.usrind.reshape(1,i1sz)), \
            fits.Column(name='seed_n',    format='J',      unit='none',           array=[lcs.seed_n]), \
            fits.Column(name='amp_n',     format='E',      unit='none',           array=[lcs.amp_n]), \
            fits.Column(name='tdelay',    format='E',      unit='day',            array=[lcs.tdelay]), \
            fits.Column(name='lc_buff',   format=form_fl4, unit='mag',            array=lcs.lc_buff.reshape(1,b1sz)) \
            ]

        # create headers
        table_hdu      = fits.new_table(col)
        table_hdu.name = "TDC Challenge Light Curves"
        phdu           = fits.PrimaryHDU()
        hdulist        = fits.HDUList([phdu, table_hdu])

        # write to file
        hdulist.writeto(out, clobber=clobber)

    else:
        print "LC_WRITE: '", type, "' file convention not understood."
        print "LC_WRITE:   ...only types 'good' or 'evil' are valid."

    return
