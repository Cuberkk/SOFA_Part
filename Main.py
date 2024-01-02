# from Gripper_V2 import Gripper_V2
from splib3.loaders import loadPointListFromFile
from stlib3.physics.constraints import FixedBox
from Prefab_Component.ElasticMaterialObject import ElasticMaterialObject
from Prefab_Component.effectorTarget import effectorTarget
from Prefab_Component.virtual_actuator import virtual_actuator
from Prefab_Component.position_effector import PositionEffector
from Prefab_Component.DataController_1_Point import DataController_1_Point
from Prefab_Component.TargetController import TargetController
from Photoneo_Main import freerun

def Gripper_V2(parentnode=None, 
               name="Gripper", 
               rotation=[0,0,0], 
               translation=[0,0,0],
               contact_point = loadPointListFromFile("Data/Contact_Point_Veri.json"),
               fixingbox_gripper_1=[-8.0,8.5,10.0,8.0,-8.5,0.0],
               effector_Position_1 = [7.3, 38.5 ,0. ],
               effector_Position_2 = [-7.3, 38.5 ,0. ],
               target_1 = [7.3, 38., -0.5],
               target_2 = [-7.3, 38., -0.5]
               ):
    
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
     
    ###Add EffectorTarget
   #  freerun()
   #  target1, target2 = freerun()
    
   #  target = effectorTarget(parentnode,
   #                           name = 'Target',
   #                           showcolor=[255., 0., 0., 255.],
   #                           showObjectScale=0.5,
   #                           position=target1
                           #   position=[7.3,37.5,-1]
                           #   )
    
                                #  position=[0.0479262918+0.0528035,27.6100006+1.59477,10-6.26488])
    
    target1 = effectorTarget(parentnode,
                             name = 'Target1', 
                             showcolor=[255., 0., 0., 255.], 
                             showObjectScale= 0.5, 
                             position=target_1)
    target2 = effectorTarget(parentnode,
                             name = 'Target2', 
                             showcolor=[0., 255., 0., 255.], 
                             showObjectScale= 0.5, 
                             position=target_2)
    
    
    ###Add PositionEffector
    pe = mechobject.addChild('Effectors')
   #  PositionEffector(parentNode= pe,
   #                   name="Position_Effector_3",
   #                   effector_Position=effector_Position,
   #                   target=target)
    
    PositionEffector(parentNode= pe,
                     name="Position_Effector_1",
                     effector_Position=effector_Position_1,
                     target=target1)
    
    PositionEffector(parentNode= pe,
                     name="Position_Effector_2",
                     effector_Position=effector_Position_2,
                     target=target2)
    
    return VF1y, VF1z

def createScene(rootNode):
    from stlib3.scene import MainHeader
    pluginList = ["Sofa.Component.IO.Mesh",
                  "Sofa.Component.LinearSolver.Iterative",
                  "Sofa.Component.Mass",
                  "Sofa.Component.MechanicalLoad",
                  "Sofa.Component.StateContainer",
                  "Sofa.Component.ODESolver.Backward",
                  "Sofa.Component.SolidMechanics.FEM.Elastic",
                  "Sofa.Component.Topology.Container.Dynamic",
                  "Sofa.Component.Visual",
                  "Sofa.GL.Component.Rendering3D",
                  "Sofa.Component.Topology.Mapping",
                  "Sofa.Component.Constraint.Projective",
                  "Sofa.Component.Mapping.Linear",
                  "Sofa.Component.Collision.Detection.Algorithm",
                  "Sofa.Component.Collision.Detection.Intersection",
                  "Sofa.Component.Collision.Geometry",
                  "Sofa.Component.Collision.Response.Contact",
                  "Sofa.Component.Topology.Container.Constant",
                  'Sofa.Component.AnimationLoop',
                  'Sofa.Component.Constraint.Lagrangian.Correction',
                  'Sofa.Component.Constraint.Lagrangian.Solver',
                  'Sofa.Component.Engine.Select',
                  'Sofa.Component.LinearSolver.Direct',
                  'Sofa.Component.SolidMechanics.Spring',
                  'SoftRobots.Inverse',
                  'SofaValidation'] 
    MainHeader(rootNode, plugins=pluginList)
    # rootNode.VisualStyle.displayFlags = "showBehavior showCollisionModels"
    rootNode.VisualStyle.displayFlags = "showInteractionForceFields showForceFields hideVisualModels"
    rootNode.addObject('FreeMotionAnimationLoop')
    rootNode.addObject('QPInverseProblemSolver', epsilon=1e-10)
    
    targetController = TargetController(name = "Target Controller",
                                        parentNode = rootNode,
                                        target1 = [7.3, 38., -0.5],
                                        target2 = [-7.3, 38., -0.5])
    
    VF1y, VF1z= Gripper_V2(parentnode=rootNode,
                           target_1 = targetController.target1,
                           target_2 = targetController.target2)
    
    
    ###DataController for 1 point
    dataController=DataController_1_Point(name = "VFO",
                                    object2 = VF1y, 
                                    object3 = VF1z,
                                    parentNode = rootNode)
    
    rootNode.addObject(dataController)
    
    return rootNode