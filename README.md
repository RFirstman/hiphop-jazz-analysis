# Hip Hop/Jazz Analysis

This repository tracks my work for Georgia Tech's Robotic Musicianship VIP team for the Spring 2019 semester.
This semester, I am working to create tools for automated rhyme scheme analysis.

## Contents

~~`lyric_scraping/` contains code for a python script that collects verses from given artists using the 
[LyricsGenius](https://github.com/johnwmillr/LyricsGenius) python library~~ UPDATE: My lyric scraping tool has been moved to its own GitHub repository. You can find it [here](https://github.com/RFirstman/versescraper).

`nltk_rhyme.py` and `words_rhyme.py` are small scripts I wrote to test out two python libraries, 
[NLTK](http://www.nltk.org/) and [Jellyfish](https://github.com/jamesturk/jellyfish), respectively.

`Raplyzer/` contains code utilizing the [Raplyzer project](https://github.com/angelogiomateo/Raplyzer).
I utilized Raplyzer to make `rhyme_schemer.py`. This python program can generate a visual representation
of rhyme schemes to either HTML or the command line. Do note that due to limitations in the number of colors
available at the command line, I recommend using the HTML route.
Please note that the only code I personally wrote in here was `rhyme_schemer.py`. All credit for the Raplyzer code goes
to the original authors of said code.

Example usage of `rhyme_schemer.py`:
```python
from rhyme_schemer import RhymeSchemer
rs = RhymeSchemer(filename="aquemini_3k.txt")
rs.rhyme_schemes_to_html(filename="aquemini_rhyme_schemes")
```

This will generate an HTML file called "aquemini_rhyme_schemes.html".

Example output:

![Rhyme Schemer HTML output](https://github.com/RFirstman/hiphop-jazz-analysis/raw/master/resources/rhyme_scheme_html.png)