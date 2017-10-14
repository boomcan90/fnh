import bs4 as bs
import urllib.request
def reutersTitles():

	sauce = urllib.request.urlopen('http://feeds.reuters.com/Reuters/worldNews').read()

	soup = bs.BeautifulSoup(sauce, 'lxml')
	titles = []
	for title in soup.find_all('title'):
		titles.append(title.text)
	return titles

print(reutersTitles())
