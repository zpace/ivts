# encoding: utf-8
#
# @Author: Zach Pace
# @Date: Nov 11, 2019
# @Filename: ivts.py
# @License: BSD 3-Clause
# @Copyright: Zach Pace

from typing import Sequence, Callable
import numpy as np

from .core import exceptions as exc

Domain = Sequence[np.float]

class IVTSDist(object):
    def __init__(self, pdf: Callable, cdf: Callable, invcdf: Callable, domain: Domain):
        """Inverse-transform sampling class
        
        Accomplishes basic logic of inverse-transform-sampling PDFs
        
        Parameters
        ----------
        pdf : {Callable}
            probability density function
        cdf : {Callable}
            Cumulative distribution function
        invcdf : {Callable}
            inverse of cumulative distribution function
        domain : {Domain}
            domain of evaluation
        """
        assert len(domain) == 2, 'domain must be length-2'

        self._pdf = pdf
        self._cdf = cdf
        self._invcdf = invcdf
        self.domain = domain



    def rvs(self, *size: Sequence):
        """sample from PDF
        
        Parameters
        ----------
        *size : {Sequence}
            number of samples to be made
        
        Returns
        -------
        |numpy_array|
            array of samples
        """
        return self._invcdf(np.random.rand(*size))

