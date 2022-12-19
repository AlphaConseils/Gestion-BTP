to_19_fr = (u'zéro', 'UN', 'DEUX', 'TROIS', 'QUATRE', 'CINQ', 'SIX',
			'SEPT', 'HUIT', 'NEUF', 'DIX', 'ONZE', 'DOUZE', 'TREIZE',
			'QUATORZE', 'QUINZE', 'SEIZE', 'DIX SEPT', 'DIX HUIT', 'DIX NEUF')
tens_fr = ('VINGT', 'TRENTE', 'QUARANTE', 'CINQUANTE', 'SOIXANTE', 'SOIXANTE DIX', 'QUATRE VINGT', 'QUATRE VINGT DIX')
denom_fr = ('',
			'MILLE', 'MILLIONS', 'MILLIARDS', 'BILLIONS', 'QUADRILLIONS',
			'QUINTILLION', 'SEXTILLTION', 'SEPTILLION', 'OCTILLION', 'NONILLION',
			'DECILLION', 'UNDECILLION', 'DUODECILLION', 'TREDECILLION', 'QUATTUORDECILLION',
			'SEXDECILLION', 'SEPTENDECILLION', 'OCTODECILLION', 'ICOSILLION', 'VIGINTILLION')


def _convert_nn_fr(val):
	""" convert a value < 100 to French
    """
	if val < 20:
		return to_19_fr[val]
	for (dcap, dval) in ((k, 20 + (10 * v)) for (v, k) in enumerate(tens_fr)):
		if dval + 10 > val:
			if val % 10:
				return dcap + '-' + to_19_fr[val % 10]
			return dcap


def _convert_nnn_fr(val):
	""" convert a value < 1000 to french

        special cased because it is the level that kicks
        off the < 100 special case.  The rest are more general.  This also allows you to
        get strings in the form of 'forty-five hundred' if called directly.
    """
	word = ''
	(mod, rem) = (val % 100, val // 100)
	if rem > 0:
		word = to_19_fr[rem] + ' CENT'
		if mod > 0:
			word += ' '
	if mod > 0:
		word += _convert_nn_fr(mod)
	return word


def french_number(val):
	if val < 100:
		return _convert_nn_fr(val)
	if val < 1000:
		return _convert_nnn_fr(val)
	for (didx, dval) in ((v - 1, 1000 ** v) for v in range(len(denom_fr))):
		if dval > val:
			mod = 1000 ** didx
			l = val // mod
			r = val - (l * mod)
			ret = _convert_nnn_fr(l) + ' ' + denom_fr[didx]
			if r > 0:
				ret = ret + ' ' + french_number(r)
			return ret


def amount_to_text_fr(number, currency):
	number = '%.2f' % number
	units_name = currency.upper()
	list = str(number).split('.')
	start_word = french_number(abs(int(list[0])))
	end_word = french_number(int(list[1]))
	cents_number = int(list[1])
	cents_name = (cents_number > 1) and ' CENTS' or ' CENT'
	if end_word == "zéro":
		end_word = ''
	final_result = start_word + ' ' + units_name + ' ' + end_word
	if final_result.startswith('UN') and int(float(number)) < 1000000:
		return final_result.split('UN')[1]
	return final_result
