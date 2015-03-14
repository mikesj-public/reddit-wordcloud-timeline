
# coding: utf-8

# In[31]:

from datetime import datetime, timedelta
from datetime import date as dt
import sys

def datespan(startDate, endDate, delta=timedelta(days=1)):
    currentDate = startDate
    while currentDate < endDate:
        yield currentDate
        currentDate += delta
        
date_span = list(datespan(dt(2014,1,1), dt(2015, 3, 1)))


# In[41]:

from bs4 import BeautifulSoup
import urllib2
import re

def get_subs_and_ids_from_url(url):
    try : 
        html_page = urllib2.urlopen(url)
        soup = BeautifulSoup(html_page)

        page_ids = set()

        for link in soup.findAll('a'):
            try:
                link_conv = link.get('href')
                if str(link_conv).startswith('http://www.reddit.com/r/'):
                    page_ids.add((link_conv.split('/')[4],link_conv.split('/')[6]))
            except UnicodeEncodeError:
                pass
            except IndexError:
                pass
            except Exception as e :
                print 'failed on url ', url, ' trying again'
                print "Error msg : ",
                print e
                return get_subs_and_ids_from_url(url)
        return page_ids
    except Exception as e:
        print 'failed on url ', url, ' trying again'
        print "Error msg : ",
        print e
        get_subs_and_ids_from_url(url)

def get_url_from_date(date):
    year = datetime.strftime(date, '%Y')
    month = datetime.strftime(date, '%B')
    day = datetime.strftime(date, '%d')
    return "http://www.redditarchive.com/?d=" + month + "+" + day + ",+" + year


# In[42]:

import praw

def get_submission_from_id(reddit_id):
    r = praw.Reddit('Comment Scraper 1.0 by u/_Daimon_ see '
                 'https://praw.readthedocs.org/en/latest/'
                 'pages/comment_parsing.html')
    return r.get_submission(submission_id=reddit_id)

def get_comments_from_submission(submission):
    #submission.replace_more_comments(limit=400, threshold=0) # optionally get more than 200 comments
    return praw.helpers.flatten_tree(submission.comments)

def get_comments_from_reddit_id(reddit_id):
    submission = get_submission_from_id(reddit_id)
    return get_comments_from_submission(submission)


# In[34]:

def convert_utf(in_):
    try :
        return str(in_)
    except UnicodeEncodeError:
        return str(in_.encode('ascii', 'ignore'))
    
def remove_breaks_and_tabs(text):
    return text.replace("\n"," ").replace("\t"," ").replace("\r"," ")

def get_comment_fields(comment, id_, subreddit):
    url_id = remove_breaks_and_tabs(convert_utf(id_))
    body = remove_breaks_and_tabs(convert_utf(comment.body))
    author = comment.author.name
    score = comment.score
    return [url_id, body, author, score, subreddit]


# In[50]:

import pandas as pd
from pandas import Series
import gc
import numpy as np
from urllib2 import HTTPError
def get_df_from_day(date):
    df_dict = {}
    column_names = ['url_id','body','author', 'score', 'subreddit']
    for name in column_names:
        df_dict[name] = []
    url = get_url_from_date(date)
    sub_id_pairs = get_subs_and_ids_from_url(url)
    for pair in sub_id_pairs:
        sub = pair[0]
        id_ = pair[1]
        try :
            comments = get_comments_from_reddit_id(id_)
        except Exception as e: 
            print 'error on id ', id_
            continue
        for comment in comments:
            try:
                c_fields = get_comment_fields(comment, id_, sub)
                for index, field in enumerate(c_fields):
                    df_dict[column_names[index]].append(field)
            except AttributeError:
                pass
            
    df = pd.DataFrame(df_dict)
    return df

def process_date(date):
    date_string = datetime.strftime(date,'%Y-%m-%d')
    print date_string
    sys.stdout.flush()
    try:
        df = get_df_from_day(date)
        df.to_csv('csvs/daily_csvs/' + date_string + '.csv', index = False, sep = '\t')
    except Exception as e:
        print 'failed on date ', date, ' trying again'
        print "Error msg : ",
        raise e
        process_date(date)


# In[36]:

import sys

args = sys.argv
# arguments should be year1,month1,date1, year2, month2, date2
#date1 = dt(int(args[1]),int(args[2]), int(args[3]))
#date2 = dt(int(args[4]),int(args[5]), int(args[6]))

#date_span = list(datespan(date1, date2))


# In[51]:

import time
from timeit import timeit

total = 0
#date_span = list(datespan(dt(2013,1,5), dt(2013,1,10)))

def process_datespan(date_span):
    for date in date_span:
        process_date(date)
    
        


# In[ ]:



