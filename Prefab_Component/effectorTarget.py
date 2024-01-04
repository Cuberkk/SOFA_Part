def effectorTarget(parentNode, name, showcolor, showObjectScale, position):
    target = parentNode.addChild(name)
    target.addObject('EulerImplicitSolver', firstOrder=True)
    target.addObject('CGLinearSolver', threshold='1e-09', tolerance='1e-09', iterations='200')
    target.t = target.addObject('MechanicalObject', name='dofs', 
                     position=position, 
                     showObject=True, 
                     showObjectScale=showObjectScale, 
                     drawMode=2,
                     showColor=showcolor)
    target.addObject('UncoupledConstraintCorrection')
    # print(list(t.__data__))
    
    return target 