import pytest

import numpy as np
import pandas as pd


import os
import sys
sys.path.insert(0, "..")



from autogenes_effectsize import objectives as ga_objectives




perfect_sm=np.array([[100,0,0],[0,100,0],[0,0,100]])
perfect_sm_std=np.array([[100,0,0],[0,0,0],[0,0,0]])

bad_sm=np.array([[100,100,100],[0,0,0],[0,0,0]])

#bad_sm2=np.array([[100,100,100],[90,0,87],[0,45,0]])

bad_sm2=np.array([[100,0,0],[50,50,50],[9,80,7]])


def test_correlation():
	print("correlation")
	print(ga_objectives.correlation(bad_sm,perfect_sm_std))
	#print(ga_objectives.correlation(perfect_sm,perfect_sm_std))

def test_condition():
	print("condition")
	print(ga_objectives.condition(bad_sm2,perfect_sm_std))
	print(ga_objectives.condition(bad_sm2.T,perfect_sm_std))
	#print(ga_objectives.condition(perfect_sm,perfect_sm_std))

def test_distance():
	print(ga_objectives.distance(perfect_sm,perfect_sm_std))



def test_affectSize():
	#print(perfect_sm)
	#print(perfect_sm_std)
	print(ga_objectives.affectSize(perfect_sm,perfect_sm_std))
	

test_correlation()
test_condition()









