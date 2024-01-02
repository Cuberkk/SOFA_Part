import math
import Sofa.Core
import Sofa.constants.Key as Key

class TargetController(Sofa.Core.Controller):
    def __init__(self, *args, **kwargs):
        Sofa.Core.Controller.__init__(self, args, kwargs)
        self.name = kwargs['name']
        self.node = kwargs['parentNode']
        self.target1 = kwargs['target1']
        self.target2 = kwargs['target2']
        
    def onKeypressedEvent(self,event):
        if event['key'] == 'L':
            self.targetcontrol()
        return
        
    def targetcontrol(self):
        self.target1[0] += 1
        self.target2[0] += 1