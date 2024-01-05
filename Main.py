# from Gripper_V2 import Gripper_V2
import Sofa.Core
from splib3.loaders import loadPointListFromFile
from stlib3.physics.constraints import FixedBox
from Prefab_Component.ElasticMaterialObject import ElasticMaterialObject
from Prefab_Component.effectorTarget import effectorTarget
from Prefab_Component.virtual_actuator import virtual_actuator
from Prefab_Component.position_effector import PositionEffector
from Prefab_Component.ModifiedController import Controller
from Photoneo_Main import freerun
import socket
import json
import threading
import numpy as np

def receive_data(server_socket, controller):
   while True:
       try:
           connection, address = server_socket.accept()
           print(f"Receive the conncetion from {address}")
           
           while True:
               try:
                   data = connection.recv(1024)
                   if not data:
                       break
                   data_arr = json.loads(data.decode())
                   target1 = np.array(data_arr[0][0]).reshape(1,3)
                   target2 = np.array(data_arr[1][0]).reshape(1,3)
                   print("Target1:", target1, "Target2:", target2)
                   controller.update_target1_position(target1,target2)
                   
               except Exception as e:
                   print(f"Error: {e}")
                   break
       except socket.timeout:
           print("Server shutdown due to timeout")
           break
       finally:
           connection.close()
           
   server_socket.close()
   print("Server Stopped")
       

def Receive_Data():
   server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   server_socket.bind(('localhost', 12345))
   server_socket.listen()
   print("Server Starts, Waiting for connection")

   while True:
      connection, address = server_socket.accept()
      print(f"Receive the connection from {address}")
      
      try:
            while True:
                data = connection.recv(1024)
                if not data:
                    # If there is no data recieved, break
                    break
                print("Received data:", data.decode())
      except Exception as e:
         print(f"Error: {e}")

   
def Gripper_V2(parentnode=None, 
               name="Gripper", 
               rotation=[0,0,0], 
               translation=[0,0,0],
               contact_point = loadPointListFromFile("Data/Contact_Point_Veri.json"),
               fixingbox_gripper_1=[-8.0,8.5,10.0,8.0,-8.5,0.0],
               effector_Position_1 = [-7.3, 38.5 ,9.6],
               effector_Position_2 = [7.3, 38.5 ,9.6],
               target1 = None,
               target2 = None):
    
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
    
    ###Contact_point
    p1 = act.addChild("Point")
    gripper.VF1y = virtual_actuator(parentNode=p1, 
                           name="VA_y",
                           contact_point=contact_point,
                           pullPoint=[0,-1973,0])
    
    gripper.VF1z = virtual_actuator(parentNode=p1,
                           name="VA_z",
                           contact_point=contact_point,
                           pullPoint=[0,27,2000])
    
    ###Add PositionEffector
    pe = mechobject.addChild('Effectors')
    PositionEffector(parentNode= pe,
                     name="Position_Effector_1",
                     effector_Position=effector_Position_1,
                     target=target1)
    
    PositionEffector(parentNode= pe,
                     name="Position_Effector_2",
                     effector_Position=effector_Position_2,
                     target=target2)
    
    return gripper

def createScene(rootNode):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen()
    server_socket.settimeout(60) #Set 60s timeout
    print("Server Starts, Waiting for connection")
    
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
    
    target1 = effectorTarget(rootNode,
                             name = 'Target1', 
                             showcolor=[255., 0., 0., 255.], 
                             showObjectScale= 0.5,
                             position = [-7.3, 38.5 ,9.6])
    target2 = effectorTarget(rootNode,
                             name = 'Target2', 
                             showcolor = [255., 0., 0., 255.], 
                             showObjectScale= 0.5, 
                             position = [7.3, 38.5 ,9.6])
    
    print(type(target1.t.findData("traslation")))
   #  print(list(target1.t.__data__))
   #  print(target1.t.findData("position").value)
    
    gripper = Gripper_V2(parentnode=rootNode, 
                         target1 = target1,
                         target2 = target2)
    
    
    #Controller
    dataController=Controller(parentNode = rootNode,
                                          name = "VFO",
                                          object_Y = gripper.VF1y, 
                                          object_Z = gripper.VF1z,
                                          target_1 = target1,
                                          target_2 = target2)
    
    rootNode.addObject(dataController)
    
    data_thread = threading.Thread(target = receive_data,
                                   args = (server_socket, dataController))
    data_thread.start()
    
    
    return rootNode
 
if __name__ == "__main__":
   createScene()