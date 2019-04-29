import time
from selenium import webdriver
from random import randint
from selenium.webdriver.common.action_chains import ActionChains
import stat_struct
import pokemon_struct
from Move import Move
# import Pokemon

class PokemonBot():
	def __init__(self):
		self.browser = webdriver.Chrome("C:\Program Files\chromedriver_win32\chromedriver.exe")

	def start(self):
		self.browser.get('https://play.pokemonshowdown.com/')
		time.sleep(4)
		button = self.browser.find_element_by_css_selector('.button.mainmenu1.big')
		button.click()
		time.sleep(2)
		self.browser.find_element_by_name('username').send_keys("zynynzpach3")
		time.sleep(1)
		self.browser.find_element_by_xpath("/html/body/div[4]/div/form/p[2]/button[1]").click()
		time.sleep(1)
		self.browser.find_element_by_css_selector('.button.mainmenu1.big').click()

		time.sleep(10)

		# Loads up data for our side's Pokemon
		for x in range(5):
			switch = self.browser.find_elements_by_name('chooseSwitch')[x]
			ActionChains(self.browser).move_to_element(switch).perform()
			time.sleep(1)
			name_level = (self.browser.find_element_by_xpath("//*[@id=\"tooltipwrapper\"]/div/div/h2").text).split()
			
			# name_level_tokenized = 

			print(name_level)
			print(self.browser.find_element_by_xpath("//*[@id=\"tooltipwrapper\"]/div/div/p[1]").text)
			print(self.browser.find_element_by_xpath("//*[@id=\"tooltipwrapper\"]/div/div/p[2]").text)
			print(self.browser.find_element_by_xpath("//*[@id=\"tooltipwrapper\"]/div/div/p[3]").text)
			print(self.browser.find_element_by_xpath("//*[@id=\"tooltipwrapper\"]/div/div/p[4]").text)
		
		# Currently just makes random moves and logs it.
		while(True):
			try: 
				random = randint(0, 3)
				# print(self.browser.find_elements_by_name('choosename')[random].getText())
				move = self.browser.find_elements_by_name('chooseMove')[random]

				


				print(move.get_attribute('data-move'))
				print(move.get_attribute('class'))
				move.click()
			except:
				x = 1

bot = PokemonBot()
bot.start()