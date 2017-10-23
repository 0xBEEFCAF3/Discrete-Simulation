# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 00:24:20 2017

@author: Armin
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 17:18:59 2017

@author: Armin
"""
import random
import math
import numpy as np


class randVar:
    def __init__(self, lmbda):
        self.lmbda = lmbda
    
    
    def exp(self):
        rand = random.uniform(0,1) 
        
        return (-1.0/self.lmbda) * math.log(1-rand)
    


#rv = randVar(4, 1000)
#rv.plot()
#rv.plot_empirical_CDF()