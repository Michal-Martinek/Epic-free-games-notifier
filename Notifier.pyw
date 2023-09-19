import requests
import json
import os, sys
import datetime
import winrt.windows.ui.notifications as notifications
import winrt.windows.data.xml.dom as dom

def getResponse() -> dict:
	url = 'https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=CZ&allowCountries=CZ'
	res = requests.get(url)
	return json.loads(res.text)
def getField(js, name: str) -> dict:
	if not isinstance(js, dict) or name not in js: raise KeyError(f'Json field not found "{name}"')
	return js[name]
def getFields(js, *fields):
	for f in fields:
		js = getField(js, f)
	return js
def parseDate(date: str):
	date = date.split('.')[0]
	return datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
def isFree(game):
	try:
		for offers in getFields(game, "promotions", "promotionalOffers"):
			for offer in getField(offers, "promotionalOffers"):
				if getFields(offer["discountSetting"]["discountPercentage"]) != 0: continue
				if parseDate(offer["startDate"]) < datetime.datetime.now() < parseDate(offer["endDate"]):
					return True
	except KeyError:
		pass
	return False
def getFreeGames():
	js = getResponse()
	js = getFields(js, "data", "Catalog", "searchStore", "elements")
	return [g for g in js if isFree(g)]
# -----------------------------------------------------------
def thumbnailName(url):
	return url.split('/')[-1]
def getThumbnailUrl(game):
	for img in getField(game, "keyImages"):
		if img["type"] == "Thumbnail":
			return img["url"]
def downloadThumbnail(url):
	res = requests.get(url)
	with open("Thumbnails\\" + thumbnailName(url), 'wb') as f:
		f.write(res.content)
def spawnNotification(game, thumbnailUrl):
	notifier = notifications.ToastNotificationManager.create_toast_notifier(sys.executable)
	tString = f"""
	<toast>
		<visual>
			<binding template='ToastGeneric'>
				<text>New free Epic Game: {game["title"]}</text>
				<text hint-maxLines='2'>{game["description"]}</text>
				<image placement='appLogoOverride' src="file:///{os.getcwd()}/epic-games-icon.ico"/>
				<image src="file:///{os.getcwd()}/Thumbnails/{thumbnailName(thumbnailUrl)}"/>
			</binding>
		</visual>
	</toast>
	"""
	xDoc = dom.XmlDocument()
	xDoc.load_xml(tString)
	notification = notifications.ToastNotification(xDoc)
	notifier.show(notification)
def reportFree(games):
	for game in games:
		url = getThumbnailUrl(game)
		downloadThumbnail(url)
		spawnNotification(game, url)

def main():
	games = getFreeGames()
	reportFree(games)

if __name__ == '__main__':
	main()
