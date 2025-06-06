import math
import numpy as np
from scipy.stats import expon
from distributions.distribution import Distribution

class ExponentialDistribution(Distribution):
    dist_name = "exponential"
    dist_type = "continuous"

    def __init__(self, lambda_: float, seed:int =12345):
        super().__init__(seed)
        self.params = {"lambda": lambda_}


    def getParams(self):
        return self.params

        
    @classmethod
    def get_instance(cls, lambda_: float):
        if cls.instance is None:
            cls.instance = cls(lambda_)
        return cls.instance


    def get_expected_pdf(self):
        lambda_ = self.params["lambda"]
        scale = 1 / lambda_

        x = np.linspace(0, 10 / lambda_, 1000)
        pdf = expon.pdf(x, scale=scale)

        return x, pdf


    def randomFromInverseTransform(self):
        lambda_ = self.params['lambda']
        r = self.rng.random()
        x = - (1 / lambda_) * math.log(r)
        self.inverse_transform_generated_numbers.append(x)

    def randomFromRejectionMethod(self):
        lambda_ = self.params['lambda']
        x_max = -math.log(0.0001) / lambda_ 
        y_max = lambda_       

        while True:
            x = self.rng.uniform(0, x_max)
            y = self.rng.uniform(0, y_max)
            fx = lambda_ * math.exp(-lambda_ * x)
            if y <= fx:
                self.rejection_method_generated_numbers.append(x)
                break

