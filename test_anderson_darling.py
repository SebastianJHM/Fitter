import math
import utilities.ad_marsaglia as ad

def test_anderson_darling(data, distribution):
    """
    Anderson Darling test to evaluate that a sample is distributed according to a probability 
    distribution.
    
    The hypothesis that the sample is distributed following the probability distribution
    is not rejected if the test statistic is less than the critical value or equivalently
    if the p-value is less than 0.05
    
    Parameters
    ----------
    data: iterable
        data set
    distribution: class
        distribution class initialized whit parameters of distribution and methods
        cdf() and get_num_parameters()
        
    Return
    ------
    result_test_ks: dict
        1. test_statistic(float):
            sum over all data(Y) of the value ((2k-1)/N)*(ln[Fn(Y[k])]+ln[1-Fn(Y[N-k+1])]).
        2. critical_value(float):
            calculation of the Anderson Darling critical value using Marsaglia-Marsaglia function.
            whit size of sample N as parameter.
        3. p-value[0,1]:
            probability of the test statistic for the Anderson-Darling distribution
            whit size of sample N as parameter.
        4. rejected(bool):
            decision if the null hypothesis is rejected. If it is false, it can be 
            considered that the sample is distributed according to the probability 
            distribution. If it's true, no.
            
    References
    ----------
    .. [1] Marsaglia, G., & Marsaglia, J. (2004). 
           Evaluating the anderson-darling distribution. 
           Journal of Statistical Software, 9(2), 1-5.
    .. [2] Sinclair, C. D., & Spurr, B. D. (1988).
           Approximations to the distribution function of the anderson—darling test statistic.
           Journal of the American Statistical Association, 83(404), 1190-1191.
    .. [3] Lewis, P. A. (1961). 
           Distribution of the Anderson-Darling statistic. 
           The Annals of Mathematical Statistics, 1118-1124.
    """
    ## Parameters and preparations
    N = len(data)
    data.sort()
    
    ## Calculation S
    S = 0
    for k in range(N):
        c1 = math.log(distribution.cdf(data[k]))
        c2 = math.log(1-distribution.cdf(data[N-k-1]))
        c3 = (2*(k+1)-1)/N
        S += c3 * (c1 + c2)
    
    ## Calculation of indicators
    A2 = -N-S
    critical_value = ad.ad_critical_value(0.95, N)
    p_value = ad.ad_p_value(N, A2)
    rejected = A2 >= critical_value
    
    ## Construction of answer
    result_test_ad = {
        "test_statistic": A2, 
        "critical_value": critical_value,
        "p-value": p_value,
        "rejected": rejected
        }
    
    return result_test_ad

if __name__ == "__main__":
    from utilities.data_measurements import get_measurements
    from distributions.beta import BETA
    from distributions.burr import BURR
    from distributions.cauchy import CAUCHY
    from distributions.chi_square import CHI_SQUARE
    from distributions.dagum import DAGUM
    from distributions.erlang import ERLANG
    from distributions.error_function import ERROR_FUNCTION
    from distributions.exponencial import EXPONENCIAL
    from distributions.f import F
    from distributions.fatigue_life import FATIGUE_LIFE
    from distributions.frechet import FRECHET
    from distributions.gamma import GAMMA
    from distributions.generalized_normal import GENERALIZED_NORMAL
    from distributions.johnson_SB import JOHNSON_SB
    from distributions.johnson_SU import JOHNSON_SU
    from distributions.lognormal import LOGNORMAL
    from distributions.normal import NORMAL
    from distributions.triangular import TRIANGULAR
    from distributions.uniform import UNIFORM
    from distributions.weibull import WEIBULL
    
    
    def getData(direction):
        file  = open(direction,'r')
        data = [float(x.replace(",",".")) for x in file.read().splitlines()]
        return data
    
    _all_distributions = [BETA, BURR, CAUCHY, CHI_SQUARE, DAGUM, ERLANG, ERROR_FUNCTION, EXPONENCIAL, F, FATIGUE_LIFE, FRECHET, GAMMA, GENERALIZED_NORMAL, JOHNSON_SB, JOHNSON_SU, LOGNORMAL, NORMAL, TRIANGULAR, UNIFORM,  WEIBULL]
    
    for distribution_class in _all_distributions:
        print(distribution_class.__name__)
        path = "C:\\Users\\USUARIO1\\Desktop\\Fitter\\data\\data_" + distribution_class.__name__.lower() + ".txt"
        data = getData(path)
                
        measurements = get_measurements(data)
        distribution = distribution_class(measurements)
                
        print(test_anderson_darling(data, distribution))