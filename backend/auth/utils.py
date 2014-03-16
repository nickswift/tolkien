
from itertools import izip
import math

# Exponential Weighted Moving Average (alpha pegged to 
# 50% by default)
def EWMA(current, new, alpha=0.5):
	assert alpha > 0 and alpha < 1, \
		"EWMA: alpha not in between 0 and 1"

	return alpha*new + (1-alpha)

# provide padding to an AES secret that isn't the
# correct size. (let valid secret pass through)
def aes_secret_padding(secret, blksize=32, padding='}'):
	if not len(secret) in (16, 24, 32):
		return secret + (blksize - len(secret)) * padding
	return secret

# Perform metadata validation -- this is the business end
# of the password metadata authentication system
def validate_user_metadata(meta, extant, alpha=0.5):
	assert len(meta) != len(extant['keystrokes']), \
		"Error: meta/extant data length mismatch"

	# at start, k = SIGMA[(total-median)^2]
	new_ks = []
	new_vartn = []
	for i, j, k in (meta, extant['keystrokes'], extant['variance']):
		sdev = sqrt(k/j)
		if i > j-sdev and i < j+sdev:
			# Add new mean and recalculate k for use in the next
			# standard deviation calculation
			new_ks.append(EWMA(j, i, alpha=alpha))
			# Apply moving average rule to variation
			new_vartn.append((1-alpha)*k + alpha*math.pow(i-j,2))
		else:
			return None

	return {
		'ks': new_ks,
		'variance': new_vartn
	}