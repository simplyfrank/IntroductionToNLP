"""
Author: Frank Fichtenmueller
Date Started: 24/8/2017
Purpose: Load and Preprocess Textual Data to be used in downstream Analysis
"""

# Import necessary external Dependencies
import numpy as np
import re
import operator
import nltk




class TextManager(object):
    """Manages a given text corpus and applies a set of basic functions to it as a whole
    
    Current issues:
    - Creates all various helper dicts and mappings in the beginning
    """


    def __init__(self, file_loc, keep_punct=False, initialize_dicts=True, calc_stats=True):
        # Load Text Corpus
        _ = self._loadText(file_loc)
        # See if we want to keep sentence punctuation
        if keep_punct:
            self.clean_text = self.raw_text
            self.words = self._tokenize(split_on='word', keep_punct=True)
            self.sentences = self._tokenize(split_on='sentence', keep_punct=True)
            self.chars = self._tokenize(split_on='char', keep_punct=True)
        else:
            self.clean_text = self._clean_text()
            self.words = self._tokenize(split_on='word')
            self.sentences = self._tokenize(split_on='sentence')
            self.cahrs = self._tokenize(split_on='char')
        
        # Create representations of subsets of the corpus
        self.word_set = set([w.lower() for w in self.words])
        
        if initialize_dicts:
            # Generate translation dicts for ML Applications
            _ = self._wordToIdx()
            _ = self._IdxToWord()
            _ = self._cntDict()

        if calc_stats:
            self._calcStats()
             

    # Helper Functions
    def _loadText(self, file):
        """Convenience wrapper to handle multiple file inputs easily"""
        with open(file, 'r') as f:
            self.raw_text = f.read()

    def _clean_text(self, keep_punct=False):
        # Remove white spaces
        text = self.raw_text.strip()
        # Remove formating from the text
        # text = 
        if keep_punct:
            return text
        else:
            # Remove punctuation
            return text


    def _tokenize(self, split_on="word", keep_punct=False):
        """Extracts whole Sentences from a given Corpus Text"""
        
        def _tokenize_sentence():
            return [[w for w in sentence.split(' ')] for sentence in self.clean_text.split('.')]
        def _tokenize_word():
            return self.clean_text.split(' ')
        def _tokenize_char():
            return list(self.clean_text)
        
        split = {
            'sentence': _tokenize_sentence,
            'word': _tokenize_word,
            'char': _tokenize_char
        } 
        return split[split_on]()

    def _wordToIdx(self):
        """Create a idx mapping for the vocabulary set of the corpus"""
        self.idx_word = {idx:w for idx,w in enumerate(self.word_set)}
    
    def _IdxToWord(self):
        """Create a word to idx mapping for the vocabulary set of the corpus"""
        self.word_idx = {w:idx for w,idx in self.idx_word.items()}
    
    def _cntDict(self):
        """Create a count dictionary for different segments of the corpus used in statistical analysis"""
        if not self.word_set:
            self.word_set = set(self.words)
        
        self.word_cnt_dict = {}
        for w in self.word_set:
            if w in self.word_cnt_dict:
                self.word_cnt_dict[w] += 1
            else:
                self.word_cnt_dict[w] = 1
    
    def _calcStats(self):
        """Generates distributional statistics on the text at different item levels"""
        
        # Generate word based Statistics
        self.word_len_dict = {word: len(word) for word in self.words}
        self.avg_wordlen = np.mean(self.word_len_dict.values())
        self.std_wordlen = np.std(self.word_len_dict.values())
        self.min_wordlen = None
        self.max_wordlen = None

    def _calcFreqDist(self):
        """Calculates a number of frequency Distribution measures for the textcorpus"""
        
        # Create Frequency based word statistics
        self.cmn_words = [word for word,c in self.cnt_dict.items() if c > 5]
        self.rare_words = [word for word,c in self.cnt_dict.items() if c < 3]
        # Create ordered lists of words based on rareness
        self.ord_wordfreq = max(self.cnt_dict.items(), key=operator.itemgetter(1))

    # Def Statistical Measures
    def cnt_words(self):
        return len(self.words)

    def std_words(self):
        return np.std()
    
    # Use Regular Expressions to identify part of speech
    def get_capWords(self, words):
        return [w for w in words if w.istitle()]

    def get_lowWords(self, words):
        return [w for w in self.words if w.islower()]

    def get_endsWords(words, ending):
        return [w for w in self.words if w.endswith(ending)]


    # Use Regular Expressions to identify Telefon number     
    def _extract_tel(self):
        """
        Expecting a list of words, it returns the extracted numbers of telefon numbers from it.
        """
        
        # Create regular expressions
        telefon_numbers = re.findall('^[abcdefghij].+', ' '.join(words))

        return telefon_numbers

    def _extract_people(self):
        pass

    def _extract_objects(self):
        pass
    
    def _extract_dates(self):
        # Setup different re expressions
        # 12 of May 2012
        # 12-05-2012
        # 5/12/2012
        # 12/5/2012
        # 12 May 2012
        # May 12 2012
        # May 12, 2012

        num_dates = re.findall(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', self.clean_text)
        char_dates = re.findall(r'(?:\d{1,2}[\w]*,? )?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* (?:\d{1,2}[\w]*,? )?\d{2,4}', string)   
        

    def _extract_time(self):
        return re.findall(r'(\w+day\b)')

    def _extract_places(self):
        """Extract Entities likely to be Places from the text"""
        pass
    

class TwitterManager(TextManager):
    """Adds special operations to efficiently handle twitter Data"""

    # Split Datastream in individual Messages

    # Extract Hashtag mentions
    def _extract_hashtags(self, tweet):
        return [w for w in tweet if re.search('#\w+', w)]

    # Extract Callouts
    def _extract_callouts(self, tweet):
        return [w for w in tweet if re.search('^@\w+', w)]
    
    # Extract Hyperlinks
    def _extract_hyperlinks(self, tweet):
        # Either fulltext hyerplinks
        links = [w for w in tweeet if re.search('(http://.+)|(www.).+')]
        # Or bitly compressed links
        bitly_links = [w for w in tweet if re.search('bit.ly/.+', w)]

        return links.append(bitly_links)
    
a = TextManager('./text.txt')
print('Wordcount:', a.cnt_words())
print('Avg Wordlength', a.avg_wordlen())