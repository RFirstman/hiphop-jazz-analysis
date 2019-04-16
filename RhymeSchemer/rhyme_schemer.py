from random import choice, randrange, randint
from colorama import init, Fore, Back

from lyrics import Lyrics
import phonetics as ph

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class RhymeSchemer(Lyrics):
    def __init__(self, filename=None, print_stats=False, text=None, language='en-us', lookback=10, verbose=False):

        super().__init__(filename, print_stats, text, language, lookback)
        self.rhymes = []
        self.words_orig = [word.replace(".", "") for line in self.lines_orig for word in line.split()]
        self.espeak_words = [word for line in self.text.split("\n") for word in line.split()]
        self.vowels = set(self.vow)
        self.verbose = verbose
                        
    def find_rhymes(self, vowel):
        rhyming_vowel_idxs = [self.vow_idxs[i] for i in range(len(self.vow_idxs)) if self.vow[i] == vowel]
        rhyming_words = []
        rhyming_word_indices = []
        for vow_idx in rhyming_vowel_idxs:
            start = end = vow_idx
            while not ph.is_space(self.text[start]):
                start -= 1
            while not ph.is_space(self.text[end]):
                end += 1
            
            word = self.text[start: end+1].strip()
            #rhyming_word_indices.append(self.espeak_words.index(word))
            rhyming_words.append(self.words_orig[self.espeak_words.index(word)])
        #print(rhyming_word_indices)
        #rhyming_word = [word for i, word in enumerate(self.words_orig) if i in rhyming_word_indices]
        #print(rhyming_vowel_idxs)
        return rhyming_words
    
    def get_rhyme_schemes(self):
        rhymes = {}
        for vowel in self.vowels:
            rhymes_for_vowel = self.find_rhymes(vowel)
            rhymes[vowel] = rhymes_for_vowel
            if self.verbose:
                print("Rhymes for vowel: {}\n".format(vowel))
                print(rhymes_for_vowel)
                print()
        return rhymes
            
    def print_rhyme_schemes_to_terminal(self):
        colors = []
        vowels = list(self.vowels)

        word_to_vowel = {}
        rhyme_schemes = self.get_rhyme_schemes()
        i = 31
        for vowel, rhymes in rhyme_schemes.items():
            if i == 37: 
                i = 38
            if i == 39:
                i = 41
            colors.append(i)
            i += 1
            for word in rhymes:
                word_to_vowel[word] = vowel

        for line in self.lines_orig:
            #print(bcolors.OKGREEN + line + bcolors.ENDC)
            line_string = ""
            for word in line.split():
                if word in word_to_vowel:
                    vowel = word_to_vowel[word]
                    #highlight_color = highlight_colors[vowels.index(vowel) % len(highlight_colors)]
                    #print(word, colors[vowels.index(vowel)])
                    line_string += '\033[{0}m {1} \033[m'.format(colors[vowels.index(vowel)], word)
                else:
                    line_string += word + " "
            print(line_string)

    def rhyme_schemes_to_html(self, filename="rhymes"):
        rhyme_schemes = self.get_rhyme_schemes()
        word_to_vowel = {}
        vowel_to_color = {}
        for vowel, rhymes in rhyme_schemes.items():
            for word in rhymes:
                if word not in word_to_vowel:
                    word_to_vowel[word] = vowel
                if vowel not in vowel_to_color:
                    vowel_to_color[vowel] = self.generate_random_hex_color()
        
        html_string = self.generate_html_header()
        for line in self.lines_orig:
            line_string = "<div>"
            for word in line.split():
                if word in word_to_vowel:
                    vowel = word_to_vowel[word]
                    line_string += "<span style='color: {0}'>{1}</span> ".format(vowel_to_color[vowel], word)
                else:
                    line_string += word + " "
            line_string += "</div>\n"
            html_string += line_string
        html_string += self.generate_html_footer()
        
        with open("{}.html".format(filename), "w") as html_file:
            html_file.write(html_string)
        return

    def generate_html_header(self):
        return """<html>\n<head>\n<title>Rhymes for {0}</title>\n</head>\n<body>""".format(self.filename)
    
    def generate_html_footer(self):
        return """</body>\n</html>"""

    def generate_random_hex_color(self):
        rand_hex_value = lambda: randint(0, 255)
        return "#{:02X}{:02X}{:02X}".format(rand_hex_value(), rand_hex_value(), rand_hex_value())