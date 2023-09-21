def virtual_actuator(parentNode, 
                     name, 
                     contact_point,
                     pullPoint):
    
    cable = parentNode.addChild(name)
    
    cable.addObject('MechanicalObject', 
                    name='dofs', 
                    position = contact_point)
    
    VF = cable.addObject('CableActuator', template='Vec3', name=name,
                     hasPullPoint=True,
                     pullPoint = pullPoint,
                     indices=list(range(0,len(contact_point))),
                     maxDispVariation='0.01'
                    )
    
    cable.addObject('BarycentricMapping', 
                    name='mapping',  
                    mapForces=False, 
                    mapMasses=False)
    
    return VF