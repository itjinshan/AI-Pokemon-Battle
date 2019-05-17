import time
from selenium import webdriver
from random import randint
from selenium.webdriver.common.action_chains import ActionChains
# import stat_struct
# import pokemon_struct
from Move import Move
from Pokemon import Pokemon

class PokemonBot():
	def __init__(self):
		# self.browser = webdriver.Chrome("C:\Program Files\chromedriver_win32\chromedriver.exe")
		self.browser = webdriver.Chrome()
	def start(self):
		self.browser.get('https://play.pokemonshowdown.com/')
		time.sleep(4)
		button = self.browser.find_element_by_css_selector('.button.mainmenu1.big')
		button.click()
		time.sleep(2)
		self.browser.find_element_by_name('username').send_keys("zynynzpach19")
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
			pokemon_data = '';
			name_level = (self.browser.find_element_by_xpath("//*[@id=\"tooltipwrapper\"]/div/div/h2").text).split()
			
			# name_level_tokenized = 
			if len(name_level) > 2:
				pokemon_data += '[' + name_level[0] + ', ' + name_level[2] + ']\n'
			else:
				pokemon_data += '[' + name_level[0] + ', ' + name_level[1] + ']\n'
			print(pokemon_data)
			pokemon_data += self.browser.find_element_by_xpath("//*[@id=\"tooltipwrapper\"]/div/div/p[1]").text + '\n'
			pokemon_data += self.browser.find_element_by_xpath("//*[@id=\"tooltipwrapper\"]/div/div/p[2]").text + '\n'
			pokemon_data += self.browser.find_element_by_xpath("//*[@id=\"tooltipwrapper\"]/div/div/p[3]").text + '\n'
			pokemon_data += self.browser.find_element_by_xpath("//*[@id=\"tooltipwrapper\"]/div/div/p[4]").text

			# print(name_level)
			# print(self.browser.find_element_by_xpath("//*[@id=\"tooltipwrapper\"]/div/div/p[1]").text)
			# print(self.browser.find_element_by_xpath("//*[@id=\"tooltipwrapper\"]/div/div/p[2]").text)
			# print(self.browser.find_element_by_xpath("//*[@id=\"tooltipwrapper\"]/div/div/p[3]").text)
			# print(self.browser.find_element_by_xpath("//*[@id=\"tooltipwrapper\"]/div/div/p[4]").text)

			poke = Pokemon(ParseString=pokemon_data)
			print(poke.get_info_str())
		for x in range(4):
			switch = self.browser.find_elements_by_name('chooseMove')[x]
			print(switch.get_attribute('data-move'))
		
		# Currently just makes random moves and logs it.
		previous = 0

		logs = []
		currentPokemon = ''
		currentEnemy = ''
		while(True):
			try: 
				random = randint(0, 3)
				# print(self.browser.find_elements_by_name('choosename')[random].getText())
				move = self.browser.find_elements_by_name('chooseMove')[random]
				move.click()
				
				history = self.browser.find_elements_by_class_name('battle-history')
				print('Start {}, End {}'.format(previous, len(history)))
				if len(history) > previous:
					for item in history[previous:]:
						if item.text != '':
							# split = item.text.split()

							# if split[0] == 'Go!':
							# 	currentPokemon = split[1]
							# 	currentPokemon = currentPokemon[:-1]
							# if split[1] == 'sent' and split[2] == 'out':
							# 	currentEnemy = split[3]
							# 	currentEnemy = currentEnemy[:-1]
							# if split[1] == 'lost':
							# 	x = 1
							# if split[len(split) - 1] == 'fainted!':
							# 	x = 1
							# 	#update to fainted
							# if split[3] == 'used':
							# 	# opponent move is at index 4
							# 	x =1
							# if split[1] == 'restored':
							# 	x = 1
							# if split[2] == 'buffeted':
							# 	x = 1
							print(item.text)
							# print(currentPokemon)
							# print(currentEnemy)
					previous = len(history)

				# print(move.get_attribute('data-move'))
				# print(move.get_attribute('class'))
				# move.click()
			except Exception as e:
				x = 1

bot = PokemonBot()
bot.start()