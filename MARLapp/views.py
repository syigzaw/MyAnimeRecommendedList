from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import requests
from xml.etree import ElementTree
from bs4 import BeautifulSoup
import time

def index(request):
	return render(request, 'MARLapp/index.html')

def input(request):
	username = request.GET['input']
	print(username)
	url = reverse('results', kwargs={'username': username})
	return HttpResponseRedirect(url)

def results(request, username):
	print('\n\n\n\n\n')
	animeListXml = requests.get('http://myanimelist.net/malappinfo.php?u=' + username + '&status=all&type=anime')
	animeListRoot = ElementTree.fromstring(animeListXml.text)
	recommendedAnimeList = {}

	for animeXmlIndex, animeXml in enumerate(animeListRoot):
		if animeXml.tag != 'myinfo' and animeXml[13].text != '0':
			# animeList.append({
			# 	'id': animeXml[0].text,
			# 	'title': animeXml[1].text,
			# 	'score': animeXml[13].text
			# })

			animeHtml = requests.get('http://myanimelist.net/anime/' + animeXml[0].text)
			if animeHtml.status_code == 429:
				t = 0.5
				for i in range(10):
					print(t)
					time.sleep(t)
					animeHtml = requests.get('http://myanimelist.net/anime/' + animeXml[0].text)
					print('\n\n\n')
					print('-------------------------------')
					print(animeXml[1].text, animeXmlIndex, len(animeListRoot))
					print('-------------------------------')
					t *= 2
					if animeHtml.status_code == 200:
						break

			recommendedAnimeHtmlList = BeautifulSoup(animeHtml.content, 'html.parser').find('ul', class_='anime-slide js-anime-slide').find_all('a', class_='link bg-center')
			time.sleep(0.1)

			for recommendedAnimeHtml in recommendedAnimeHtmlList:
				myScore = int(animeXml[13].text)
				numOfRecs = int(recommendedAnimeHtml.find('span', class_='users').string.split()[0])
				recommendedAnimeScoreHtml = requests.get('http://myanimelist.net/anime/' + recommendedAnimeHtml.get('href').split('/')[5].split('-')[0])
				if recommendedAnimeScoreHtml.status_code == 429:
					t = 0.5
					for i in range(10):
						print(t)
						time.sleep(t)
						recommendedAnimeScoreHtml = requests.get('http://myanimelist.net/anime/' + recommendedAnimeHtml.get('href').split('/')[5].split('-')[0])
						print('\n\n\n')
						print('-------------------------------')
						print(animeXml[1].text, animeXmlIndex, len(animeListRoot))
						print('-------------------------------')
						t *= 2
						if recommendedAnimeScoreHtml.status_code == 200:
							break
				recommendedAnimeScore = float(BeautifulSoup(recommendedAnimeScoreHtml.content, 'html.parser').find('div', class_='fl-l score').get_text(strip=True))
				time.sleep(0.1)
				addedScore = myScore * numOfRecs * recommendedAnimeScore

				if recommendedAnimeHtml.find('span', class_='title fs10').string not in [y[1].text for x, y in enumerate(animeListRoot)]:
					if recommendedAnimeHtml.find('span', class_='title fs10').string in recommendedAnimeList:
						recommendedAnimeList[recommendedAnimeHtml.find('span', class_='title fs10').string] += addedScore
					else:
						recommendedAnimeList[recommendedAnimeHtml.find('span', class_='title fs10').string] = addedScore
				print(recommendedAnimeList)

	# print(animeList)
	print('\n\n\n\n\n')
	return HttpResponse(username)