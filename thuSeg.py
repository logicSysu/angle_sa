
import thulac

seger = thulac.thulac('')

# chinese segmenter
# input: stn (str)
# output: tokens (list)
def segmenter(stn):
	return seger.cut(stn)
