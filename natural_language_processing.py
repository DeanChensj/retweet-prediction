
# coding: utf-8

# # Natural Language Processing (688 only) [35pts]
# ## Introduction
# 
# In this problem you will develop two techniques for analyzing free text documents: a bag of words approach based upon creating a TFIDF matrix, and an n-gram language model.
# 
# You'll be applying your models to the text from the Federalist Papers.  The Federalist papers were a series of essay written in 1787 and 1788 by Alexander Hamilton, James Madison, and John Jay (they were published anonymously at the time), that promoted the ratification of the U.S. Constitution.  If you're curious, you can read more about them here: https://en.wikipedia.org/wiki/The_Federalist_Papers . They are a particularly interesting data set, because although the authorship of most of the essays has been long known since around the deaths of Hamilton and Madison, there was still some question about the authorship of certain articles into the 20th century.  You'll use document vectors and language models to do this analysis for yourself.

# ## The dataset
# 
# You'll use a copy of the Federalist Papers downloaded from Project Guttenberg, available here: http://www.gutenberg.org/ebooks/18 .  Specifically, the "pg18.txt" file included with the homework is the raw text downloaded from Project Guttenberg.  To ensure that everyone starts with the exact same corpus, we are providing you the code to load and tokenize this document, as given below.

# In[1]:


import re



import collections # optional, but we found the collections.Counter object useful
import scipy.sparse as sp
import numpy as np
from scipy.sparse.linalg import norm


# ## Q2: N-gram language models [0+10+13pts]

# In this question, you will implement an n-gram model to be able to model the language used in the Federalist Papers in a more structured manner than the simple bag of words approach.  You will fill in the following class:

# In[135]:


class LanguageModel:
    def __init__(self, docs, n):
        """
        Initialize an n-gram language model.
        
        Args:
            docs: list of strings, where each string represents a space-separated
                  document
            n: integer, degree of n-gram model
        """
        self.counts = collections.defaultdict(lambda: collections.defaultdict(int))
        self.count_sums = collections.defaultdict(int)
        self.dict = set()
        self.n = n
        
        for doc in docs:
            doc = doc.split()
            self.dict |= set(doc)
            l = len(doc)
            for i in range(n-1, l):
                ngram = " ".join(doc[i-n+1:i])
                self.count_sums[ngram] += 1
                self.counts[ngram][doc[i]] += 1
            
    def perplexity(self, text, alpha=1e-3):
        """
        Evaluate perplexity of model on some text.
        
        Args:
            text: string containing space-separated words, on which to compute
            alpha: constant to use in Laplace smoothing
            
        Note: for the purposes of smoothing, the dictionary size (i.e, the D term)
        should be equal to the total number of unique words used to build the model
        _and_ in the input text to this function.
            
        Returns: perplexity
            perplexity: floating point value, perplexity of the text as evaluted
                        under the model.
        """
      
        counts = self.counts
        count_sums = self.count_sums
        n = self.n
        
        doc = text.split()
        l = len(doc)
        local_dict = set(doc).union(self.dict)
        D = len(local_dict)
         
        N = l-n+1
        
        
        sum_logP = 0
        for i in range(n-1, l):
            ngram = " ".join(doc[i-n+1:i])
            P = (counts[ngram][doc[i]] + alpha) / (count_sums[ngram] + alpha * D)
            logP = np.log(P)
            sum_logP += logP
        
        return np.exp(-sum_logP / N)

    def sample(self, k):
        """
        Generate a random sample of k words.
        
        Args:
            k: integer, indicating the number of words to sample
            
        Returns: text
            text: string of words generated from the model.
        """
        counts = self.counts
        count_sums = self.count_sums
        n = self.n
        
        ngram_list = list(count_sums.keys())
        ngram_count = np.array(list(count_sums.values())).sum()
        ngram_p = [count_sums[ngram] / ngram_count for ngram in ngram_list]
        text = np.random.choice(ngram_list, p = ngram_p).split()
        
        i = 0
        while len(text) < k:
            ngram = " ".join(text[i:i+n-1])
            if count_sums[ngram] == 0:
                text += np.random.choice(ngram_list, p=ngram_p).split()
                i += n - 1
                continue
            choices = list(counts[ngram].keys())              
            probs = [counts[ngram][choice] / count_sums[ngram] for choice in choices]
            next_term = np.random.choice(choices, p=probs)
            text.append(next_term)
            i += 1

        return ' '.join(text)
    
    


