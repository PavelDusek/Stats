import scipy
import pandas as pd

def corr( df, alpha = 0.05 ):
	"""
	Uses dataframe df and returns 3 dataframes:
	* corr_r: Pearson's correlation coefficient.
	* corr_p: p-value for correlation coefficient
	* corr_b: if p-value survives a Bonferoni correction (using level of signitifance alpha).
	"""
	variables = df.columns #or use all
	corr_r = {}
	corr_p = {}
	corr_b = {} #survives Bonferoni

	variablesNo = len(variables)
	#not counting correlation of the variable with itself, count only half of correlations (they are symmetrical)
	Bonferoni = 2 * alpha/float((variablesNo-1)*(variablesNo-1))

	for variable in variables:
	    corr_r[variable] = []
	    corr_p[variable] = []
	    corr_b[variable] = []
	    for column in df.columns:
		if variable == column:
		    corr_r[variable].append(1)
		    corr_p[variable].append(0)
		    corr_b[variable].append( True )
		else:    
		    corrdf = df[[variable, column]].dropna(how='any')
		    r, p = scipy.stats.pearsonr(corrdf[variable], corrdf[column])
		    corr_r[variable].append(r)
		    corr_p[variable].append(p)
		    corr_b[variable].append( p < Bonferoni )
	corr_r = pd.DataFrame(corr_r, index=df.columns).sort_index()
	corr_p = pd.DataFrame(corr_p, index=df.columns).sort_index()
	corr_b = pd.DataFrame(corr_b, index=df.columns).sort_index()
	return corr_r, corr_p, corr_b
