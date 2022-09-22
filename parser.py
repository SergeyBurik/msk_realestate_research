# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver import Proxy
# from selenium.webdriver.common.proxy import ProxyType
# from geopy.geocoders import Nominatim
# from settings import *
# from selenium.webdriver.firefox.options import Options
# import pandas as pd
#
# class Parser:
# 	def __init__(self, url):
# 		print("Parser.__init__ executing")
# 		self.url = url
# 		self.pages = 20
# 		self.driver = self.init_driver()
# 		self.output_file_name = "data_east2.csv"
#
# 		self.create_dataframe()
# 		self.driver.quit()
#
# 	def init_driver(self):
# 		myProxy = "121.1.41.162:111"
#
# 		proxy = Proxy({
# 			'proxyType': ProxyType.MANUAL,
# 			'httpProxy': myProxy,
# 			'ftpProxy': myProxy,
# 			'sslProxy': myProxy,
# 			'noProxy': ''  # set this value as desired
# 		})
#
# 		options = Options()
# 		options.add_argument('--headless')
# 		driver = webdriver.Firefox(executable_path=BROWSER_DRIVER_PATH, options=options,
# 		                           firefox_binary=FIREFOX_PATH_BIN, proxy=proxy)
# 		return driver
#
# 	def create_dataframe(self):
# 		data = self.parse()
#
# 		title = []
# 		address = []
# 		price = []
# 		price_per_meter = []
# 		meters = []
# 		building = []
# 		rooms = []
# 		is_flat = []
# 		latitude = []
# 		longitude = []
# 		floor = []
# 		floors = []
# 		metro = []
# 		metro_distance = []
# 		metro_distance_type = []
# 		description = []
#
# 		for flat in data:
# 			address.append(flat["address"])
# 			latitude.append(flat["latitude"])
# 			longitude.append(flat["longitude"])
# 			price.append(flat["price"])
# 			price_per_meter.append(flat["price_per_meter"])
# 			meters.append(flat["meters"])
# 			building.append(flat["building"])
# 			rooms.append(flat["rooms"])
# 			is_flat.append(flat["is_flat"])
# 			title.append(flat["title"])
# 			floor.append(flat["floor"])
# 			floors.append(flat["floors"])
# 			metro.append(flat["metro"])
# 			metro_distance.append(flat["metro_distance"])
# 			metro_distance_type.append(flat["metro_distance_type"])
# 			description.append(flat["description"])
#
# 		data = {'meters': meters,
# 				'address': address,
# 				'latitude': latitude,
# 				'longitude': longitude,
# 				'title': title,
# 				'price_per_meter': price_per_meter,
# 				'price': price,
# 				'floor': floor,
# 				'floors': floors,
# 		        'metro': metro,
# 		        'metro_distance': metro_distance,
# 		        'metro_distance_type': metro_distance_type,
# 		        'building': building,
# 		        'rooms': rooms,
# 		        'is_flat': is_flat,
# 		        'description': description}
#
# 		df = pd.DataFrame(data)
#
# 		print(df)
# 		df.to_csv(self.output_file_name, encoding='utf-8', index=False)
#
# 	def parse(self):
# 		data = []
# 		#prefix = "j8F4L3WVVsl4LvwItem__"
# 		prefix = "OffersSerpItem__"
# 		for i in range(1, self.pages+1):
# 			print(f"{i}/{self.pages}")
# 			self.driver.get(f"{self.url}&page={50+i}")
# 			soup = BeautifulSoup(self.driver.page_source, "html.parser")
# 			flats = soup.find_all("li", class_="OffersSerp__list-item_type_offer")
# 			#flats = soup.find_all("li", class_="OffersSerp__list-item_type_offer")
# 			print(len(flats))
# 			for flat in flats:
# 				try:
# 					title = flat.find("span", class_= prefix + "title").text.strip()
# 					building = flat.find("div", class_= prefix + "building").text.strip()
# 					address = flat.find("div", class_= prefix + "address").text.strip()
# 					price = flat.find("div", class_= prefix + "price").text.strip()
# 					price_per_meter = flat.find("div", class_= prefix + "price-detail").text.strip()
# 					metro = flat.find("span", class_= "MetroStation__title").text.strip()
# 					metro_distance = flat.find("span", class_= "MetroWithTime__distance").text.strip()
# 					description = flat.find("p", class_= prefix + "description").text.strip()
# 					metro_distance_type = 0 if flat.find_all("i", {"class": "Icon_type_small-pedestrian"}) else 1
# 					f = {"title":title, "building": building, "address": address, "price": price,
# 					     "price_per_meter": price_per_meter, "metro": metro, "metro_distance": metro_distance,
# 					     "metro_distance_type": metro_distance_type, "description": description}
# 					data.append(f)
# 				except Exception as e:
# 					print("ignored:", e)
#
# 		print(data)
# 		return self.clean(data)
#
# 	def clean(self, data):
# 		print("cleaning data...")
# 		flats = []
# 		k = 0
# 		geolocator = Nominatim(user_agent="mskapp")
# 		for el in data:
# 			k +=1
# 			if k % 50 == 0: print(k)
# 			addr = "Москва, " + el["address"]
# 			s = addr
# 			s = s.split(",")[-1]
# 			s = s.split("к")[0]
# 			s = s.split("с")[0]
#
# 			a = addr.split(",")
# 			a[-1] = s
# 			addr = ", ".join(a)
#
# 			location = geolocator.geocode(addr)
# 			try:
# 				el["latitude"] = location.latitude
# 				el["longitude"] = location.longitude
# 			except:
# 				print("location exception")
# 				el["latitude"] = None
# 				el["longitude"] = None
#
# 			price_meter = ""
# 			for s in el["price_per_meter"]:
# 				if s.isdigit(): price_meter += s
# 			el["price_per_meter"] = int(price_meter[:-1])
#
# 			price_num = ""
# 			for s in el["price"]:
# 				if s.isdigit(): price_num += s
# 			el["price"] = int(price_num)
#
# 			metro_dist = ""
# 			for s in el["metro_distance"]:
# 				if s.isdigit(): metro_dist += s
# 			el["metro_distance"] = int(metro_dist)
#
# 			building = el["building"].split()
# 			k = 0
# 			nums = ""
# 			for word in reversed(building):
# 				if word.isdigit():
# 					k += 1
# 					if k <= 2:
# 						nums += word + ";"
#
# 			floors, floor = nums.split(";")[:2]
# 			el["floor"] = int(floor)
# 			el["floors"] = int(floors)
# 			el["meters"] = int(price_num) / int(price_meter[:-1])
#
# 			rooms = 0
# 			if el["title"].count("-комнатная"):
# 				rooms = el["title"].split("-комнатная")[0][-1]
# 			elif el["title"].count("-комнатные"):
# 				rooms = el["title"].split("-комнатные")[0][-1]
# 			if el["title"].count("студия"): rooms = 0
# 			is_flat = False if el["title"].count("апартаменты") else True
# 			el["rooms"] = rooms
# 			el["is_flat"] = is_flat
#
# 			res = el
# 			flats.append(res)
#
# 		return flats



