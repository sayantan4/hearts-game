import tkinter
from tkinter import *
import random
from greenlet import greenlet
from collections import OrderedDict
import time
from colorama import *

cards_on_play = OrderedDict()
points_display = None
turn_display = None
deck_display = None
user_cards = None
b_user = None
b_machine1 =None
b_machine2 = None
b_machine3 = None
button_clear_deck = None
winner_display = None
dict_of_buttons = dict()
ROW = 1

root = Tk()


class Card:
	def __init__(self, value, color, rank):
		self.value = value
		self.color = color
		self.rank = rank


class Machines:
	def __init__(self, name, index, id):
		self.name = name
		self.is_turn = False
		self.type = "Machine"
		self.next_index = index
		self.points = 0
		self.cards = list()
		self.id = id


class User:
	def __init__(self, name, index):
		self.name = name
		self.is_turn = False
		self.type = "User"
		self.next_index = index
		self.points = 0
		self.cards = list()


machine1 = Machines(name="BOB", index=1, id=1)
machine2 = Machines(name="Lisa", index=2, id=2)
machine3 = Machines(name="Andy", index=3, id=3)
user = User(name="YOUR", index=0)

colors = ['hearts', 'diamonds', 'spades', 'clubs']
deck = list()
for value in range(1, 14):
	rank = value
	for color in colors:
		if value == 11:
			value = 'J'
		elif value == 12:
			value = 'Q'
		elif value == 13:
			value = 'K'
		card = Card(value=value, color=color, rank=rank)
		deck.append(card)

random.shuffle(deck)

machine1.cards, machine2.cards, machine3.cards, user.cards = deck[:13], deck[13:26], deck[26:39], deck[39:]
# e = Entry(root, width=35, borderwidth=5)
# e.grid(row=0, column=0, columnspan=3, padx=10, pady=10 )


def display_deck():
	global deck_display
	global cards_on_play
	colour = None
	string_to_display = ''
	text = ''
	# import ipdb;ipdb.set_trace()
	for cards in cards_on_play.values():
		values = cards[1]
		if cards[0] == 'hearts' or cards[0] == 'diamonds':
			colour = Fore.RED
		else:
			colour = Fore.BLACK

		if cards[1] == 11:
			values = 'J'
		elif cards[1] == 12:
			values = 'Q'
		elif cards[1] == 13:
			values = 'K'

		string_to_display = f'{string_to_display},{cards[0]}({values})'
	if string_to_display == '':
		text = "Deck is Empty"
	else:
		text = string_to_display[1:]
	deck_display.configure(text=text)
	deck_display.update()


def click(number):
	if user.is_turn:
		global b_user
		global dict_of_buttons
		global cards_on_play
		global ROW
		if cards_on_play and present_suit_present(user) and dict_of_buttons[number].color != get_first_card_on_deck()[0]:
			pass

		else:
			ROW = ROW + 1
			cards = dict_of_buttons[number]
			cards_on_play[f'{user.name}'] = [f'{cards.color}', f'{cards.rank}']
			user.cards.remove(cards)
			# user.is_turn = False
			number.destroy()
			b_user = Button(root, text=f"{cards.color}({cards.value})", highlightbackground=color_decider(cards.color),height=10, width=10)
			b_user.grid(row=8, column=ROW, sticky=W, pady=10)
			b_user.update()
			backward_process.switch()


def color_decider(color):
	if color == 'hearts' or color == 'diamonds':
		return "RED"
	else:
		return "BLACK"

def is_all_buttons_from_deck_removed():
	global b_user
	global b_machine1
	global b_machine3
	global b_machine2
	if not b_user and not not b_machine1 and not b_machine3 and not b_machine2:
		return True
	else:
		return False
def clear_deck():
	global b_user
	global b_machine1
	global b_machine3
	global b_machine2
	if b_user and b_machine1 and b_machine3 and b_machine2:
		b_user.destroy()
		b_machine1.destroy()
		b_machine2.destroy()
		b_machine3.destroy()

