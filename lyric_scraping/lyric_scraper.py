import lyricsgenius
import re
import json
import os

lyricsgenius.verbose = True

def process_lyrics(lyrics, song_name, album, song_artist):
    lyric_dict = {}

    # Replace (most) unicode characters with their ASCII equivalent
    lyrics = lyrics.replace("\u200b", "").replace("\u2014", "-").replace("\u2018","'").replace("\u2019", "'")
    lyrics = lyrics.replace("\u201c", "\"").replace("\u201d", "\"")

    # Use a regular expression to fetch verses, had a few different attempts
    #out = re.findall('\[(?P<Type>.*)(?:\:\s(?P<Artist>.*)|\s(?:[1-9]))\]\n(?P<verse>[^\[]*)\s\n', lyrics)
    #out = re.findall('\[(?P<Type>.*)(?:\:\s(?P<Artist>.*)\s&(?:.*)|\s(?:[1-9]))\]\n(?P<verse>[^\[]*)\s\n', lyrics)
    out = re.findall('\[(?P<Type>.*)(?:\:\s(?P<Artist>.*)|\s(?:[1-9]))\]\n(?P<verse>[^\[]*)[$\n]?', lyrics)

    # each match will be of format (Type, Artist, Verse lyrics)
    # Type corresponds to the type of verse (e.g. "Verse", "Chorus", "Hook")
    for match in out:
        lyric_type = match[0]
        if "Verse" in lyric_type:
            # The type will either be of the form [Verse 1: Artist] or
            # something like [Verse 1]. In the latter case, we'll just used
            # the supplied artist name
            if not match[1] or (song_artist in match[1] and match[1].index(song_artist) == 1):
                artist = song_artist
            else:
                artist = match[1]
            
            # This is literally to make sure Andre 3000 isn't split into two separate entries
            # i.e. some songs have him with an accent over the "e", some do not
            artist = artist.replace("\u00e9", "e")
            
            # Get the verse and split it into an array by line
            verse = match[2]
            verse = verse.split("\n")
            verse = list(filter(None, verse)) # remove unnecessary empty strings
            if artist not in lyric_dict:
                lyric_dict[artist] = {}
            if album not in lyric_dict[artist]:
                lyric_dict[artist][album] = {}
            if song_name not in lyric_dict[artist][album]:
                lyric_dict[artist][album][song_name] = []
            
            lyric_dict[artist][album][song_name].append(verse)

    return lyric_dict

# Save everything in the lyric dictionary to a single JSON file
def save_lyrics_to_json(lyric_dict, filename="Lyrics"):
    filename = filename + ".json"

    if os.path.isfile(filename):
        while True:
            res = input("{} already exists. Overwrite?\n(y/n): ".format(filename)).lower()
            if res == 'y':
                break
            elif res == 'n':
                print("Aborting.")
                return
            else:
                print("Enter y/n")
    
    with open(filename, 'w') as lyrics_file:
        json.dump(lyric_dict, lyrics_file, indent=4)
    return

# Given two lyric dictionaries, merge them without overwriting any values
def merge_lyric_dicts(dict1, dict2):
    return_dict = dict1.copy()

    for artist, _ in dict2.items():
        if artist not in return_dict:
            return_dict[artist] = dict2[artist]
        else:
            for album in dict2[artist]:
                if album not in return_dict[artist]:
                    return_dict[artist][album] = dict2[artist][album]
                else:
                    for song, lyrics in dict2[artist][album].items():
                        if song not in return_dict[artist][album]:
                            return_dict[artist][album][song] = lyrics
    return return_dict
    
# Given a JSON file generated by `save_lyrics_to_json()`, create a file structure
# from it. The folder structure is: Artist/Album/Song.txt
# Note that the structure is compatible with Raplyzer
def save_json_to_folders(filename, prefix_folder=None):
    with open(filename) as file:
        lyric_dict = json.load(file)

    if prefix_folder:
        os.makedirs(prefix_folder, exist_ok=True)

    for artist, _ in lyric_dict.items():
        artist_dir = artist
        if prefix_folder:
            artist_dir = prefix_folder + "/" + artist

        os.makedirs(artist_dir, exist_ok=True)
        for album, _ in lyric_dict[artist].items():
            formatted_album = make_string_filename_safe(album)
            album_dir = artist_dir + "/" + formatted_album

            os.makedirs(album_dir, exist_ok=True)
            for song, _ in lyric_dict[artist][album].items():
                formatted_song = make_string_filename_safe(song)
                with open(album_dir + "/" + formatted_song + ".txt", "w") as song_file:
                    for verse in lyric_dict[artist][album][song]:
                        for line in verse:
                            song_file.write("{}\n".format(line))
                        song_file.write("\n")

    return

# Remove any non-alphanumeric characters from a string so
# it can be used as a folder/file name
def make_string_filename_safe(string):
    return "".join([c for c in string if c.isalpha() or c.isdigit() or c==' ']).rstrip()

if __name__ == "__main__":
    # Get Genius client access token from JSON
    with open("genius_access_token.json") as file:
        token_json = json.load(file)
    client_access_token = str(token_json["clientAccessToken"])
    genius = lyricsgenius.Genius(client_access_token)

    # Specify which artists to fetch lyrics for
    artists = [
        "OutKast", "Rakim", "Eric B. & Rakim", 
        "MF DOOM", "Madvillain", "Aesop Rock", 
        "Kendrick Lamar", "Denzel Curry", "JID",
        "Del the Funky Homosapien", "J Cole", "Kanye West"
    ]

    lyric_dict = {}
    for artist in artists:
        artist = genius.search_artist(artist, max_songs=10, sort="popularity")
        for song in artist.songs:

            # If a song doesn't have an album, skip it--album is needed for organizing
            # songs. TODO: potentially handle this case later
            if not song.album: 
                print("no album found for " + song.title)
                continue
            new_dict = process_lyrics(song.lyrics, song.title, song.album, artist.name)
            lyric_dict = merge_lyric_dicts(lyric_dict, new_dict)

    save_lyrics_to_json(lyric_dict, filename="total")
    save_json_to_folders("total.json", prefix_folder="lyrics")
    print("Done. All songs written to disk.")
