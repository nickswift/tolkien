'''
Authentication utils
'''
from numpy import matrix
import numbers, json, math

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

def validate_meta_fingerprint(fp, extant_fps):
    col_failures = 0
    tmp_fp = fp[:] 

    # Load extant_fps into matrix M -- transpose
    m_transpose = matrix(extant_fps).transpose()
    # Calculate the standard deviation of each row
    for item in m_transpose:
        row = item.tolist()[0]
        mean = sum(row)/len(row)
        # Difference from mean
        dfm = [ pow(x-mean,2) for x in row ]

        # input within ceil(2*std_dev) variation is within a statistically 
        # acceptable threshold
        std_dev = math.ceil(math.sqrt(sum(dfm)/float(mean)) * 2.0)
        compare = tmp_fp[0:1][0]
        tmp_fp = tmp_fp[1:]

        # Validate the current column of the proposed fingerprint against
        # the standard deviation of the 
        if compare < mean - std_dev or compare > mean + std_dev:
            # Bad column -- add to failure rate
            col_failures = col_failures + 1

    # Ensure < 25% failure rate
    return math.floor( col_failures/float(len(fp)) * 100 ) < 25
