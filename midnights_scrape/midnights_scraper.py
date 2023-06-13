from bs4 import BeautifulSoup, NavigableString
from urllib.request import Request, urlopen
import pandas as pd

SOURCE = "https://www.lyricsondemand.com/t/taylorswiftlyrics/midnightsthetildawneditionalbumlyrics.html"
DESTINATION = "midnights.csv"

def get_lyrics(source):
    data = None
    with urlopen(Request(url=SOURCE, headers={'User-Agent': 'Mozilla/5.0'})) as fp: # open
        data_bytes = fp.read()
        data = data_bytes.decode("utf8") # decode

    soup = BeautifulSoup(data, "html.parser") # parse

    sel = soup.find("div", class_="lcontent") # select

    songs = dict()

    # album_name = []
    track_title = []
    track_n = []
    lyrics = []
    lines = []
    section = []

    curr_track_name = None
    curr_track_n = 0
    curr_line = 0
    curr_section = 0
    # is_new_track = False


    for line in sel:
        # print()
        if line.name == "a" and line.has_attr("class"): # and line["class"] == "bold":
            curr_track_n += 1
            curr_track_name = line.text
            curr_line = 0
            curr_section = 0
            # is_new_track = True
            
            
            # if current_song is not None:
            #     songs[current_song] = {'lyric':song_lines, 'line'
            # song_name = line.text
            # song_lines = []
            # song_section = []
        elif isinstance(line, NavigableString) and line.name is None:
            # print(line.name, line.text)
            # and line.name is None:
            if len(line.text) > 1:
                curr_line += 1
                # print(line.text, curr_line)
                lyrics.append(line.text.strip())
                track_title.append(curr_track_name)
                track_n.append(curr_track_n)
                lines.append(curr_line)
                section.append(curr_section)
            else:
                curr_section += 1
        # elif line.name == "br":
        #     print("br", line.text)
        
        
        # elif line.name == "br" and len(line.text) > 0:
        #     curr_line += 1
        #     track_title.append(curr_track_name)
        #     track_n.append(curr_track_n)
        #     lyric.append(line.text)
        #     line.append(curr_line)
        #     section.append(curr_section)
        # elif line.name == "br" and len(line.text) == 0:
        #     curr_section += 1

    df = pd.DataFrame({'track_title':track_title, 'track_n':track_n, 'lyric':lyrics, 'line':lines, 'section':section})

    print(df.head(20))
    return df


df.to_csv("midnights.csv", index=False)
        # if is_new_track:
        #     is_new_track = False
        #     track_n.append(track_n[-1] + 1)
        # # line += 1
        
        # tran
        
        
        
        
        
    #     print(type(line), line.string, line.text)
    # # if line.startswith("<a"): # and line.class_ == "bold":
    #     # line_bs = BeautifulSoup(line, "html.parser")
    #     print(line.text)
    #     songs[line.text] = dict()

# for title in sel.find_all(["a", "b"], class_="bold"):
#     print(title)
    
    
# soup.find_all()