#Parser('https://msk.etagi.com/realty/?city_id[]=155&type[]=flat')
#Parser('https://realty.yandex.ru/moskva/kupit/kvartira/')
# Parser('https://realty.yandex.ru/moskva_i_moskovskaya_oblast/kupit/kvartira/?subLocality=193391&subLocality=193283&subLocality=193292&subLocality=193380&subLocality=193296&subLocality=193305&subLocality=193362&subLocality=193288&subLocality=193394&subLocality=193358&subLocality=12447&subLocality=193363&subLocality=193367&subLocality=193313&subLocality=12444&subLocality=12425&subLocality=193393&subLocality=193278&subLocality=193347&subLocality=12435&subLocality=193282&subLocality=193377&subLocality=193346&subLocality=193349&subLocality=193350&subLocality=193371&subLocality=193285&subLocality=193392&subLocality=193374&subLocality=193340&subLocality=17394073&subLocality=193341&subLocality=193345&subLocality=193293&subLocality=12431&subLocality=12434&subLocality=193388&subLocality=193348&subLocality=193351&subLocality=193378&subLocality=193357&subLocality=193364&subLocality=12453&subLocality=12452&subLocality=12449&subLocality=193384&subLocality=193385&subLocality=193281&subLocality=193297&subLocality=193299&subLocality=193304&subLocality=193289&subLocality=12450&subLocality=193355&subLocality=193356&subLocality=193361&subLocality=193284&subLocality=12440&subLocality=12443&subLocality=193336&subLocality=193337')


# Average MAE score:
# 1921015.6195226917
# (4162, 19)
# Average MAE score (only zones 3 and 4):
# 636187.3277310925

# Average MAE score:
# 1493205.7910798122
# (4164, 19)
# Average MAE score (only zones 3 and 4):
# 514120.81032412965

# Average MAE score:
# 1493205.7910798122
# (4164, 19)
# Average MAE score (only zones 3 and 4):
# 514120.81032412965
# (2224, 19)
# Average MAE score (only zones 1 and 2):
# 960988.7438202248
import random
import pandas as pd

data = pd.read_csv("data_extended_2.csv")
print(data.longitude)
s = ""
for i in range(350):
	idx = random.randint(1, 6500)
	s += f"{data.iloc[idx].longitude}%2C{data.iloc[idx].latitude}~"
print(f"https://yandex.ru/maps/?pt={s}"[:-1])
