import vadersentiment as v
import youtubepull as yt
import member_functions as f


def get_rate_limited(start, end, namelist):
    """Implementation of """
    new_scores = []
    for member_index in range(start, end):
        
        titles, descriptions = yt.titlesanddescriptions(namelist[member_index]["name"]) #titles and descriptions of top 50 search results (will print failures)
        
        ratingsynthesis = []
        
        for i in range(len(titles)):
            title_rating, description_rating = v.sentiment_analyzer(titles[i]), v.sentiment_analyzer(descriptions[i])
            ratingsynthesis.append({'title_rating': title_rating, 'description_rating': description_rating})
    
        synthesize = []
        
        for i in range(len(ratingsynthesis)):
            description, title = ratingsynthesis[i]["description_rating"], ratingsynthesis[i]["title_rating"]
            combined = f.averagedict(description, title, 0.5, 0.5)
            synthesize.append(combined)
    
        #Conduct exponential decay on each data set
        
        compound = []
        for i in range(len(synthesize)):
            compound.append(synthesize[i]["compound"])
        
        
        score = f.exponentialdecay(compound, len(compound))
        
        temp = namelist[member_index]
        temp["score"] = score
        new_scores.append(temp)
        
    return new_scores    


def single_score(name):
    titles, descriptions = yt.titlesanddescriptions(name)
    
    ratingsynthesis = []
    
    for i in range(len(titles)):
        title_rating, description_rating = v.sentiment_analyzer(titles[i]), v.sentiment_analyzer(descriptions[i])
        ratingsynthesis.append({'title_rating': title_rating, 'description_rating': description_rating})
    
    synthesize = []
    
    for i in range(len(ratingsynthesis)):
        description, title = ratingsynthesis[i]["description_rating"], ratingsynthesis[i]["title_rating"]
        combined = f.averagedict(description, title, 0.5, 0.5)
        synthesize.append(combined)
    
    #Conduct exponential decay on each data set
    
    compound = []
    for i in range(len(synthesize)):
        compound.append(synthesize[i]["compound"])
    
    
    score = f.exponentialdecay(compound, len(compound))
    
    return score, titles, descriptions, synthesize, compound



