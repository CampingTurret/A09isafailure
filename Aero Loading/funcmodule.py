def convert(value,unit):
    
    match unit:
        case 1:
            conversion = float(1)
        case 2:
            conversion = float(2)


    newvalue = float(value*conversion)


    return newvalue