from tkinter import *
from design import *
from card import Card, collect_cards
from deal import Deal
import ctypes

# Initializing window as a tkinter object
window = Tk()
window.geometry('1280x720')
window.title('Blackjack => By Ansh Gaikwad')
window.configure(bg=background_color)

# UI frames

# Player
player_frame = Frame(window, bg=background_color, **hightlight_frame_with_white)
player_frame.pack(side=BOTTOM, fill=X)

player_cards_frame = Frame(player_frame, bg=background_color)
player_cards_frame.pack(side=RIGHT, fill=Y)

player_options_frame = Frame(player_frame, bg=background_color)
player_options_frame.pack(**pack_left_and_fill_y)

# Dealer
dealer_frame = Frame(window, bg=background_color, **hightlight_frame_with_white)
dealer_frame.pack(side=TOP, fill=X)

dealer_cards_frame = Frame(dealer_frame, bg=background_color)
dealer_cards_frame.pack(side=TOP, fill=Y)

# Chips
player_chips_frame = Frame(window, bg=background_color)
player_chips_frame.pack(side=BOTTOM, fill=Y)

chip1 = PhotoImage(file=r'./chips/1.png')
chip2 = PhotoImage(file=r'./chips/2.png')
chip5 = PhotoImage(file=r'./chips/5.png')
chip10 = PhotoImage(file=r'./chips/10.png')
chip20 = PhotoImage(file=r'./chips/20.png')
chip25 = PhotoImage(file=r'./chips/25.png')
chip50 = PhotoImage(file=r'./chips/50.png')
chip100 = PhotoImage(file=r'./chips/100.png')
chip250 = PhotoImage(file=r'./chips/250.png')
chip500 = PhotoImage(file=r'./chips/500.png')
chip1000 = PhotoImage(file=r'./chips/1000.png')
chip2000 = PhotoImage(file=r'./chips/2000.png')
chip5000 = PhotoImage(file=r'./chips/5000.png')

_1 = Button(player_chips_frame, image=chip1)
_2 = Button(player_chips_frame, image=chip2)
_5 = Button(player_chips_frame, image=chip5)
_10 = Button(player_chips_frame, image=chip10)
_20 = Button(player_chips_frame, image=chip20)
_25 = Button(player_chips_frame, image=chip25)
_50 = Button(player_chips_frame, image=chip50)
_100 = Button(player_chips_frame, image=chip100)
_250 = Button(player_chips_frame, image=chip250)
_500 = Button(player_chips_frame, image=chip500)
_1000 = Button(player_chips_frame, image=chip1000)
_2000 = Button(player_chips_frame, image=chip2000)
_5000 = Button(player_chips_frame, image=chip5000)

_1.pack(side=LEFT)
_2.pack(side=LEFT)
_5.pack(side=LEFT)
_10.pack(side=LEFT)
_20.pack(side=LEFT)
_25.pack(side=LEFT)
_50.pack(side=LEFT)
_100.pack(side=LEFT)
_250.pack(side=LEFT)
_500.pack(side=LEFT)
_1000.pack(side=LEFT)
_2000.pack(side=LEFT)
_5000.pack(side=LEFT)

# Score Board
scoreboard = Frame(window, bg=background_color)
scoreboard.pack(side=LEFT, fill=Y)

dealer_score = Frame(scoreboard, bg=background_color)
dealer_score.pack(side=TOP, fill=BOTH)

player_score = Frame(scoreboard, bg=background_color)
player_score.pack(side=BOTTOM, fill=BOTH)

player_score_label = Label(player_score, bg=background_color, text='Your Score: 00', **button_args)
player_score_label.pack()

dealer_score_label = Label(dealer_score, bg=background_color, text="Dealer Score: 00", **button_args)
dealer_score_label.pack()

# Bet Amount
betboard = Frame(window, bg=background_color)
betboard.pack(side=RIGHT, fill=Y)

placed_bet = Frame(betboard, bg=background_color)
placed_bet.pack(side=TOP, fill=BOTH)

remaining_chips = Frame(betboard, bg=background_color)
remaining_chips.pack(side=BOTTOM, fill=BOTH)

placed_bet_label = Label(placed_bet, bg=background_color, text='Placed Bet: 0$', **button_args)
placed_bet_label.pack()

remaining_chips_label = Label(remaining_chips, bg=background_color, text="CHIPS: 2000$", **button_args)
remaining_chips_label.pack()

# Player options in the game - I
deal_btn = Button(player_options_frame, text=' DEAL ', **button_args, bg="#34CA3A")
deal_btn.pack(side=LEFT, fill=Y)

player_game_options_frame = Frame(player_options_frame, bg=background_color)
player_game_options_frame.pack(side=TOP, fill=X)

# Player options in the game - II
hit = Button(player_game_options_frame, text='HIT', bg='#FF3300', **button_args, state=DISABLED, name='hit')
stand = Button(player_game_options_frame, text='STAND', bg='#B5BD18', **button_args, state=DISABLED, name='stand')
double = Button(player_game_options_frame, text='DOUBLE', bg='#CC00CC', **button_args, state=DISABLED, name='double')
split = Button(player_game_options_frame, text='SPLIT', bg='#66FFFF', **button_args, state=DISABLED, name='split')

hit.pack(side=TOP, fill=X)
stand.pack(side=TOP, fill=X)
double.pack(side=TOP, fill=X)
split.pack(side=TOP, fill=X)

