"""
Purpose: To collect data from youtube and analyze any political trends in Youtube's search algorithms.

Sources of error/ leniency:
For some politicians, a common name unfortunately means that they are superceded by another person - perhaps a famous athlete or comedian. Some politicans also go by different names and *may* be referred to by two at a relatively similar frequency. 

It is recommended to consider the typical search for a candidate - ex. Mitch McConnell instead of Addison Mitchell McConnell, Chuck Schumer instead of Charles Ellis Schumer.
    
4 high profile examples:
    Ted Cruz, Beto O'Rourke
    Diane Feinstein, Mitch McConnell
    
4 medium profile examples:
    Rob Portman, Tina Smith
    Marsha Blackburn, Ro Khanna
    
4 low profile examples:
    Roger Williams, Ron Wright
    Scott Peters, Maria Cantwell
    
"""

import vader as v
import youtubepull as yt
import member_functions as f


def score_pull(name, maxResults = 20):
    """Downloads a list of youtube videos in a conviniently packaged bundle of dictionaries each consisting of:
        
    videoid, title, description, channel, link, date, thumbnail.
    
    Includes VaderSentiment scores of description_rating and title_rating.
    
    Prints channels that are not recorded but in the top search results, and prints a weighted score based on VaderSentiment scores of vanilla sentiment as a reference. 
    
    *Note that VaderSentiment is not optimized for this purpose.
    """
    bundle = yt.theworks(name, maxResults)
    
    combined_score = []

    for i in range(len(bundle)):
        #Generate vaderSentiment ratings as a reference, add to bundle
        title_rating, description_rating = v.sentiment_analyzer(bundle[i]["title"]), v.sentiment_analyzer(bundle[i]["description"])
        bundle[i]["title_rating"], bundle[i]["description_rating"] = title_rating, description_rating
        
        description, title = title_rating['compound'], description_rating['compound']
        
        #create a compound score from the description and title
        combined_score.append(0.5*description + 0.5*title)
        
    #Generate a single score for reference with exponential decay as the rank decreases
    score = f.exponentialdecay(combined_score, len(combined_score), factor = -0.2)
    
    print("Weighted score is ", score)
    
    return bundle