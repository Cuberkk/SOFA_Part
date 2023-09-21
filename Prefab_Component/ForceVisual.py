import Sofa

def ForceVisual(parentNode = None, 
                name = "Force_Visualization",
                rotation = [0.,0.,0.],
                translation = [0.,28,12],
                scale = [1.,1.,1.]):
    arrow = parentNode.addChild(name)
    rt = arrow.addObject('MeshOBJLoader', 
                    name="FV", 
                    filename="Mesh/FV/Arrow.obj",
                    translation = translation)
    arrow.addObject('OglModel', 
                    name = "Force_VM",  
                    src='@FV', 
                    color = [255.0, 255.0, 255.0, 255])
    
    # print(list(rt.__data__))
    
    return rt