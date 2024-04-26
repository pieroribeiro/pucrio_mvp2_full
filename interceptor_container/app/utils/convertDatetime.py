from datetime import datetime

def convertDatetime(dt, isISO = True, format = '%Y-%m-%d %H:%M:%S'):
    if isISO:
        return datetime.strptime(str(dt), format).isoformat()
    else:
        return datetime.strptime(str(dt), format) 
    
def getNow():
    return datetime.now()
