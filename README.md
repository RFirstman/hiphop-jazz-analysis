# Hip Hop/Jazz Analysis

This repository tracks my work for Georgia Tech's Robotic Musicianship VIP team for the Spring 2019 semester.
This semester, I am working to create tools for automated rhyme scheme analysis.

## Contents

~~`lyric_scraping/` contains code for a python script that collects verses from given artists using the 
[LyricsGenius](https://github.com/johnwmillr/LyricsGenius) python library~~ UPDATE: My lyric scraping tool has been moved to its own GitHub repository. You can find it [here](https://github.com/RFirstman/versescraper).

`nltk_rhyme.py` and `words_rhyme.py` are small scripts I wrote to test out two python libraries, 
[NLTK](http://www.nltk.org/) and [Jellyfish](https://github.com/jamesturk/jellyfish), respectively.

`RhymeSchemer/` contains code utilizing the [Raplyzer project](https://github.com/angelogiomateo/Raplyzer).
I utilized Raplyzer to make `rhyme_schemer.py`. This python program can generate a visual representation
of rhyme schemes to either HTML or the command line. Do note that due to limitations in the number of colors
available at the command line, I recommend using the HTML route.
Please note that the only code I personally wrote in here was `rhyme_schemer.py`. All credit for the Raplyzer code goes
to the original authors of said project.

Example usage of `rhyme_schemer.py`:
```python
from rhyme_schemer import RhymeSchemer
rs = RhymeSchemer(filename="aquemini_3k.txt")
rs.rhyme_schemes_to_html(filename="aquemini_rhyme_schemes")
```

This will generate an HTML file called "aquemini_rhyme_schemes.html".

Example output:

![Rhyme Schemer HTML output](https://github.com/RFirstman/hiphop-jazz-analysis/raw/master/resources/rhyme_scheme_html.png)

Rhyme Schemer utilizes common vowel sounds in words to detect assonant rhymes. The words are then grouped by their shared vowel
sounds and assigned a color. That is why words such as "my" and "mind" or "blend" and "again" are given the same color despite
not being perfect rhymes.

The tool is not without its issues, of course. First, the colors are picked randomly, so there is no guarantee for noticeable
differences between colors let alone accessibility for color-blind individuals. 

Second, words are naively assigned to rhyming groups such that a word is put in the first group that shares one of its vowel sounds.
Put plainly, a word may have multiple syllables, each with their own vowel sound. These syllables can each belong to distinct rhyming
groups. Ideally, colorations of words would be split up into individual syllables.

Third, this tool does not take into account the actual delivery of the verse, let alone the rhythm or stresses put on syllables.
Here, Andre 3000 uses a repeated pattern of words and vowel sounds for some of the verse. "Warps and bends", "floats the wind",
"count to ten", "meet the twin", and "Andre Ben" do not rhyme by convential standards. However, these phrases are delivered in
such a way that they _do_ end up rhyming to the listener. The shared vowel sounds between each respective word in a phrase are
not perfectly alike, but sound similar enough to pass as a rhyme. This is especially true when factoring in Andre 3000's southern
accent. The words "ten" and "twin" sound like they share the same vowel sound when listening to the verse. Lastly, a consistent
meter, or rhythmic structure, ties these phrases together to an additional degree.

In summary, Rhyme Schemer needs more accessible color schemes, categorization rhymes on the syllable level, and consideration
for lyrical rhythm and stresses to more accurately capture the true rhyme scheme of a given verse.