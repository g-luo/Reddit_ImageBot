#import Reddit's praw library and Google's BeautifulSoup (you can find instructions online)
import praw
import urllib.request
from bs4 import BeautifulSoup
import requests
import json
				  
def detect_comment():	
	#initialize your Reddit bot
	bot = praw.Reddit(user_agent='RedditBot v0.1',
				  client_id='insert yours here',
	              client_secret='insert yours here',
	              username='insert yours here',
	  			  password='insert yours here')
	
	#collect all the comments in a thread and cycle through them
	subreddit = bot.subreddit('insert yours here')
	comments = subreddit.stream.comments()
	
	for comment in comments:
		text = comment.body 
		caption = text.split()
		text ='+'.join(caption) #the search term sent to image_scrape 
		caption =' '.join(caption) #the caption for the bot's reply
		
		plus = text.find("+")+1 #to find the location of the next distinct word
		if (text[0].isupper() and text[plus].isupper()): #checking for consecutive upper-case words
			link = image_scrape(text) #link is the url to the image
			message = "[Beep boop. I am a bot. Here's a photo of "+caption+".]("+link+")"
			comment.reply(message)

def image_scrape(query):
	#searches for the first Google image with the given search term (query)
	url = "https://www.google.com/search?q=" + query + "&source=lnms&tbm=isch"
	headers={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
	try:
		html = requests.get(url, headers=headers).text
	except requests.ConnectionError:
		print("couldn't reach google")
	soup = BeautifulSoup(html, 'html.parser')
	image = soup.find("div",{"class":"rg_meta"})
	try:
	    link = json.loads(image.text)["ou"]
	except AttributeError:
	    print("No images found.")
	except ValueError:
	     print("Wrong formatting for json.")
			
	return link #returns the first Google image link 

if __name__ == "__main__":
	detect_comment() #main method; doesn't do much
