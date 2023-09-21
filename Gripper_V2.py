# from stlib3.physics.deformable import ElasticMaterialObject
from Prefab_Component.ElasticMaterialObject import ElasticMaterialObject
from Prefab_Component.DataController_1_Point import DataController_1_Point
from splib3.loaders import loadPointListFromFile
from stlib3.physics.constraints import FixedBox
from Prefab_Component.effectorTarget import effectorTarget
from Prefab_Component.virtual_actuator import virtual_actuator
from Prefab_Component.position_effector import PositionEffector
from Prefab_Component.ForceVisual import ForceVisual

def Gripper_V2(parentnode=None, 
               name="Gripper", 
               rotation=[0,0,0], 
               translation=[0,0,0],
               contact_point = loadPointListFromFile("Data/Contact_Point_Veri.json"),
               fixingbox_gripper_1=[-8.0,0.0,5.0,8.0,-8.5,0.0],
               effector_Position_1 = [5., 35.5 ,10. ],
               effector_Position_2 = [-5., 35.5 ,10. ],
               effector_Position = [0.0479262918,27.6100006,10]):
    
    gripper = parentnode.addChild(name)
    
    mechobject = ElasticMaterialObject(gripper,
                                       name = "Mesh",
                                       volumeMeshFileName="Mesh/Gripper/GripperSoftPart.msh",
                                       poissonRatio=0.45,
                                       # youngModulus=4.4, (YoungsModulus for TPU 92A)
                                       youngModulus=110,
                                       totalMass=0.5,
                                       surfaceColor=[1.0, 2.0, 1.0, 0.5],
                                       surfaceMeshFileName="Mesh/Gripper/GripperSoftPart.obj",
                                    #    surfaceMeshFileName="Mesh/FV/Arrow.obj",
                                       rotation=rotation,
                                       translation=translation)
    
    gripper.addChild(mechobject)
    
    ##Add BoundaryCondition
    FixedBox(mechobject,
             atPositions=fixingbox_gripper_1,
             name="BoundryCondition_1",
             doVisualization=True)
    
    ###Add Cables
    act = mechobject.addChild("Vitual_Actuator")
    
    ###Contact_point 1
    p1 = act.addChild("Point")
    VF1y = virtual_actuator(parentNode=p1, 
                           name="VA_y",
                           contact_point=contact_point,
                           pullPoint=[0,-1972,10])
    
    VF1z = virtual_actuator(parentNode=p1,
                           name="VA_z",
                           contact_point=contact_point,
                           pullPoint=[0,28,-1990])
    
   #  VF1x = virtual_actuator(parentNode=p1,
   #                         name="VA_x",
   #                         contact_point=contact_point,
   #                         pullPoint=[2000,28,10])
     
    ###Add EffectorTarget
    target = effectorTarget(parentnode,
                             name = 'Target',
                             showcolor=[255., 0., 0., 255.],
                             showObjectScale=0.5,
                             position=[0.0479262918+0.0528035,27.6100006+1.59477,10-6.26488])
    
   #  target1 = effectorTarget(parentnode,
   #                           name = 'Target1', 
   #                           showcolor=[255., 0., 0., 255.], 
   #                           showObjectScale= 0.5, 
   #                           position=[5., 32.5, -2.])
   #  target2 = effectorTarget(parentnode,
   #                           name = 'Target2', 
   #                           showcolor=[0., 255., 0., 255.], 
   #                           showObjectScale= 0.5, 
   #                           position=[-5., 32.5, -2.])
    
    
    ###Add PositionEffector
    pe = mechobject.addChild('Effectors')
    PositionEffector(parentNode= pe,
                     name="Position_Effector_3",
                     effector_Position=effector_Position,
                     target=target)
    
   #  PositionEffector(parentNode= pe,
   #                   name="Position_Effector_1",
   #                   effector_Position=effector_Position_1,
   #                   target=target1)
    
   #  PositionEffector(parentNode= pe,
   #                   name="Position_Effector_2",
   #                   effector_Position=effector_Position_2,
   #                   target=target2)
    
    ###Add DataController
    # dataController=DataController(name = "VFO",
    #                                 object1 = VF1, 
    #                                 object2 = VF2, 
    #                                 object3 = VF3,
    #                                 parentNode = parentnode)
    # parentnode.addObject(dataController)
    
    ###Add Force_Visualization
    ForceVisual(parentnode)
    return VF1y, VF1z
    
    #  return VF1z
    #  return VF1x, VF1y, VF1z
    

#  , VF3x, VF3y, VF3z, VF4x, VF4y, VF4z