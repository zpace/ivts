from .ivts import *

class Linear(IVTSDist):
    def __init__(self, slope, intercept, domain: Domain):
        """Linear Distribution
        
        Parameters
        ----------
        slope : {number}
            slope of linear distribution
        intercept : {number}
            intercept of linear distribution
        domain : {Domain}
            domain of evaluation
        """
        self.slope, self.intercept, self.domain = slope, intercept, domain

        a, b = tuple(domain)

        assert np.all(self.pdf(np.array(domain)) >= 0.), \
               'probability densities must be positive across domain'

        self.norm = 1. / (self.cdf_unnorm(b) - self.cdf_unnorm(a))

        super().__init__(pdf=self.pdf_norm, cdf=self.cdf_norm,
                         invcdf=self.invcdf_norm, domain=domain)

    def pdf(self, x):
        return self.intercept + self.slope * x

    def cdf_unnorm(self, x):
        return self.intercept * x + 0.5 * self.slope * x**2.

    def cdf_norm(self, x):
        return self.cdf_unnorm(x) * self.norm

    def pdf_norm(self, x):
        return self.pdf(x) * self.norm

    def invcdf_norm(self, u):
        K, slope, intercept = self.norm, self.slope, self.intercept
        sqrt = np.sqrt(K * (2. * slope * u + intercept**2. * K))
        numer = sqrt - (intercept * K)
        return numer / (slope * K)


class BoundedPowerlaw(IVTSDist):
    def __init__(self, plslope: float, domain: Domain):
        """Power-law distribution
        
        Valid for domains within (0., inf), as long as plslope < -1,
        and for a wider range in plslopes with more restrictive bounds
        
        Parameters
        ----------
        plslope : {float}
            base-10-log slope of power law
        domain : {Domain}
            domain of evaluation (default is (0, inf))
        """
        a, b = tuple(domain)

        if a <= 0.:
            raise exc.IvtsDomainError('domain lower limit must be positive')
        if ~np.isfinite(b):
            raise exc.IvtsDomainError('domain upper limit must be finite')

        self.plslope, self.domain = plslope, domain
        self.plslope1 = plslope + 1

        self.norm = 1. / (self.cdf_unnorm(b) - self.cdf_unnorm(a))

        super().__init__(pdf=self.pdf_norm, cdf=self.cdf_norm,
                         invcdf=self.invcdf_norm, domain=domain)

    def pdf(self, x):
        """un-normalized PDF
        
        Parameters
        ----------
        x : {|numpy_array|}
            number to evaluate
        
        Returns
        -------
        |numpy_array|
            probability density at supplied point(s)
        """
        return x**self.plslope

    def cdf_unnorm(self, x):
        """un-normalized CDF
        
        Parameters
        ----------
        x : {array-like}
            number to evaluate

        Returns
        -------
        array-like
            un-normalized CDF value(s)
        """
        return (x**self.plslope1) / self.plslope1

    def cdf_norm(self, x):
        """normalized CDF
        
        Parameters
        ----------
        x : {array-like}
            number to evaluate

        Returns
        -------
        array-like
            normalized CDF value(s)
        """
        return self.cdf_unnorm(x) * self.norm

    def pdf_norm(self, x):
        """normalized PDF
        
        Parameters
        ----------
        x : {|numpy_array|}
            number to evaluate
        
        Returns
        -------
        |numpy_array|
            probability density at supplied point(s)
        """
        return self.pdf(x) * self.norm

    def invcdf_norm(self, u):
        """normalized inverse-CDF
        
        allows generation of a proper sample from a unit-uniform distribution
        
        Parameters
        ----------
        u : |numpy_array|
            number on (0, 1)

        Returns
        -------
        |numpy_array|
            number on domain of distribution
        """
        plslope, plslope1 = self.plslope, self.plslope1
        a, b = self.domain[0], self.domain[1] - self.domain[0]
        norm = self.norm

        return (u * b + a)**(1. / plslope1)


class BrokenBoundedPowerlaw(IVTSDist):
    def __init__(self, plslopes: Sequence[np.float], domain: Domain):
        """Series of contiguous power-laws
        
        A set of continuous (not continuously-differentiable) power-laws
        with defined set of slopes and domains
        
        Parameters
        ----------
        plslopes : {Sequence[np.float]}
            logarithmic power-law slopes
        domain : {Domain}
            domains of power-law validity: first and last are endpoints,
            intermediates are changepoints
        """

        self.domain = domain
        self.plslopes = plslopes
        self.plslopes1 = plslopes + 1.
        self.xmin, *self.breakpoints, self.xmax = domain

        assert len(plslopes) == (len(domain) - 1), \
               'you should have one fewer power law slope than domain marker'

        valsatbreaks_left  = np.array(self.breakpoints)**plslopes[:-1]
        valsatbreaks_right = np.array(self.breakpoints)**plslopes[1:]
        ratios_at_breaks = valsatbreaks_left / valsatbreaks_right

        self.relnorm = np.cumprod(
            np.concatenate([np.ones(1), ratios_at_breaks]))

    def pdf(self, x):
        """un-normalized PDF
        
        Parameters
        ----------
        x : {|numpy_array|}
            number to evaluate
        
        Returns
        -------
        |numpy_array|
            probability density at supplied point(s)
        """
        
        condlist = [(x >= ddl) * (x < ddh)
                    for ddl, ddh in zip(self.domain[:-1], self.domain[1:])]
        funclist = [lambda x: r * x**power
                    for r, power in zip(self.relnorm, self.plslopes)]
        return np.piecewise(x, condlist, funclist)

    def cdf_unnorm(self, x):
        """un-normalized CDF
        
        Parameters
        ----------
        x : {array-like}
            number to evaluate

        Returns
        -------
        array-like
            un-normalized CDF value(s)
        """
        
        # integral of power law between 

        return 

    def cdf_norm(self, x):
        """normalized CDF
        
        Parameters
        ----------
        x : {array-like}
            number to evaluate

        Returns
        -------
        array-like
            normalized CDF value(s)
        """
        return self.cdf_unnorm(x) * self.norm

    def pdf_norm(self, x):
        """normalized PDF
        
        Parameters
        ----------
        x : {|numpy_array|}
            number to evaluate
        
        Returns
        -------
        |numpy_array|
            probability density at supplied point(s)
        """
        return self.pdf(x) * self.norm

    def invcdf_norm(self, u):
        """normalized inverse-CDF
        
        allows generation of a proper sample from a unit-uniform distribution
        
        Parameters
        ----------
        u : |numpy_array|
            number on (0, 1)

        Returns
        -------
        |numpy_array|
            number on domain of distribution
        """
        plslope, plslope1 = self.plslope, self.plslope1
        a, b = self.domain[0], self.domain[1] - self.domain[0]
        norm = self.norm

        return (u * b + a)**(1. / plslope1)