def main():
	global turn_display
	global deck_display
	global points_display
	global user_cards
	global dict_of_buttons
	global button_clear_deck
	global winner_display
	root.configure(background='Blue')
	points_text = "BOB -> 0, Lisa -> 0, Andy -> 0, Your -> 0"
	turn_display = Label(root, text="TURN", bg ="RED", height=5, width=15)
	turn_display.grid(row=0, column=0, pady=2)
	points_display = Label(root, text=points_text, bg="GREEN", height=10, width=32)
	points_display.grid(row=2, column=0, pady=2)
	winner_display = Label(root, text="WINNER ?", bg ="RED", height=5, width=15)
	winner_display.grid(row=0, column=8, pady=10, padx=10)

	# Label(root, text="Deck").grid(row=5, column=5, sticky=W, pady=10)
	# deck_display = Label(root, text="Deck is Empty", bg="GREEN",height=10, width=10)
	# deck_display.grid(row=6, column=5, sticky=W, pady=10)
	# button_clear_deck = Button(root, text='CLEAR DECK ', height=4, width=15, command=clear_deck)
	root.title("Hearts")
	b1 = Button(root, text=f"{user.cards[0].color}({user.cards[0].value})", highlightbackground=color_decider(user.cards[0].color),height=10, width=9, command=lambda: click(b1))
	b2 = Button(root, text=f"{user.cards[1].color}({user.cards[1].value})", highlightbackground=color_decider(user.cards[1].color),height=10, width=9, command=lambda: click(b2))
	b3 = Button(root, text=f"{user.cards[2].color}({user.cards[2].value})", highlightbackground=color_decider(user.cards[2].color),height=10, width=9, command=lambda: click(b3))
	b4 = Button(root, text=f"{user.cards[3].color}({user.cards[3].value})", highlightbackground=color_decider(user.cards[3].color),height=10, width=9, command=lambda: click(b4))
	b5 = Button(root, text=f"{user.cards[4].color}({user.cards[4].value})", highlightbackground=color_decider(user.cards[4].color),height=10, width=9, command=lambda: click(b5))
	b6 = Button(root, text=f"{user.cards[5].color}({user.cards[5].value})", highlightbackground=color_decider(user.cards[5].color),height=10, width=9, command=lambda: click(b6))
	b7 = Button(root, text=f"{user.cards[6].color}({user.cards[6].value})", highlightbackground=color_decider(user.cards[6].color),height=10, width=9, command=lambda: click(b7))
	b8 = Button(root, text=f"{user.cards[7].color}({user.cards[7].value})", highlightbackground=color_decider(user.cards[7].color),height=10, width=9, command=lambda: click(b8))
	b9 = Button(root, text=f"{user.cards[8].color}({user.cards[8].value})", highlightbackground=color_decider(user.cards[8].color),height=10, width=9, command=lambda: click(b9))
	b10 = Button(root, text=f"{user.cards[9].color}({user.cards[9].value})", highlightbackground=color_decider(user.cards[9].color), height=10, width=9, command=lambda: click(b10))
	b11 = Button(root, text=f"{user.cards[10].color}({user.cards[10].value})", highlightbackground=color_decider(user.cards[10].color), height=10, width=9, command=lambda: click(b11))
	b12 = Button(root, text=f"{user.cards[11].color}({user.cards[11].value})", highlightbackground=color_decider(user.cards[11].color), height=10, width=9, command=lambda: click(b12))
	b13 = Button(root, text=f"{user.cards[12].color}({user.cards[12].value})", highlightbackground=color_decider(user.cards[12].color), height=10, width=9, command=lambda: click(b13))

	# button_clear_deck.grid(row=1, column=0,  pady=100)
	row_of_cards_for_user = 30
	b1.grid(row=row_of_cards_for_user, column=0, sticky=W, pady=10)
	b2.grid(row=row_of_cards_for_user, column=1, sticky=W, pady=10)
	b3.grid(row=row_of_cards_for_user, column=2, sticky=W, pady=20)
	b4.grid(row=row_of_cards_for_user, column=3, sticky=W, pady=10)
	b5.grid(row=row_of_cards_for_user, column=4, sticky=W, pady=10)
	b6.grid(row=row_of_cards_for_user, column=5, sticky=W, pady=10)
	b7.grid(row=row_of_cards_for_user, column=6, sticky=W, pady=10)
	b8.grid(row=row_of_cards_for_user, column=7, sticky=W, pady=10)
	b9.grid(row=row_of_cards_for_user, column=8, sticky=W, pady=10)
	b10.grid(row=row_of_cards_for_user, column=9, sticky=W, pady=10)
	b11.grid(row=row_of_cards_for_user, column=10, sticky=W, pady=10)
	b12.grid(row=row_of_cards_for_user, column=11, sticky=W, pady=10)
	b13.grid(row=row_of_cards_for_user, column=12, sticky=W, pady=10)

	dict_of_buttons[b1] = user.cards[0]
	dict_of_buttons[b2] = user.cards[1]
	dict_of_buttons[b3] = user.cards[2]
	dict_of_buttons[b4] = user.cards[3]
	dict_of_buttons[b5] = user.cards[4]
	dict_of_buttons[b6] = user.cards[5]
	dict_of_buttons[b7] = user.cards[6]
	dict_of_buttons[b8] = user.cards[7]
	dict_of_buttons[b9] = user.cards[8]
	dict_of_buttons[b10] = user.cards[9]
	dict_of_buttons[b11] = user.cards[10]
	dict_of_buttons[b12] = user.cards[11]
	dict_of_buttons[b13] = user.cards[12]

	root.after(4000, backward_process.switch)

	root.mainloop()


