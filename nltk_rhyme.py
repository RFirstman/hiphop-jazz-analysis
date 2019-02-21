import sys
from datetime import datetime
import jellyfish
import nltk
nltk.download('cmudict')

def rhyme(inp, level):
    entries = nltk.corpus.cmudict.entries()
    syllables = [(word, syl) for word, syl in entries if word == inp]
    rhymes = []
    for (word, syllable) in syllables:
        rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
    return set(rhymes)

def doTheyRhyme(word1, word2, rhyme_dict=None, level=1):
    # first, we don't want to report 'glue' and 'unglue' as rhyming words
    # those kind of rhymes are LAME
    if word1.find(word2) == len(word1) - len(word2):
        return False
    if word2.find(word1) == len(word2) - len(word1): 
        return False

    if rhyme_dict is None:
        return word1 in rhyme(word2, level)

    if (word1 in rhyme_dict and word2 in rhyme_dict[word1]) \
        or (word2 in rhyme_dict and word1 in rhyme_dict[word2]):
        return True
    return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("please provide a file path and word to check rhymes for")
        exit()

    startTime = datetime.now()
    
    lyricsFile = open(sys.argv[1])
    wordToCheckRhymes = sys.argv[2]

    text = lyricsFile.read()
    words = text.replace("\n", " ").replace(",", "").replace("'", "").split(" ")
    lines = text.split("\n")
    
    all_rhymes = {}
    for word in set(words):
        # print(word)
        all_rhymes[word] = rhyme(word, 1)
    print("rhymes generated")

    wordsThatRhyme = []

    for word in words:
        if doTheyRhyme(wordToCheckRhymes, word, rhyme_dict=all_rhymes):
            wordsThatRhyme.append(word)
    print(wordsThatRhyme)
    
    print("Took: {0}".format(datetime.now()-startTime))
