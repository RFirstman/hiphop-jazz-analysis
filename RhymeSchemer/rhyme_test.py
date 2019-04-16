from rhyme_schemer import RhymeSchemer

filename = "../aquemini_3k.txt"
rs = RhymeSchemer(filename=filename, verbose=True)

#vowel = "e"
#print(set(rs.vow))
#rs.find_rhymes(vowel)
rhymes = rs.get_rhyme_schemes()
print(rhymes)

#rs.display_rhyme_schemes()
rs.print_rhyme_schemes_to_terminal()

rs.rhyme_schemes_to_html()