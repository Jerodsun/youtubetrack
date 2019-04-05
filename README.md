## QuickStart: 

### Dependencies:
vaderSentiment  
googleapiclient     

good to have:  
pandas  
congress  

#### pip install vaderSentiment python-congress google-api-python-client

https://github.com/cjhutto/vaderSentiment
https://developers.google.com/api-client-library/python/
https://github.com/eyeseast/propublica-congress
Obtain a developer key for Youtube via the instructions here:
https://developers.google.com/youtube/v3/getting-started

#### Open secrets.py and replace the developer key.

#### Sample Usage:
trump = score_pull("Donald Trump")
for video in trump:
    print(video["title"])

## Purpose: 

### To collect data from youtube and analyze any political trends in Youtube's search algorithms.

Sources of error/leniency:
For some politicians, a common name unfortunately means that they are superceded by another person - perhaps a famous athlete or comedian. Some politicans also go by different names and *may* be referred to by two at a relatively similar frequency. 

It is recommended to consider the typical search for a candidate - ex. Mitch McConnell instead of Addison Mitchell McConnell, Chuck Schumer instead of Charles Ellis Schumer.
    
#### 4 high profile examples:
    Ted Cruz, Beto O'Rourke
    Diane Feinstein, Mitch McConnell
    
#### 4 medium profile examples:
    Rob Portman, Tina Smith
    Marsha Blackburn, Ro Khanna
    
#### 4 low profile examples:
    Roger Williams, Ron Wright
    Scott Peters, Maria Cantwell


Optional: obtain a ProPublica api key to get an updated list of current house/senate members.

Sample usage:

### Main function: score_pull
Downloads a list of youtube videos in a conviniently packaged bundle of dictionaries each consisting of:
  
videoid, title, description, channel, link, date, thumbnail.

Includes VaderSentiment scores of description_rating and title_rating.

Prints channels that are not recorded but in the top search results, and prints a weighted score based on VaderSentiment scores of vanilla sentiment as a reference.

*Note that VaderSentiment is not optimized for this purpose.

## Files:

### Main.py:
Where score_pull resides.

### Secrets.py:
__put your API key here!__

### Descriptions.txt
Some ideas for analyzing data for political effect.

### Sample Usage:
    import pytz
    import pandas as pd
    import datetime as dt

    senators = f.pickleimport("Senate_list.p")
    from popular import D_candidates #prominent Democrats
    alldates = []
    bundlelist = []

    for name in D_candidates:
        bundle = score_pull(name)
        dates = [i['date'] for i in bundle]
        alldates.extend(dates)
        bundlelist.append(bundle)
    
    cutoff = pytz.timezone("UTC").localize(dt.datetime(2019, 3, 1))
    recent = [k for k in alldates if k > cutoff]

    df = pd.DataFrame(recent, columns = ["date"])
    
    df.groupby(df["date"].dt.date).count().plot(kind="bar")

![alt text](Supporting/sample1.png?raw=true "Sample1")


### Another example:

    Trump = score_pull("Donald Trump", 50)
    df = pd.DataFrame(Trump, columns = ["title", "date", "link", "channel"])
    channel_frequency = df["channel"].value_counts()
    
    #analyze change over time...
    
