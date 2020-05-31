import ctypes
from tkinter import *
from card import Card, collect_cards
from design import *
from dealer import DealerAI

bet = 0
chips = 2000
check = False  # True when user chooses double down
newbet = 0  # Used when the bet is set to zero


class Deal:
    '''
       This classes goal is to handle each IN GAME situation you have in blackjack!
       So this is why you want to pass all information from main to here as initializer
    '''

    def __init__(self,
                 master,
                 player_cards_frame, player_game_options_frame,
                 player_card1_label, player_card2_label,
                 dealer_card1_label, dealer_card2_label,
                 player_score_label, dealer_score_label,
                 placed_bet_label, remaining_chips_label,
                 dealer_cards_frame,
                 player_busted_message, dealer_busted_message,
                 deal_results_frame, split,
                 placed_bet=bet, rem_chips=chips, deck=[]
                 ):

        '''
        Indexed from game properties
        :param master:
        :param player_cards_frame:
        :param player_game_options_frame:
        :param player_card1_label:
        :param player_card2_label:
        :param dealer_card1_label:
        :param dealer_card2_label:
        :param player_score_label:
        :param dealer_score_label:
        :param placed_bet_label:
        :param remaining_chips_label:
        :param dealer_cards_frame:
        :param player_busted_message:
        :param dealer_busted_message:
        :param deal_results_frame:
        :param split:
        :param placed_bet:
        :param rem_chips:
        :param deck:
        '''

        self.deck = deck  # Card Instances
        self.master = master  # The main windows
        self.player_cards_frame = player_cards_frame  # Player frame that cards are in
        self.player_game_options_frame = player_game_options_frame  # Player options buttons during the blackjack like hit stand split Double
        self.player_card1_label = player_card1_label  # Players first card label
        self.player_card2_label = player_card2_label  # Players second card label
        self.dealer_card1_label = dealer_card1_label  # Dealer first card label
        self.dealer_card2_label = dealer_card2_label  # Dealer second card label , this is going to be hidden in the first stage
        self.player_score_label = player_score_label  # Player Score
        self.dealer_score_label = dealer_score_label  # Dealer Score
        self.dealer_cards_frame = dealer_cards_frame  # Dealer cards Frame
        self.player_busted_message = player_busted_message  # Busted case for player
        self.dealer_busted_message = dealer_busted_message  # Busted case for dealer
        self.deal_results_frame = deal_results_frame  # results of the gameplay
        self.split = split  # changing the split button dynamically if the values of first two cards are equal
        self.placed_bet = placed_bet  # For calculating player bet
        self.rem_chips = rem_chips  # For calculating remaining chips
        self.placed_bet_label = placed_bet_label  # Label for placed bet
        self.remaining_chips_label = remaining_chips_label  # Label for remaining chips

        # New indexed Parameters to be indexed throughout the deal:
        self.player_cards = []
        self.dealer_cards = []

        # Methods to Execute after Initialize
        self.enable_buttons(
            buttons=['stand', 'hit', 'double'])  # referring to the buttons that ALWAYS have to be enabled

    # This function will enable the buttons that are required on order to play
    def enable_buttons(self, buttons):
        for button in self.player_game_options_frame.winfo_children():
            if button.winfo_name() in buttons:
                button.configure(state='normal')  # set the state from disabled to normal

    '''
    Dynamic Method that changes from card to card
    Made in order to get a new card for player and dealer
    This Function responsible also to update the score of the player or dealer after the card
    By default it is for the player
    '''

    def get_card(self, card_label, display=True, is_player=True):
        card = Card.random_card(instances=self.deck)
        card_image = Card.get_card_image(card)

        if is_player:
            self.player_cards.append(card)
            # Check if to modify ACE from eleven to one
            self.handle_aces(card, self.player_cards, self.get_player_score())

        if not is_player:
            self.dealer_cards.append(card)
            # Check if to modify ACE from eleven to one
            self.handle_aces(card, self.dealer_cards, self.get_dealer_score())

        if display:
            self.display_card(card_label=card_label, card_image=card_image)
        else:
            # Change the is_displayed value from automatic True to False
            card.is_displayed = False
            hidden_card = Card.hidden_card()
            card_label.configure(image=hidden_card)
            card_label.image = hidden_card

        # Remove from the deck the selected card
        self.deck.remove(card)
        return card

    def display_card(self, card_label, card_image):
        card_label.configure(image=card_image)
        card_label.image = card_image

    def deal_player(self):
        card1 = self.get_card(self.player_card1_label)
        card2 = self.get_card(self.player_card2_label)

    '''
    This function would triggered when player hits the hit button
    This will give him another card
    And will check if the player is busted by the end of the hit
    '''

    def hit(self, dealer_card_2=None, is_player=True):
        # Bring with hidden card by default (Maybe its the dealer ? )
        hidden_card = Card.hidden_card()

        # Double Down Condition
        global check
        if check:
            check = False
            self.finish_player_turn(dealer_card_2=dealer_card_2)

        if is_player:
            # Create new label with image right there
            new_card = Label(self.player_cards_frame, image=hidden_card, bg=background_color)
            new_card.pack(side=RIGHT)

            # Call the get_card function with setting up the image of the card
            card = self.get_card(card_label=new_card)
            self.update_player_score_after_hit()

            # Handle busted
            if self.player_is_busted():
                self.player_busted_message.pack(side=TOP, anchor='nw')
                self.finish_player_turn(dealer_card_2=dealer_card_2)

            return card

        # If its the dealer and not the player
        else:
            new_card = Label(self.dealer_cards_frame, image=hidden_card, bg=background_color)
            new_card.pack(side=LEFT)

            card = self.get_card(card_label=new_card, is_player=False)
            self.update_dealer_score_after_hit()

            return card

    # Get players current score
    def get_player_score(self):
        value = 0
        for card in self.player_cards:
            value += card.value
        return str(value)

    # Get dealers current score
    def get_dealer_score(self):
        value = 0
        for card in self.dealer_cards:
            if card.is_displayed:
                value += card.value
        return str(value)

    # This will set the score board when the user clicks deal
    def set_scoreboard(self):
        self.player_score_label.configure(text=f'Player Score: {self.get_player_score()}')
        self.dealer_score_label.configure(text=f'Dealer Score: {self.get_dealer_score()}')

    # Update player score after the hit
    def update_player_score_after_hit(self):
        self.player_score_label.configure(text=f'Player Score: {self.get_player_score()}')

    # Update dealer score after the hit
    def update_dealer_score_after_hit(self):
        self.dealer_score_label.configure(text=f'Dealer Score: {self.get_dealer_score()}')

    # Clean table in given frames children
    @staticmethod
    def clean_table(frames):
        for frame in frames:
            # get all frames children
            delete_from = frame.winfo_children()

            for widget in delete_from:
                if not str(widget.winfo_name()).startswith('dealcard'):
                    widget.forget()

    '''
    Check if Player is busted
    This check will run on each hit, so we know if to continue or not
    '''

    def player_is_busted(self):
        if int(self.get_player_score()) > 21:
            return True
        else:
            return False

    '''
    Check if Dealer is busted
    This check will run on each hit, so we know if to continue or not
    '''

    def dealer_is_busted(self):
        if int(self.get_dealer_score()) > 21:
            return True
        else:
            return False

    '''
    This will handle situations after player finished
    Important first of all to display the hidden card of dealer
    '''

    def stand_or_busted(self, dealer_card_2):
        # Get its images
        card_image = Card.get_card_image(dealer_card_2)
        # Display the Card
        self.display_card(self.dealer_card2_label, card_image)
        # Change the property of is_displayed
        dealer_card_2.is_displayed = True
        # update the score of dealer
        self.update_dealer_score_after_hit()

    '''
    Decide if Split button should be enabled or not
    Should stay disabled if cards value not equal
    '''

    def set_split_button_state(self):
        player_dealt_cards = self.player_cards[0:2]
        if player_dealt_cards[0].value == player_dealt_cards[1].value:
            self.split.configure(state='normal')
        else:
            self.split.configure(state='disabled')

    # Handles what happens after player clicked stand or Busted
    def finish_player_turn(self, dealer_card_2):
        for button in self.player_game_options_frame.winfo_children():
            button.configure(state='disabled')
            button.unbind('<Button-1>')

        # Display the dealers second card and update its score
        self.stand_or_busted(dealer_card_2)

        # Start dealer Automatic Play
        dealer = DealerAI(dealer_score=self.get_dealer_score())
        while dealer.is_hit():
            self.hit(is_player=False)
            # Update the DealerAI about the new dealer score after each hit
            dealer.dealer_score = self.get_dealer_score()
            if self.dealer_is_busted():
                self.dealer_busted_message.pack(side=LEFT)

        # Decide who won the deal
        self.decider()

    '''
    This Method is going to decide who is the winner
    And gives the winning amount to winner
    '''
    def decider(self):
        global chips, newbet
        player_score = int(self.get_player_score())
        dealer_score = int(self.get_dealer_score())
        result = Label(self.deal_results_frame, text='', font=font_large, bg=background_color)
        result.pack(fill=BOTH, side=TOP)

        player_won_text = 'YOU WON!'
        dealer_won_text = 'DEALER WINS!'
        tied_text = 'PUSH!'
        both_busted = 'BOTH BUSTED!'

        if self.player_is_busted() and self.dealer_is_busted():
            result.configure(fg='#FFFFFF', text=both_busted)
            chips += newbet

        if self.player_is_busted() and not self.dealer_is_busted():
            result.configure(fg="#FF0000", text=dealer_won_text)
            # Game Over when chips are zero
            if chips == 0:
                ctypes.windll.user32.MessageBoxW(0,
                                                 "You are out of chips, Resetting Chips to 1K",
                                                 "You LOST",
                                                 1)
                self.set_rem_chips_to_onek()

        if not self.player_is_busted() and self.dealer_is_busted():
            result.configure(fg="#00FF00", text=player_won_text)
            if player_score == 21:
                chips += newbet
                chips += 1.5 * newbet
            else:
                # print(self.rem_chips)
                chips += 2 * newbet
                # print(self.rem_chips)

        if not self.player_is_busted() and not self.dealer_is_busted():
            if player_score > dealer_score:
                result.configure(fg="#00FF00", text=player_won_text)
                if player_score == 21:
                    chips += newbet
                    chips += 1.5 * newbet
                else:
                    # print(self.rem_chips)
                    chips += 2 * newbet
                    # print(self.rem_chips)
            elif player_score < dealer_score:
                result.configure(fg="#FF0000", text=dealer_won_text)
                # Game Over when chips are zero
                if chips == 0:
                    ctypes.windll.user32.MessageBoxW(0,
                                                     "You are out of chips, Resetting Chips to 1K",
                                                     "You LOST",
                                                     1)
                    self.set_rem_chips_to_onek()
            else:
                result.configure(fg='#FFFFFF', text=tied_text)
                chips += newbet

        bet = 0
        self.remaining_chips_label.configure(text=f'CHIPS: {int(chips)}$')
        self.placed_bet_label.configure(text=f'Placed Bet: {int(bet)}$')

    # This function will check the ace count in cards of dealer or player
    def ace_count(self, cards):
        counter = 0
        for card in cards:
            if str(card.name)[0] == 'A':
                counter += 1
        return counter

    # This function returns all cards instances that they are Aces
    def all_aces(self, cards):
        aces = []
        for card in cards:
            if str(card.name)[0] == 'A':
                aces.append(card)
        return aces

    # This function returns all cards instances that they are NOT Aces
    def all_not_aces_value(self, cards):
        not_aces = 0
        for card in cards:
            if str(card.name)[0] != 'A':
                not_aces += card.value

        return not_aces

    '''
    This function is going to check either Ace value must be eleven or one
    It well set the Ace value to one if he sees that total score gonna be over 21
    first argument     - self.player_cards or self.dealer cards
    second argument    - self.get_player_score() or self.get_dealer_score()
    '''

    def handle_aces(self, current_card, cards, cards_score):
        if self.ace_count(cards) == 1 and int(cards_score) > 21:
            for card in cards:
                if str(card.name)[0] == 'A':  # Only One, Looping to find it:
                    card.value = 1

        if self.ace_count(cards) > 1:
            if str(current_card.name)[0] == 'A':
                current_card.value = 1

            elif self.all_not_aces_value(cards) >= 12 - self.ace_count(cards):
                for card in self.all_aces(cards):
                    card.value = 1

    # Placed Bets Functions
    def get_placed_bet(self):
        global bet
        return bet

    def set_placed_bet_to_zero(self):
        global bet
        bet = 0

    def get_bet(self, bet):
        global newbet
        newbet = bet

    def set_bet(self):
        global chips, bet
        self.remaining_chips_label.configure(text=f'CHIPS: {int(chips)}$')
        self.placed_bet_label.configure(text=f'Placed Bet: {int(bet)}$')

    # Remaining Chips Functions
    def get_rem_chips(self):
        global chips
        return chips

    def set_rem_chips_to_onek(self):
        global chips
        chips = 1000
        self.set_bet()

    # Chips Add
    def chips1_add(self):
        global chips, bet
        if chips >= 1:
            bet += 1
            chips -= 1
        self.set_bet()

    def chips2_add(self):
        global chips, bet
        if chips >= 2:
            bet += 2
            chips -= 2
        self.set_bet()

    def chips5_add(self):
        global chips, bet
        if chips >= 5:
            bet += 5
            chips -= 5
        self.set_bet()

    def chips10_add(self):
        global chips, bet
        if chips >= 10:
            bet += 10
            chips -= 10
        self.set_bet()

    def chips20_add(self):
        global chips, bet
        if chips >= 2:
            bet += 20
            chips -= 20
        self.set_bet()

    def chips25_add(self):
        global chips, bet
        if chips >= 25:
            bet += 25
            chips -= 25
        self.set_bet()

    def chips50_add(self):
        global chips, bet
        if chips >= 50:
            bet += 50
            chips -= 50
        self.set_bet()

    def chips100_add(self):
        global chips, bet
        if chips >= 100:
            bet += 100
            chips -= 100
        self.set_bet()

    def chips250_add(self):
        global chips, bet
        if chips >= 250:
            bet += 250
            chips -= 250
        self.set_bet()

    def chips500_add(self):
        global chips, bet
        if chips >= 500:
            bet += 500
            chips -= 500
        self.set_bet()

    def chips1000_add(self):
        global chips, bet
        if chips >= 1000:
            bet += 1000
            chips -= 1000
        self.set_bet()

    def chips2000_add(self):
        global chips, bet
        if chips >= 2000:
            bet += 2000
            chips -= 2000
        self.set_bet()

    def chips5000_add(self):
        global chips, bet
        if chips >= 5000:
            bet += 5000
            chips -= 5000
        self.set_bet()

    # Double Down Function
    def double(self):
        global chips, bet, check
        check = True
        bet += bet
        chips -= bet
        self.set_bet()
