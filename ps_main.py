import time
from selenium import webdriver
from random import randint


class PokemonBot():
	def __init__(self):
		self.browser = webdriver.Chrome()

	def start(self):
		self.browser.get('https://play.pokemonshowdown.com/')
		time.sleep(4)
		button = self.browser.find_element_by_css_selector('.button.mainmenu1.big')
		button.click()
		time.sleep(2)
		self.browser.find_element_by_name('username').send_keys("ssganu13")
		time.sleep(1)
		self.browser.find_element_by_xpath("/html/body/div[4]/div/form/p[2]/button[1]").click()
		time.sleep(1)
		self.browser.find_element_by_css_selector('.button.mainmenu1.big').click()

		time.sleep(8)
		
		
		while(True):
			try: 
				random = randint(0, 3)
				self.browser.find_elements_by_name('chooseMove')[random].click()
			except:
				x = 1

bot = PokemonBot()
bot.start()