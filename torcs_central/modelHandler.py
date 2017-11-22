import sys
import os
from inspect import getsourcefile

current_path = os.path.abspath(getsourcefile(lambda:0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
sys.path.insert(0,parent_dir)

from networks.models import ActorModel, CriticModel


class CentralModel():
	def __init__(self):
		pass