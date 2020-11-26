# Problem Set 2, hangman.py
# Name: Рутов Олег, КМ-03
# Collaborators: Плиско Єлизавета, КМ-03
# Time spent: приблизно 4 години

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)

import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()



# ----------------------------------------------------------------------
#                               Hangman
# ----------------------------------------------------------------------



def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for checking_letter in secret_word:
        if not checking_letter in letters_guessed:
            return False
    return True



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guessed_word = ''
    for checking_letter in secret_word:
        if checking_letter in letters_guessed:
            guessed_word += checking_letter
        else:
            guessed_word += '_ '
    return guessed_word



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    avaliable_letters = ''
    for checking_letter in string.ascii_lowercase:
        if checking_letter not in letters_guessed:
            avaliable_letters += checking_letter + ' '
    return avaliable_letters




def warning_alert(guessed_letter, letters_guessed):
    """
    guessed_letter: the letter we must check
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: True if there are a problem situation with warning
             or False if the letter is correct.

    Also function prints warning message if warning was found.
    """
    if not guessed_letter.isalpha():
        print("Oops! That is not a valid letter. ", end='')
        return True
    elif guessed_letter in letters_guessed:
        print("Oops! You've already guessed that letter. ", end='')
        return True
    else:
        return False



def get_sanction(guessed_letter):
    """
    my_letter: incorrect guessed letter
    returns: number of guesses, which will be taken away for incorrect guess.
    """
    if guessed_letter in 'aeiou':
        return 2
    else:
        return 1



def get_total_score(guessed_word, remaining_guesses_number):
    """
    guessed_word: word, which was guessed successful
    remaining_guesses_number: number of remaining guesses
    returns: total score of successful game

    Game score calculation is performed by formula:
    total score = number of unique letters in word * number of remaining guesses
    """
    unique_letters = set()
    for letter in guessed_word:
        unique_letters.add(letter)
    return remaining_guesses_number * len(unique_letters)



def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    guesses_remaining = 6
    warnings_remaining = 3
    letters_guessed = []
    user_win = False
    print('Welcome to the game Hangman!'
          f'\nI am thinking of a word that is {len(secret_word)} letters long.'
          f'\nYou have {warnings_remaining} warnings left.')
    while guesses_remaining > 0:
        print('---------------------------------------'
              f'\nYou have {guesses_remaining} guesses left.'
              f'\nAvaliable letters: {get_available_letters(letters_guessed)}')
        guessed_letter = input('Please guess a letter: ').lower()
        if warning_alert(guessed_letter, letters_guessed):
            if warnings_remaining > 0:
                warnings_remaining -= 1
                print(f"You have {warnings_remaining} warnings left: ", end='')
            else:
                guesses_remaining -= 1
                print("You have no warnings left so you lose one guess: ", end='')
        else:
            letters_guessed.append(guessed_letter)
            if guessed_letter in secret_word:
                print('Good guess: ', end='')
            else:
                guesses_remaining -= get_sanction(guessed_letter)
                print('Oops! That letter is not in my word: ', end='')
        print(get_guessed_word(secret_word, letters_guessed))
        if is_word_guessed(secret_word, letters_guessed):
            user_win = True
            break
    print('---------------------------------------')
    if user_win:
        print('Congratulations, you won! Your total score for this game is:',
              get_total_score(secret_word, guesses_remaining))
    else:
        print('Sorry, you ran out of guesses. The word was else')



# ----------------------------------------------------------------------
#                          Hangman with hints
# ----------------------------------------------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    if len(my_word) == len(other_word):
        for checking_index in range(0, len(my_word)):
            if my_word[checking_index] != '_':
                if my_word[checking_index] != other_word[checking_index]:
                    return False
                elif my_word.count(my_word[checking_index]) != other_word.count(my_word[checking_index]):
                    return False
        return True
    else:
        return False



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    my_word = my_word.replace(' ', '')
    matches_not_found = True
    print('Possible word matches are: ', end='')
    for checking_word in wordlist:
        if match_with_gaps(my_word, checking_word):
            matches_not_found = False
            print(checking_word, end=' ')
    if matches_not_found:
        print('no matches found in basic words library')
    else:
        print()



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    guesses_remaining = 6
    warnings_remaining = 3
    letters_guessed = []
    user_win = False
    print('Welcome to the game Hangman!'
          f'\nI am thinking of a word that is {len(secret_word)} letters long.'
          f'\nYou have {warnings_remaining} warnings left.')
    while guesses_remaining > 0:
        print('---------------------------------------'
              f'\nYou have {guesses_remaining} guesses left.'
              f'\nAvaliable letters: {get_available_letters(letters_guessed)}')
        guessed_letter = input('Please guess a letter: ').lower()
        if guessed_letter == '*':
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
        else:
            if warning_alert(guessed_letter, letters_guessed):
                if warnings_remaining > 0:
                    warnings_remaining -= 1
                    print(f"You have {warnings_remaining} warnings left: ", end='')
                else:
                    guesses_remaining -= 1
                    print("You have no warnings left so you lose one guess: ", end='')
            else:
                letters_guessed.append(guessed_letter)
                if guessed_letter in secret_word:
                    print('Good guess: ', end='')
                else:
                    guesses_remaining -= get_sanction(guessed_letter)
                    print('Oops! That letter is not in my word: ', end='')
            print(get_guessed_word(secret_word, letters_guessed))
            if is_word_guessed(secret_word, letters_guessed):
                user_win = True
                break
    print('---------------------------------------')
    if user_win:
        print('Congratulations, you won! Your total score for this game is:',
              get_total_score(secret_word, guesses_remaining))
    else:
        print('Sorry, you ran out of guesses. The word was else')



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":

    # pass

###############

    ## Random choose of secret word
    # secret_word = choose_word(wordlist)

    ## Input secret word from console
    # secret_word = input('?')


    ####


    ## Start hangman game
    # hangman(secret_word)

    ## Start hangman game with hints
    # hangman_with_hints(secret_word)

    # exit(0)

###############

    ## Ineractive testing cover:

    while True:
        print('///////////////////////////////////////')
        print('DEV MODE MENU')
        print('* To play hangman with random word without hints, enter "rd"'
              '\n* To play hangman with random word and hints, enter "rh"'
              '\n* To play hangman with your word without hints, enter "ed"'
              '\n* To play hangman with your word and hints, enter "eh"'
              '\n* To exit program, enter "b"')
        users_change = input('Enter your change: ').lower()

        if "b" in users_change:
            break

        print('///////////////////////////////////////')

        change_correct = True

        if "r" in users_change:
            secret_word = choose_word(wordlist)
        elif "e" in users_change:
            secret_word = input('>>> Enter your word: ')
        else:
            change_correct = False
            print('Error! Incorrect change')

        if change_correct:
            if "d" in users_change:
                hangman(secret_word)
            elif "h" in users_change:
                hangman_with_hints(secret_word)
            else:
                print('Error! Incorrect change')
