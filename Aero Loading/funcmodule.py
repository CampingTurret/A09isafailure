def convert(value,unit):
    
    match unit:
        case 1:
            conversion = float(1)
        case 2:
            conversion = float(2)


    newvalue = float(value*conversion)


    return newvalue

def MAC(cr,ct):
    
    taper=ct/cr
    mac=(2/3)*cr*((1+taper+taper**2)/(1+taper))
    
    return mac

def yMAC(b,cr,ct):
    
    taper=ct/cr
    ymac=(b/6)*((1+2*taper)/(1+taper))
    
    return ymac