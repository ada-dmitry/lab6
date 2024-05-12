from datetime import datetime
 
def max_len(vals, index):
    tmp = -1
    for i in vals:
        tmp = max(tmp, len(i[index]))
    if index == 2:
        return max(tmp, 3)
    return max(tmp, 7)   
def check_format(val):
    format = "%Y-%m-%d"
    res = True
    try:
        res = bool(datetime.strptime(val, format))
    except ValueError:
        res = False
    return not(res)
