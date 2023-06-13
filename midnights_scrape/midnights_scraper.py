from bs4 import BeautifulSoup, NavigableString
from urllib.request import Request, urlopen
import pandas as pd
import re

SOURCE = ["https://www.lyricsondemand.com/t/taylorswiftlyrics/midnightsthetildawneditionalbumlyrics.html",
          "https://www.lyricsondemand.com/t/taylorswiftlyrics/fearlesstaylorsversionalbumlyrics.html",
          "https://www.lyricsondemand.com/t/taylorswiftlyrics/youallovermetaylorsversionfromthevaultlyrics.html",
          "https://www.lyricsondemand.com/t/taylorswiftlyrics/mrperfectlyfinetaylorsversionfromthevaultlyrics.html",
          "https://www.lyricsondemand.com/t/taylorswiftlyrics/wewerehappytaylorsversionfromthevaultlyrics.html",
          "https://www.lyricsondemand.com/t/taylorswiftlyrics/thatswhentaylorsversionfromthevaultlyrics.html",
          "https://www.lyricsondemand.com/t/taylorswiftlyrics/dontyoutaylorsversionfromthevaultlyrics.html",
          "https://www.lyricsondemand.com/t/taylorswiftlyrics/byebyebabytaylorsversionfromthevaultlyrics.html",
          "https://www.lyricsondemand.com/t/taylorswiftlyrics/redtaylorsversionalbumlyrics.html"]
ALBUMS = ["Midnights", "Fearless", "Fearless", "Fearless", "Fearless", "Fearless", "Fearless", "Fearless", "Red"]
DESTINATION = "../data/midnights_fearless_red_2.csv"

def get_lyrics(source, album_name=None, starting_track=0):
    data = None
    with urlopen(Request(url=source, headers={'User-Agent': 'Mozilla/5.0'})) as fp: # open
        data_bytes = fp.read()
        data = data_bytes.decode("utf8") # decode

    soup = BeautifulSoup(data, "html.parser") # parse
    
    try:
        possible_track_name = soup.find("div", id="ldata")
        possible_track_name = possible_track_name.find("a", class_="SngLnk")
        possible_track_name = re.findall(r"(.+) Lyrics", possible_track_name.text)[0]
        print(possible_track_name)
    except:
        possible_track_name = None
        # print("None")
        
    sel = soup.find("div", class_="lcontent") # select

    track_title = []
    track_n = []
    lyrics = []
    lines = []
    section = []

    # curr_track_name = None if possible_track_name is None else possible_track_name.text
    curr_track_name = possible_track_name
    curr_track_n = starting_track
    curr_line = 0
    curr_section = 0

    for line in sel:
        # print()
        if line.name == "a" and line.has_attr("class"): # and line["class"] == "bold":
            curr_track_n += 1
            curr_track_name = line.text
            curr_line = 0
            curr_section = 0
        elif isinstance(line, NavigableString) and line.name is None:
            if len(line.text) > 1:
                if curr_track_n == starting_track: # If track name comes from "possible_track_name", need to increment track number
                    # print(curr_track_n, starting_track, curr_track_name, line.text)
                    curr_track_n += 1
                
                curr_line += 1
                # print(line.text, curr_line)
                lyrics.append(line.text.strip())
                track_title.append(curr_track_name)
                track_n.append(curr_track_n)
                lines.append(curr_line)
                section.append(curr_section)
            else:
                curr_section += 1

    df = pd.DataFrame({'track_title':track_title, 'track_n':track_n, 'lyric':lyrics, 'line':lines, 'section':section})
    df['album_name'] = album_name
    return df

if __name__ == "__main__":
    
    df_all = pd.DataFrame()
    previous_track_n = 0
    previous_album_name = None
    for source, album in zip(SOURCE, ALBUMS):
        if previous_album_name != album:
            previous_track_n = 0
        
        print(source, album)
        df = get_lyrics(source, album, previous_track_n)
        df_all = pd.concat([df_all, df], ignore_index=True)
        
        previous_track_n = df['track_n'].max()
        print(previous_track_n)
        previous_album_name = album
    print(df_all.head(20))
    print(df_all.tail(20))

    df_all.to_csv(DESTINATION, index=False)
