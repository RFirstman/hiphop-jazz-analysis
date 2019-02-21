# Lyric Scraper

Utilizes the Genius API and [John W. Miller's](https://www.johnwmillr.com/scraping-genius-lyrics/) [lyricsgenius](https://github.com/johnwmillr/LyricsGenius) python module to collect verses for various artists. 

This script also compiles the verses to a JSON file as well as a distributed folder structure.

To run, you'll need to [sign up](https://genius.com/api-clients) for a free Genius API account. Once you create an account,
create an API client. Now, you should be able to generate a new client access token. Generate one and copy it. Now create
a file called `genius_access_token.json` and put your access token in it like so:

```JSON
{
    "clientAccessToken": "<ACCESS-TOKEN-GOES-HERE"
}
```

You can now run `python lyric_scraper.py` to start the script. It will fetch lyrics for a handful of artists. If you want to get lyrics for different artists or want to
adjust how many songs are fetched for each artist, then examine `lyric_scraper.py`'s main function.