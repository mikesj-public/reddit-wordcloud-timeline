import string
import re

stop_words = {'im','a','able','about','across','after','all','almost','also','am','among','an','and','any','are','as','at','be','because','been','but','by','can','cannot','could','dear','did','do','does','either','else','ever','every','for','from','get','got','had','has','have','he','her','hers','him','his','how','however','i','if','in','into','is','it','its','just','least','let','like','likely','may','me','might','most','must','my','neither','no','nor','not','of','off','often','on','only','or','other','our','own','rather','said','say','says','she','should','since','so','some','than','that','the','their','them','then','there','these','they','this','tis','to','too','twas','us','wants','was','we','were','what','when','where','which','while','who','whom','why','will','with','would','yet','you','your'}
exclude = set(string.punctuation)
exclude.remove('\'')

def convert_utf(in_):
    try :
        return str(in_)
    except UnicodeEncodeError:
        return str(in_.encode('ascii', 'ignore'))   
  
url_regex = r'/^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/'
simple_url_regex = r'(http|www)\S+'

def remove_websites(text):
    simple = re.sub(simple_url_regex,' ', text)
    return simple
    #remove_brackets = simple.replace('](',' ').replace('[','').replace(')','')
    #return re.sub(url_regex,' ',remove_brackets , flags=re.MULTILINE)   

def replace_punctiation_char(ch):
    if ch in exclude:
        return '  '
    else :
        return ch
    
def remove_nan(text):
    if text == 'nan':
        return ''
    else:
        return text

def remove_punctuation(s):
    return ''.join(replace_punctiation_char(ch) for ch in s )

def remove_numbers(s):
    return re.sub("\s\d+", "", s)

def remove_repeats(s):
    return re.sub(r'(.)\1{3,}', r'\1', s)

def remove_whitespace(s):
    return ' '.join(s.split())

import sys

def scrub_text(text):
    clean1  = convert_utf(text).lower()
    no_websites = remove_websites(clean1)
    no_repeats = remove_repeats(no_websites)
    no_punct = remove_punctuation(no_repeats)
    no_numbers = remove_numbers(no_punct)    
    ret = remove_whitespace(no_numbers)
    return ret
