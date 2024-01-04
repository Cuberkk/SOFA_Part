import math
import Sofa.Core
import Sofa.constants.Key as Key
from Prefab_Component.effectorTarget import effectorTarget

class TargetController(Sofa.Core.Controller):
    def __init__(self, *args, **kwargs):
        Sofa.Core.Controller.__init__(self, args, kwargs)
        self.name = kwargs['name']
        self.node = kwargs['parentNode']
        self.target_1 = kwargs['target1']
        self.target_2 = kwargs['target2']
        
    def onEvent(self,event):
        self.target_1 = [7.3, 38., -0.5]
        self.target_2 = [-7.3, 38., -0.5]
        print("Current value of target_1:", self.target_1)