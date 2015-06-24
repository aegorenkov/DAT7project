# Project Proposal: Predict whether a Twitter user will retweet the PersonalVictories hashtag

##What is the question you hope to answer?
I plan to answer whether it is possible to predict whether a Twitter user will retweet a particular hashtag given their Twitter history. In this particular case I am interested in the PersonalVictories hastag, but will use another if the sample size proves to be too small. A related question is what kind of topics such users are interested in. The broader goal is to say something about what kind of users retweet a particular hashtag.

##What data are you planning to use to answer that question?
I plan to use the Twitter API. Ideally, I can pull in tweets with the hastag PersonalVictories using the Twitter streaming API because it has a rate limit of 180 requests per hour as opposed to 60 requests per hour. If I have trouble with the streaming API I can use the search API to pull up a smaller sample of tweets using the lower rate limit.

##What do you know about the data so far?
I know there are severe limitation in the API and I have to start early and plan carefully. Generally, I have a user's tweet history, followers, following, and most recent favorited tweets.

##Why did you choose this topic?
I chose this topic so I can get some practice with Natural Language Programming as well as working with streaming datasets. The particular question arose when I met a GA student who owns a small page that reposts tweets that contain the PersonalVictories hashtag--he was curious about what type of people read his page. 
