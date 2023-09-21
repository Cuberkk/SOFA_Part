def PositionEffector(parentNode,
                     name,
                     effector_Position,
                     target):

    pe = parentNode.addChild(name)
    
    pe.addObject('MechanicalObject', 
                 position=effector_Position)
    
    n = pe.addObject('PositionEffector',
                 indices=list(range(len([effector_Position]))), 
                 effectorGoal=target.dofs.getData('position').getLinkPath())
    
    pe.addObject('BarycentricMapping', mapForces=False, mapMasses=False)
    
    # print(list(n.__data__))
    # print(n.findData("indices").value)
    
    # return n.findData("indices").value


