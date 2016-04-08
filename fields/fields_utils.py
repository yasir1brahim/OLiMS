
def boolean_value_based_mapper(obj, srcName, srcValue, dstName=None, dstValueTrue=True, \
                   dstValueFalse=False, deleteSrc=True):
    if dstName == None: dstName = srcName 
    
    try:
        if getattr(obj, srcName) == srcValue:
            setattr(obj, dstName, dstValueTrue)  
        else: 
            setattr(obj, dstName, dstValueFalse)
        if srcName != dstName and deleteSrc == True: delattr(obj, srcName) 
    except AttributeError:
        setattr(obj, dstName, dstValueFalse)

def direct_mapper(obj, srcName, dstName):    
    try:
        widget = getattr(obj, 'widget')
        value_from_widget = getattr(widget, srcName)
        
        setattr(obj, dstName, value_from_widget)
    except AttributeError:
        setattr(obj, dstName, '')

     
            
        
    