def get_first_card_on_deck() -> list:
	global cards_on_play
	for card in cards_on_play.values():
		return card


def only_hearts_present(player) -> bool:
	count = 1  # to determine wether there are  cards other than hearts
	for cards in player.cards:
		if cards.color != 'hearts':
			count = 0
			break
	return True if count else False


def find_the_min_card(player, suit_only_to_include=None) -> Card:
	MIN_CARD_RANK = 30
	min_card = None
	if suit_only_to_include:
		for card in player.cards:
			if card.color == suit_only_to_include:
				if MIN_CARD_RANK > card.rank:
					MIN_CARD_RANK = card.rank
					min_card = card
	else:
		for card in player.cards:
			if MIN_CARD_RANK > card.rank:
				MIN_CARD_RANK = card.rank
				min_card = card
	return min_card


def find_the_max_card(player, suit_only_to_include=None, exclude_suits=None) -> Card:
	MAX_CARD_RANK = -1
	max_card = None
	cards_to_check = []
	for card in player.cards:
		if suit_only_to_include:
			if card.color == suit_only_to_include:
				cards_to_check.append(card)
		elif exclude_suits:
			if card.color != exclude_suits[0] and card.color != exclude_suits[1]:
				cards_to_check.append(card)
		else:
			cards_to_check.append(card)

	for card in cards_to_check:
		# import ipdb;ipdb.set_trace()
		if MAX_CARD_RANK < card.rank:
			MAX_CARD_RANK = card.rank
			max_card = card

	return max_card


def least_suit(player) -> str:
	MIN_CARD_RANK = 30
	least_frequency_suit = ''
	from collections import defaultdict
	dict_to_store_frequency_of_suits = defaultdict(int)
	for card in player.cards:
		dict_to_store_frequency_of_suits[card.color] = dict_to_store_frequency_of_suits[card.color] + 1
	for suit in dict_to_store_frequency_of_suits:
		if MIN_CARD_RANK > dict_to_store_frequency_of_suits[suit]:
			MIN_CARD_RANK = dict_to_store_frequency_of_suits[suit]
			least_frequency_suit = suit
	return least_frequency_suit


def suit_exists_other_than_hearts_spade(player) -> bool:
	count = 0
	for card in player.cards:
		if card.color != 'hearts' and card.color != 'spades':
			count = 1
			break
	return True if count else False


def present_suit_present(player) -> bool:
	card_details_of_first_card = get_first_card_on_deck()
	for card in player.cards:
		if card.color == card_details_of_first_card[0]:
			return True
	return False


def get_card_with_max_value_on_deck_of_same_suit(card_details) -> list:
	global cards_on_play
	MAX_CARD_RANK = int(card_details[1])
	card_details_having_max_value = []
	for card in cards_on_play.values():
		if card_details[0] == card[0]:
			if MAX_CARD_RANK <= int(card[1]):
				MAX_CARD_RANK = int(card[1])
				card_details_having_max_value = card
	return card_details_having_max_value


def custom_sort_of_card_objects(card):
	return card.rank