# Player Cards
player_card1_image = Card.hidden_card()
player_card1_label = Label(player_cards_frame, image=player_card1_image, bg=background_color, name='dealcard1_player')
player_card1_label.pack(side=RIGHT)

player_card2_image = Card.hidden_card()
player_card2_label = Label(player_cards_frame, image=player_card2_image, bg=background_color, name='dealcard2_player')
player_card2_label.pack(side=RIGHT)

# Dealer Cards
dealer_card1_image = Card.hidden_card()
dealer_card1_label = Label(dealer_cards_frame, image=dealer_card1_image, bg=background_color, name='dealcard1_dealer')
dealer_card1_label.pack(side=LEFT)

dealer_card2_image = Card.hidden_card()
dealer_card2_label = Label(dealer_cards_frame, image=dealer_card2_image, bg=background_color, name='dealcard2_dealer')
dealer_card2_label.pack(side=LEFT)

# Busted Text
player_busted_message = Label(player_cards_frame, text='BUSTED', font=font_medium, fg='#FF0000', bg=background_color)
dealer_busted_message = Label(dealer_cards_frame, text='BUSTED', font=font_medium, fg='#FF0000', bg=background_color)

# Table Frame for displaying result of the deal (WON OR LOST)
deal_results_frame = Frame(window, bg=background_color)
deal_results_frame.pack(fill=BOTH, side=LEFT)

game = Deal(
    master=window,
    player_cards_frame=player_cards_frame,
    player_game_options_frame=player_game_options_frame,
    player_card1_label=player_card1_label,
    player_card2_label=player_card2_label,
    dealer_card1_label=dealer_card1_label,
    dealer_card2_label=dealer_card2_label,
    player_score_label=player_score_label,
    dealer_score_label=dealer_score_label,
    dealer_cards_frame=dealer_cards_frame,
    deal_results_frame=deal_results_frame,
    player_busted_message=player_busted_message,
    dealer_busted_message=dealer_busted_message,
    split=split,
    placed_bet_label=placed_bet_label,
    remaining_chips_label=remaining_chips_label,
)


# Dealing a game
def deal_init():
    # Clean player frame from the hit cards
    Deal.clean_table(frames=[player_cards_frame, dealer_cards_frame, deal_results_frame])

    # Initialize Card Instances so this way i will have a new deck each time deal is pressed
    cards_instances = []

    # Initialize Game
    game = Deal(
        deck=cards_instances,
        master=window,
        player_cards_frame=player_cards_frame,
        player_game_options_frame=player_game_options_frame,
        player_card1_label=player_card1_label,
        player_card2_label=player_card2_label,
        dealer_card1_label=dealer_card1_label,
        dealer_card2_label=dealer_card2_label,
        player_score_label=player_score_label,
        dealer_score_label=dealer_score_label,
        dealer_cards_frame=dealer_cards_frame,
        deal_results_frame=deal_results_frame,
        player_busted_message=player_busted_message,
        dealer_busted_message=dealer_busted_message,
        split=split,
        placed_bet_label=placed_bet_label,
        remaining_chips_label=remaining_chips_label,
    )

    # Condition if bet is not placed
    if int(game.get_placed_bet()) != 0:

        game.get_bet(int(game.get_placed_bet()))
        game.set_placed_bet_to_zero()

        # Starting operations in real game
        for card in collect_cards():
            cards_instances.append(Card(name=card))  # (Card instance)

        # deal player
        game.deal_player()

        # deal for dealer
        # handle all dealt cards for dealer for here so we can keep one undisplayed
        dealer_1 = game.get_card(dealer_card1_label, is_player=False)
        dealer_2 = game.get_card(dealer_card2_label, is_player=False, display=False)

        # fill the score board
        game.set_scoreboard()

        # See if split should be disabled or enabled
        game.set_split_button_state()

        # Set the Buttons click function <Button-1> Stand for left click
        hit.bind('<Button-1>', lambda event: game.hit(dealer_2))
        stand.bind('<Button-1>', lambda event: game.finish_player_turn(dealer_2))
        double.bind('<Button-1>', lambda event: game.double())

    else:
        ctypes.windll.user32.MessageBoxW(0,
                                         "Please place a bet",
                                         "Bet is not placed", 1)


def place_bet():

    # Initialize Chips
    _1.bind('<Button-1>', lambda event: game.chips1_add())
    _2.bind('<Button-1>', lambda event: game.chips2_add())
    _5.bind('<Button-1>', lambda event: game.chips5_add())
    _10.bind('<Button-1>', lambda event: game.chips10_add())
    _20.bind('<Button-1>', lambda event: game.chips20_add())
    _25.bind('<Button-1>', lambda event: game.chips25_add())
    _50.bind('<Button-1>', lambda event: game.chips50_add())
    _100.bind('<Button-1>', lambda event: game.chips100_add())
    _250.bind('<Button-1>', lambda event: game.chips250_add())
    _500.bind('<Button-1>', lambda event: game.chips500_add())
    _1000.bind('<Button-1>', lambda event: game.chips1000_add())
    _2000.bind('<Button-1>', lambda event: game.chips2000_add())
    _5000.bind('<Button-1>', lambda event: game.chips5000_add())

    # fill the bet board
    game.set_bet()

    # Binding Deal Button
    deal_btn.bind('<Button-1>', lambda event: deal_init())


place_bet()
window.mainloop()
