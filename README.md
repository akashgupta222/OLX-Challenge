# OLX- Code the Curious Challenge

## Ads Recommendation
Akash Gupta

akashgupta222 | akii.gupta16@gmail.com

The approach for the solution is as follows: 

# Preprocessing
## Reading the csv files and making data structures:
### user_data.csv
-  Columns Read: 'event_time', 'user_id' ,'event', 'ad_id'
-  Converted event time from string to pandas datetime
-  Sorted the dataframe by event time (ascending) 
-  Made a user dictionary where I stored the list of  ads viewed for each user, indexed by the user_id. 
- Made a second user dictionary where I stored the list of  ads messaged for each user, indexed by the user_id 
### user_messages.csv
- Converted the ads into a python list 
- Made a category dictionary storing the list of ads messaged in user_messages.csv corresponding to each category. The dictionary was indexed by the category_id 
### ads_data.csv
- Read the ad_id, enabled and category_id columns into a pandas dataframe. 
- Converted the dataframe into a dictionary indexed by the ad_id. Each ad_id has a value telling whether it is enabled or not and telling the category of the ad_id. 

# Model Used 
For each user-category pair in the user_messages_test.csv, two approaches: 
- If we have some activity of the user in that category : Content Based Recommendation. 
- Else, if we  dont have any activity of the user in that category: Popularity Based Recommendation. 
## Content Based Recommendation: 
For each user-category pair in user_messages_test.csv, do the following:
- Find out the list of ads which the user has viewed from the user dictionary we had built from user_data.csv. 
- Filter the list to keep the ads only from the given category with the help of ad_dictionary we had created. 
- Filter the list to keep only the ads which would be enabled for displaying to the users in the next seven days and lets call this list ad_list. 
- Reverse this list in descending order(latest events first) and call it the recent list. 
- From the ad_list, find out the most popular ads (by counting) and filter this list to keep only the ads which have been viewed more than once. Lets call this list popular_list. 
- Initialize the recommendation list to empty list. 
- Append all elements for the popular_list to the recommendation_list. 
- For each element in recent_list, append to recommendation_list if the element is not already there. 
- Extract a overall list of all the ads in the given category, not related to the user, from the category dictionary we had created from the user_messages.csv. From this list, find out the most popular ads and append them to the recommendation list until the length of the recommendation list is greater than 20. 
- Now the recommendation list might have some ads which the user would have already messaged. We need to remove these ads. 
- So, using the second user dictionary we had created from user_data.csv, find out the ads the user has already messaged and remove such ads from the recommendation list. 
- Return the first 10 elements of the recommendation list. 
- This way we are recommending a list of popular ads followed by recent ads followed by the trending ads. 
### Such a model was used because: 
- A user has a high chance to message an ad he has viewed many times but not yet messaged yet. (Justifying the popular ads) 
- A user has a moderate chance to message an ad he has viewed recently. (Justifying the recent ads) 
- A user a chance to message the ads to which many other users are already messaging. (Justifying the trending ads). 
## Popularity Based Recommendation: 
For each user-category pair in user_messages_test.csv, do the following if the user does not have any activity in the given category (cold start problem) : 
- Extract a overall list of all the ads in the given category, not related to the user, from the category dictionary we had created from the user_messages.csv. From this list, find out the most popular ads and append them to the recommendation list. 
- Return the first 10 elements of the recommendation list. 
- This way we are recommending the trending ads for the cold start problem. 
### Such a model was used because: 
- A user a chance to message the ads to which many other users are already messaging. (Justifying the trending ads). 

## Exploratory Data Analysis (EDA): 
- EDA revealed that close to 20% users in user_messages_test have messaged an ad which they recently viewed further strengthening the intuition of using the ads already viewed. 
- For each category in user_messages.csv, it was found out that there are only 5-7 ads having high number of messages with the rest having less than 3 messages. This skew in the distribution made way for recommending the top trending ads. 
- User journey was observed for about many users which showed that before a user messages an ad, he always has a view event associated with it. This made way for recommending the recent ads. 
## Dataset Quality: 
- Most of the latitude and longitude were very close to each other, defeating the purpose of giving them explicitly (Looks like the users have been sampled out by location). 
- No missing values were found apart from the latitude and longitude making it a good dataset. 

### Advice to beginners: 
As one of my friend pointed out after seeing my solution, you need to look at the data first and see for the trends yourself before feeding it into machine learning algorithms. 

# Running the code
### Requirements: 
Python 2.7.6 
Pandas 0.18.1 http://pandas.pydata.org/
Numpy 1.12.1 http://www.numpy.org/

### Running: 
1. Keep the data csv files and the python script in the same folder and change working directory to that folder. 
2. Run the ad_recommend.py script (python ad_recommend.py)
3. Output is in ads_recommendation.csv