def number_just_less_than_current_card(player):
	card_details_of_first_card = get_first_card_on_deck()
	max_card_of_that_suit = get_card_with_max_value_on_deck_of_same_suit(card_details_of_first_card)
	cards = [card for card in player.cards if card.color == card_details_of_first_card[0]]
	cards.sort(key=custom_sort_of_card_objects)
	card_just_less_than_current_card = None
	# import ipdb;ipdb.set_trace()
	for card in cards:
		if card.rank > int(max_card_of_that_suit[1]):
			break
		else:
			card_just_less_than_current_card = card

	return card_just_less_than_current_card


def number_just_greater_than_current_card(player):
	card_details_of_first_card = get_first_card_on_deck()
	max_card_of_that_suit = get_card_with_max_value_on_deck_of_same_suit(card_details_of_first_card)
	cards = [card for card in player.cards if card.color == card_details_of_first_card[0]]
	cards.sort(key=custom_sort_of_card_objects, reverse=True)
	card_just_greater_than_current_card = None
	# import ipdb;
	# ipdb.set_trace()
	for card in cards:
		if card.rank < int(max_card_of_that_suit[1]):
			break
		else:
			card_just_greater_than_current_card = card

	return card_just_greater_than_current_card


def king_spade(player):
	spade_king = None
	for card in player.cards:
		if card.color == 'spades' and card.rank == 13:
			spade_king = card
	return spade_king


def queen_spade(player):
	spade_queen = None
	for card in player.cards:
		if card.color == 'spades' and card.rank == 12:
			spade_queen = card
	return spade_queen


def heart_present(player):
	for card in player.cards:
		if card.color == 'hearts':
			return True
	return False


def first_turn(player, round):
	global cards_on_play
	global b_machine1
	global b_machine3
	global b_machine2
	if only_hearts_present(player):
		card = find_the_min_card(player)
	else:
		if round == 1:
			suit = least_suit(player)
			if (suit == 'spades' and (find_the_max_card(player, suit_only_to_include=suit).rank == 12 or find_the_max_card(player, suit_only_to_include=suit).rank == 13)) or (suit =='hearts') :
				if suit_exists_other_than_hearts_spade(player):
					card = find_the_max_card(player, exclude_suits=['spades', 'hearts'])
				else:
					card = find_the_min_card(player)
			else:
				card = find_the_max_card(player, suit_only_to_include=suit)

		else:
			card = find_the_min_card(player, suit_only_to_include=least_suit(player))

	cards_on_play[f'{player.name}'] = [f'{card.color}', f'{card.rank}']
	global ROW
	ROW = ROW + 1
	if player.id == 1:
		b_machine1 = Button(root, text=f"{card.color}({card.value})", highlightbackground=color_decider(card.color),
						height=10, width=10)
		b_machine1.grid(row=8, column=ROW, sticky=W, pady=10)
		b_machine1.update()
	if player.id == 2:
		b_machine2 = Button(root, text=f"{card.color}({card.value})", highlightbackground=color_decider(card.color),
						height=10, width=10)
		b_machine2.grid(row=8, column=ROW, sticky=W, pady=10)
		b_machine2.update()
	if player.id == 3:
		b_machine3 = Button(root, text=f"{card.color}({card.value})", highlightbackground=color_decider(card.color),
						height=10, width=10)
		b_machine3.grid(row=8, column=ROW, sticky=W, pady=10)
		b_machine3.update()

	player.cards.remove(card)


def on_the_way(player):
	global b_machine1
	global b_machine3
	global b_machine2
	if present_suit_present(player):
		card = number_just_less_than_current_card(player)
		if not card:
			card = number_just_greater_than_current_card(player)
			if card.color == 'spades' and card.rank == 12:
				if king_spade(player):
					card = king_spade(player)
	else:
		if queen_spade(player):
			card = queen_spade(player)
		elif heart_present(player):
			card = find_the_max_card(player, suit_only_to_include='hearts')
		else:
			suit = least_suit(player)
			card = find_the_max_card(player, suit_only_to_include=suit)
	global ROW
	ROW = ROW + 1
	cards_on_play[f'{player.name}'] = [f'{card.color}', f'{card.rank}']
	# import ipdb;
	# ipdb.set_trace()
	if player.id == 1:
		b_machine1 = Button(root, text=f"{card.color}({card.value})", highlightbackground=color_decider(card.color),
						height=10, width=10)
		b_machine1.grid(row=8, column=ROW, sticky=W, pady=10)
		b_machine1.update()
	if player.id == 2:
		b_machine2 = Button(root, text=f"{card.color}({card.value})", highlightbackground=color_decider(card.color),
						height=10, width=10)
		b_machine2.grid(row=8, column=ROW, sticky=W, pady=10)
		b_machine2.update()
	if player.id == 3:
		b_machine3 = Button(root, text=f"{card.color}({card.value})", highlightbackground=color_decider(card.color),
						height=10, width=10)
		b_machine3.grid(row=8, column=ROW, sticky=W, pady=10)
		b_machine3.update()

	player.cards.remove(card)


