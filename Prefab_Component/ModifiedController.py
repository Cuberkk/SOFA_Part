import math
import Sofa
import Sofa.Core
import Sofa.constants.Key as Key
import numpy as np

class Controller(Sofa.Core.Controller):
    def __init__(self, *args, **kwargs):
        Sofa.Core.Controller.__init__(self, args, kwargs)
        self.name = kwargs['name']
        self.node = kwargs['parentNode']
        # self.object1 = kwargs['object1']
        self.object_Y = kwargs['object_Y']
        self.object_Z = kwargs['object_Z']
        self.target1 = kwargs['target_1']
        self.target2 = kwargs['target_2']
        
    def update_target1_position(self, target1, target2):
        self.target1.t.findData("position").value = target1
        self.target2.t.findData("position").value = target2
        
    # def onAnimateBeginEvent(self,event):
    #     print(type(self.target1.t.findData("traslation")))
    #     low = -20
    #     high = 20
    #     shape = (1,3)
    #     random_array = np.random.uniform(low, high, shape)
    #     # print(random_array)
    #     self.target1.t.findData("position").value = random_array
    #     # print(self.target1.t.findData("traslation").value)
        
    def onAnimateEndEvent(self,event):
        print(f'Total_force:{round(math.sqrt(pow(self.object_Y.findData("force").value,2)+pow(self.object_Z.findData("force").value,2)),5)}')

