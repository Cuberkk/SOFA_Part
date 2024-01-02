import math
import Sofa.Core
import Sofa.constants.Key as Key

class DataController_1_Point(Sofa.Core.Controller):
    def __init__(self, *args, **kwargs):
        Sofa.Core.Controller.__init__(self, args, kwargs)
        self.name = kwargs['name']
        self.node = kwargs['parentNode']
        # self.object1 = kwargs['object1']
        self.object2 = kwargs['object2']
        self.object3 = kwargs['object3']
        
    def onAnimateEndEvent(self,event):
        # print(f'V1x: {round(self.object1.findData("force").value,5)},V1y: {round(self.object2.findData("force").value,5)},V1z:{round(self.object3.findData("force").value,5)}')
        # print(f'V1z:{round(self.object3.findData("force").value,5)}')
        # print(f'Total_force:{round(math.sqrt(pow(self.object1.findData("force").value,2)+pow(self.object2.findData("force").value,2)+pow(self.object3.findData("force").value,2)),5)}')
        print(f'Total_force:{round(math.sqrt(pow(self.object2.findData("force").value,2)+pow(self.object3.findData("force").value,2)),5)}')

