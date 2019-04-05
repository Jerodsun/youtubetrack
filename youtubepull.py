"""
Main functions to pull data from youtube.

Reference:
https://github.com/youtube/api-samples/tree/master/python

Note that rate limits means that a key can process around 59 search queries per day for 50 search results each.

https://developers.google.com/youtube/v3/determine_quota_cost
"""

from googleapiclient.discovery import build
from secrets import developer_key_google
import dateutil.parser

youtube_api_service_name = 'youtube'
youtube_api_version = 'v3'

youtube = build(youtube_api_service_name, youtube_api_version, developerKey=developer_key_google)


def _full_description(video_ids):
    """Submethod to get full video description, as standard search only returns a snippet of the video description."""
    videos = youtube.videos().list(id=video_ids,part='id,snippet', maxResults=50).execute()
    descriptions =  [vid['snippet']['description'] for vid in videos.get('items', [])]
    
    return descriptions

def theworks(query, maxResults = 20):
    """Get the following: videoid, title, description, channel, link, date, thumbnail with this method for the top (20, up to 50) search results. Package into a bundle and returns as a list of dicts.
    """

    search_response = youtube.search().list(q=query, part='id,snippet', maxResults=maxResults).execute()
    videoids = []
    titles = []
    channels = []
    links = []
    publishdates = []
    thumbs = []
    
    n, m = 0, 0
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videoids.append(search_result['id']['videoId'])
            titles.append(search_result['snippet']['title'])
            channels.append(search_result['snippet']['channelTitle'])
            links.append("http://www.youtube.com/watch?v=" + search_result['id']['videoId'])
            date = dateutil.parser.parse(search_result['snippet']['publishedAt'])
            publishdates.append(date) #always UTC time
            thumbs.append(search_result['snippet']['thumbnails']['high']['url'])
        else:
            print(search_result['snippet']['title'])
            n += 1
        m+= 1

    video_ids = ','.join(videoids) #concatenate into one string for api call
    descriptions = _full_description(video_ids)

    if n:
        print(str(n) + " channels/playlists in main search were not recorded for " + query)
    
    print(str(m) + " videos recorded for " + query)
    
    #Text processing, ex. O'Rourke always prints as O&#39;Rourke

    for i in range(len(titles)):
        titles[i] = titles[i].replace("&#39;", "'")
        titles[i] = titles[i].replace("&quot;", "'")
        descriptions[i] = descriptions[i].replace("&#39;", "'")
        descriptions[i] = descriptions[i].replace("&quot;", "'")
    
    #prettify
    bundle = [
            {"videoid": videoids[i], 
             "title": titles[i], 
             "description": descriptions[i], 
             "channel": channels[i], 
             "link": links[i], 
             "date": publishdates[i], 
             "thumbnail": thumbs[i]} 
            for i in range(len(videoids))]
        
    return bundle