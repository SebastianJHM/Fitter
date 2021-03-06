import scipy.integrate
import math
from scipy.optimize import fsolve, least_squares
import numpy as np

class KUMARASWAMY:
    """
    Beta distribution
    https://www.vosesoftware.com/riskwiki/Kumaraswamy4distribution.php          
    """
    def __init__(self, measurements):
        self.parameters = self.get_parameters(measurements)
        self.alpha_ = self.parameters["alpha"]
        self.beta_ = self.parameters["beta"]
        self.min_ = self.parameters["min"]
        self.max_ = self.parameters["max"]
        
    def cdf(self, x):
        """
        Cumulative distribution function
        Calculated with quadrature integration method of scipy
        """
        z = lambda x: (x - self.min_) / (self.max_ - self.min_)
        result = 1 - ( 1 - z(x)**self.alpha_) ** self.beta_
        return result
    
    def pdf(self, x):
        """
        Probability density function
        """
        z = lambda x: (x - self.min_) / (self.max_ - self.min_)
        return (self.alpha_ * self.beta_) * (z(x)**(self.alpha_-1)) * ((1-z(x)**self.alpha_)**(self.beta_-1))/ (self.max_ - self.min_)

    def get_num_parameters(self):
        """
        Number of parameters of the distribution
        """
        return len(self.parameters.keys())
    
    def parameter_restrictions(self):
        """
        Check parameters restrictions
        """
        v1 = self.alpha_ > 0
        v2 = self.beta_ > 0
        v3 = self.min_ < self.max_
        return v1 and v2 and v3
    
    def get_parameters(self, measurements):
        """
        Calculate proper parameters of the distribution from sample measurements.
        The parameters are calculated by solving the equations of the measures expected 
        for this distribution.The number of equations to consider is equal to the number 
        of parameters.
        
        Parameters
        ----------
        measurements : dict
            {"mean": *, "variance": *, "skewness": *, "kurtosis": *, "data": *}

        Returns
        -------
        parameters : dict
            {"alpha": *, "beta": *, "min": *, "max": *}
        """
        def equations(sol_i, data_mean, data_variance, data_skewness, data_kurtosis, data_median):
            ## Variables declaration
            alpha_, beta_, min_, max_ = sol_i
            
            ## Generatred moments function (not-centered)
            E = lambda r: beta_ * math.gamma(1+r/alpha_) * math.gamma(beta_) / math.gamma(1+beta_+r/alpha_)
            
            ## Parametric expected expressions
            parametric_mean = E(1) * (max_ - min_) + min_
            parametric_variance = (E(2) - E(1)**2) * (max_ - min_)**2
            parametric_skewness = (E(3) - 3*E(2)*E(1) + 2*E(1)**3) / ((E(2)-E(1)**2))**1.5
            parametric_kurtosis = (E(4) - 4 * E(1) * E(3) + 6 * E(1)**2 * E(2) - 3 * E(1)**4)/ ((E(2)-E(1)**2))**2
            parametric_median = ((1-2**(-1/beta_))**(1/alpha_)) * (max_ - min_) + min_
            
            ## System Equations
            eq1 = parametric_mean - data_mean
            eq2 = parametric_variance - data_variance
            # eq2 = parametric_median - data_median
            eq3 = parametric_skewness - data_skewness
            eq4 = parametric_kurtosis  - data_kurtosis
            
            return (eq1, eq2, eq3, eq4)
        
        # solution =  fsolve(equations, (1, 1, 1, 1), measurements)
        l = measurements.min - 3 * abs(measurements.min)
        response = least_squares(equations, (1, 1, 1, 1), bounds = ((0, 0, l, l), (np.inf, np.inf, np.inf, np.inf)), args=(measurements.mean, measurements.variance, measurements.skewness, measurements.kurtosis, measurements.median))
        solution = response.x
        parameters = {"alpha": solution[0], "beta": solution[1], "min": solution[2], "max": solution[3]}
        return parameters
    
if __name__ == '__main__':
    ## Import function to get measurements
    from measurements.measurements import MEASUREMENTS

    ## Import function to get measurements
    def get_data(direction):
        file  = open(direction,'r')
        data = [float(x.replace(",",".")) for x in file.read().splitlines()]
        return data
    
    ## Distribution class
    path = "..\\data\\data_kumaraswamy.txt"
    data = get_data(path) 
    measurements = MEASUREMENTS(data)
    distribution = KUMARASWAMY(measurements)
    
    print(distribution.get_parameters(measurements))
    print(distribution.cdf(18))
    print(distribution.pdf(18))
    