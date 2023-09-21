from Gripper_V2 import Gripper_V2
from Prefab_Component.DataController_1_Point import DataController_1_Point

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
    
    VF1y, VF1z= Gripper_V2(rootNode)
    
    
    ###DataController for 1 point
    dataController=DataController_1_Point(name = "VFO",
                                    object2 = VF1y, 
                                    object3 = VF1z,
                                    parentNode = rootNode)
    
    rootNode.addObject(dataController)
    
    return rootNode