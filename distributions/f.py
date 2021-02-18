import scipy.stats

class F:
    """
    F distribution
    https://en.wikipedia.org/wiki/F-distribution
    """
    def __init__(self, measurements):
        self.parameters = self.get_parameters(measurements)
        self.df1 = self.parameters["df1"]
        self.df2 = self.parameters["df2"]
        
    def cdf(self, x):
        """
        Cumulative distribution function.
        Calculated with quadrature integration method of scipy.
        """
        return scipy.stats.f.cdf(x, self.df1, self.df2)
    
    def pdf(self, x):
        """
        Probability density function
        """
        return scipy.stats.f.pdf(x, self.df1, self.df2)
    
    def get_num_parameters(self):
        """
        Number of parameters of the distribution
        """
        return len(self.parameters.keys())
    
    def get_parameters(self, measurements):
        """
        Calculate proper parameters of the distribution from sample measurements.
        The parameters are calculated by formula.
        
        Parameters
        ----------
        measurements : dict
            {"mean": *, "variance": *, "skewness": *, "kurtosis": *, "data": *}

        Returns
        -------
        parameters : dict
            {"df1": *, "df2": *}
        """
        ## Scipy parameters of distribution
        scipy_params = scipy.stats.f.fit(measurements["data"])
       
        ## Results
        parameters = {"df1": scipy_params[0], "df2": scipy_params[1]}

        return parameters