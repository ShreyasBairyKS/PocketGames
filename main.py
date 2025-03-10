import random  #to generate random choices by the computer for hand cricket and rock paper scissors

def hangman():  #function to play the hangman game
    def choose_word():
        words = ['python', 'java', 'swift', 'javascript', 'kotlin', 'typescript', 'rust']   #wordbank
        return random.choice(words) #returns a random programming language

    def display_current_state(word, guessed_letters): #function to display the guessed word
        display = ''.join([letter if letter in guessed_letters else '_' for letter in word])
        print('Current word:', display)
    
    word = choose_word()
    guessed_letters = set()
    wrong_guesses = 0
    max_wrong_guesses = 6   #maximum number of attempts
    print("Welcome to Hangman!")
    print("Guess the programming language, one letter at a time.")
    while wrong_guesses < max_wrong_guesses:
        display_current_state(word, guessed_letters)
        guess = input("Enter a letter: ").lower()
        #Check the condition of the guess entered by the user
        if guess in guessed_letters:
            print("You already guessed that letter. Try again.")
        elif guess in word:
            guessed_letters.add(guess)
            print("Good guess!")
        else:
            wrong_guesses += 1
            print(f"Wrong guess! You have {max_wrong_guesses - wrong_guesses} guesses left.")
            guessed_letters.add(guess)
        if all(letter in guessed_letters for letter in word):   #Checks whether the complete word has been guessed
            print(f"Congratulations! You've guessed the word: {word}")
            break
    else:
        print(f"Sorry, you've run out of guesses. The word was: {word}")
        
def hand_cricket(): #function to play hand cricket
    def get_user_choice():
        while True:
            try:    #Prevention when user enters a non numerical value
                user_input = int(input("Enter your choice (1-6): "))
                if 1 <= user_input <= 6:
                    return user_input
                else:
                    print("Invalid input. Enter a number between 1 and 6.")
            except ValueError:
                print("Invalid input. Enter a number between 1 and 6.")
    
    print("Welcome to Hand Cricket!")
    player_score = 0
    computer_score = 0
    print("\nPlayer's turn to bat:")
    while True:
        player_choice = get_user_choice()
        computer_choice = random.randint(1, 6)  #generates random number between 1 to 6
        print(f"Computer chose: {computer_choice}")
        if player_choice == computer_choice:
            print("Player is out!")
            break                       #exits the loop
        player_score += player_choice
        print(f"Score: {player_score}")
    print(f"\nPlayer's final score: {player_score}")
    print("\nComputer's turn to bat:")
    while True:
        player_choice = get_user_choice()
        computer_choice = random.randint(1, 6)
        print(f"Computer chose: {computer_choice}")
        if player_choice == computer_choice:
            print("Computer is out!")
            break
        computer_score += computer_choice
        print(f"Computer's score: {computer_score}")
        if computer_score > player_score:
            break
    print(f"\nComputer's final score: {computer_score}")
    if player_score > computer_score:
        print("\nCongratulations! You win!")
    elif player_score < computer_score:
        print("\nComputer wins! Better luck next time.")
    else:
        print("\nIt's a tie!")
        
def rock_paper_scissors():  #function to play rock paper scissors
    def get_bot_choice():
        choices = ['Rock', 'Paper', 'Scissors']
        return random.choice(choices)
    
    def winner(player, bot): #function to find out who won
        if player == bot:
            return "It's a draw! Both chose {}.".format(player)
        elif (player == 'Rock' and bot == 'Scissors') or (player == 'Paper' and bot == 'Rock') or  (player == 'Scissors' and bot == 'Paper'):
            return "You win! {} beats {}.".format(player, bot)
        else:
            return "You lose! {} beats {}.".format(bot, player)
    
    
    play_again = 'Y'
        
    while play_again in ['Y', 'y']:
        choice = input("\nEnter your choice (R for Rock, P for Paper, S for Scissors): ").upper()
            
        dict1 = {'R':'Rock','P': 'Paper','S':'Scissors'}
            
        player_choice = dict1[choice]
            
        if choice not in ['R', 'P', 'S']:   #checks whether the input is valid
            print("Invalid choice. Please try again.")
            continue
            
        bot_choice = get_bot_choice()
            
        print("You chose: {}".format(player_choice))
        print("Computer chose: {}".format(bot_choice))
            
        result = winner(player_choice, bot_choice)
        print(result)
            
        play_again = input("Do you want to play again? (Y/N): ").upper()
        
    print("Thanks for playing!")

while True:
    choice = input("Enter the game of your choice: (1. Hangman, 2. Hand Cricket, 3. Rock-Paper-Scissors, 4. Exit) ")
    if choice == '1':
        hangman()
    elif choice == '2':
        hand_cricket()
    elif choice == '3':
        rock_paper_scissors()
    elif choice == '4':
        print("Thank You!")
        break
    else:
        print("Invalid choice. Please select 1, 2, or 3.")
