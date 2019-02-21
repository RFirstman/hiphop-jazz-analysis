import sys
import jellyfish

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Please provide two words as arguments.")
        exit()
    
    word1 = sys.argv[1]
    word2 = sys.argv[2]

    print(word1, word2)
    print("Edit distance: {0}".format(jellyfish.levenshtein_distance(word1, word2)))
    print("Phonetic Encodings")
    print("{0}: {1}".format(word1, jellyfish.nysiis(word1)))
    print("{0}: {1}".format(word2, jellyfish.nysiis(word2)))