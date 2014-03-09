'''
Authentication utils
'''
import numbers, json

# Sanitize metadata string -- this should be input as a JSON string
def sanitize_passwd_meta(meta):
    # load json string
    data = json.loads(meta)
    retval = [
            item 
        if isinstance(item, numbers.Number)
        else
            None
        for index, item in enumerate(data)
    ]
    # Screen out non-numeric input
    if None in retval:
        return None
    else:
        return retval

