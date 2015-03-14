# create reddit wordcloud timelines

Comment scraping - run comment scraping ipython notebook, default is to run 12 threads, one for each month of the target year, may cause performance issues on some machines.

Comment cleaning - to be run next, cleans text and maps the words into Counter objects (which are then pickled)

Wordcloud - recommend that the surprise metric is replaced (unfortunately cannot publish the author's algorithm)