def compute():
	global turn_display
	global points_display
	global cards_on_play
	global b_user
	global b_machine1
	global b_machine3
	global b_machine2
	global ROW
	global points_display
	global winner_display
	players = [machine1, machine2, machine3, user]
	random.choice(players).is_turn = True  # starting the game with random player
	points_of_each_user = dict()
	for round in range(1, 14):
		player_to_start_round = None
		no_of_players_played_till_now = 0  # signifies how many players have played in one round.
		for player in players:
			if player.is_turn:
				player_to_start_round = player
		player = player_to_start_round
		while no_of_players_played_till_now < 5:
			if no_of_players_played_till_now == 4:
				time.sleep(5)
				b_user.destroy()
				b_machine1.destroy()
				b_machine2.destroy()
				b_machine3.destroy()
				break
			turn_display.configure(text=f"It is {player.name} turn")
			turn_display.update()
			print(player.name)
			time.sleep(2)
			# import ipdb;ipdb.set_trace()
			if player.type == "User":
				main_loop.switch()
			elif not cards_on_play:
				# time.sleep(5)
				first_turn(player, round)
				# time.sleep(5)
			else:
				# time.sleep(5)
				on_the_way(player)
			# display_deck()
			no_of_players_played_till_now = no_of_players_played_till_now + 1
			player.is_turn = False
			player = players[player.next_index]
			if no_of_players_played_till_now < 4:
				player.is_turn = True



		# Fetching the first Card
		player_with_first_card = None
		for player in cards_on_play:
			player_with_first_card = player
			break

		# Identifying which is the player with highest rank
		color, max_rank = cards_on_play[player_with_first_card]
		player_with_highest_card = player_with_first_card
		for player in cards_on_play:
			if cards_on_play[player][0] == color:
				if int(cards_on_play[player][1]) > int(max_rank):
					max_rank = cards_on_play[player][1]
					player_with_highest_card = player

		# Calculating points for the highest player
		points = 0

		for player in cards_on_play:
			if cards_on_play[player][0] == 'hearts':
				points = points + 1
			elif cards_on_play[player][0] == 'spades' and int(cards_on_play[player][1]) == 12:
				points = points + 13
		# time.sleep(7)
		ROW = 1
		# assigning points to players and deciding who will start next
		# points_display_text = ''
		for player in players:
			if player.name == player_with_highest_card:
				player.points = player.points + points
				player.is_turn = True
			points_of_each_user[player.name] = player.points


		# displaying points of each player

		print(cards_on_play)

		points_display_text = f"BOB -> {points_of_each_user['BOB']}, Lisa -> {points_of_each_user['Lisa']}, Andy -> {points_of_each_user['Andy']}, Your -> {points_of_each_user['YOUR']}"
		points_display.configure(text=points_display_text)
		points_display.update()
		for player in players:
			print(f'{player.name} ->  {player.points} (after round {round})/n')



		cards_on_play.clear()
		# display_deck()

	# Deciding the winner

	for player in players:
		if player.points == 26:
			print(f"{player.name} is the Winner")
	MIN = 30
	winner = None
	for player in players:
		if player.points == 26:
			winner = player.name
			break
		if MIN > player.points:
			MIN = player.points
			winner = player.name

	print(f"{winner} is the Winner")

	winner_display.configure(text=f'Winner is {winner}')
	winner_display.update()
	main_loop.switch()


main_loop = greenlet(main)
backward_process = greenlet(compute)
main_loop.switch()