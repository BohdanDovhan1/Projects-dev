import random
import time
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True
#Class
class Card:
    
    def __init__(self,suits,ranks):
        self.suits = suits
        self.ranks = ranks
    
    def __str__(self):
        return f"{self.ranks} of {self.suits}"   
#Class
class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(f"{rank} of {suit}")
                
    def __str__(self):
        return (str('\n'.join(self.deck)))
    
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        out_card = self.deck.pop(0)
        return out_card
#Class   
class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
        
    def add_card(self,out_card):
        self.cards.append(out_card)
    
        if self.value>10 and (out_card.split(' ', 1)[0])=='Ace':
            values['Ace']=1   
        else:
            values['Ace']=11
        self.value += values[(out_card.split(' ', 1)[0])]
#Class
class Chips:
    
    def __init__(self,total):
        self.total = total  # This can be set to a default value or supplied by a user input
        #l=self.total
        self.bet = 0
        print(f'Now you have:  {self.total}')
        
    def win_bet(self):
        self.total+=self.bet
        return self.total
    
    def lose_bet(self):
        self.total-=self.bet
        return self.total
#Function
def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('Enter your bet: '))
            if chips.bet < 0:
                raise 
                continue
        except:
            print('Please use positive numbers only!')
            continue
        else:
            if chips.bet > chips.total:
                print ('Not enough money!')
                continue
            else:
                print(f'Your bet {chips.bet} accepted!')
                break
#Function
def hit(deck,hand):
    hand.add_card(deck.deal())
#Function
def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    decision = (input('Hit or Stand? H/S')).capitalize()
    while True:
        if decision[0] == 'H':
            print('Hit')
            hit(deck,hand)
        elif decision[0] == 'S':
            print('Stand')
            playing = False
        else:
            print('Did not understand your decision!')
            continue
        break
#Function
def show_some(player,dealer):
    print(f'\nPlayer value: {player_hand.value} \nPlayer cards:')
    print(*player_hand.cards,sep = ", ")
    
    print(f'\nDealer cards:')
    print(*dealer_hand.cards[1:],sep = ", ")    
    
def show_all(player,dealer):
    print(f'\nPlayer value: {player_hand.value} \nPlayer cards:')
    print(*player_hand.cards,sep = ", ")
    
    print(f'\nDealer value: {dealer_hand.value} \nPlayer cards:')
    print(*dealer_hand.cards,sep = ", ")
#Function      
def player_busts(player,dealer,Chips):
    print(f'Player lost! Has {player_hand.value}')
    player_chips.lose_bet()
        
def player_wins(player,dealer,Chips):
    print('Player won!')
    player_chips.win_bet()
    
def dealer_busts(player,dealer,Chips):
    print(f'Dealer lost! Has {dealer_hand.value}')
    player_chips.win_bet()
    
def dealer_wins(player,dealer,Chips):
    print('Dealer won!')
    player_chips.lose_bet()
    
def push(player,dealer):
    print('Both have same value of cards!')    
    
    
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
print("Welcome to Blackjack game!")
money = int(input('Please enter the amount of your money: '))

while True:

    
    deck = Deck()
    deck.shuffle()
    
    #create player
    player_hand = Hand()
    
    #add a card to player
    #dealing two cards to player and dealear
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    #create dealer
    dealer_hand = Hand()
    
    #add a card to dealer
    #dealing two cards to player and dealear
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
        
    # Set up the Player's chips  
    player_chips = Chips(money)
    
    # Prompt the Player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)

    
    while playing:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand)
        
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)
  
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips) 
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:   
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)
        # Show all cards
        show_all(player_hand,dealer_hand)
    
        # Run different winning scenarios
        if dealer_hand.value >21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)
    
    # Inform Player of their chips total 
    print(f'\nPlayer chips: {player_chips.total}')
    # Ask to play again
    game = input('Start a new game? Y/N').upper()
    if game[0]=='Y':
        playing = True
        if player_chips.total > 0:
            money = player_chips.total
            continue
        else:
            print('You lost! Good bye!')
            time.sleep(2)
            break
    else:
        print('We will be waiting for you! Good bye!')
        time.sleep(2)
        break
