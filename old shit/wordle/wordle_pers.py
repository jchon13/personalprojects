import numpy as np

#Load in accepted words form word_list.txt
text_file = open("word_list.txt","r")
possible_words = text_file.readlines()
text_file.close()


#remvoe \n at the end of words
for i in range(len(possible_words)):
    possible_words[i] = possible_words[i][0] + possible_words[i][1] + possible_words[i][2] + possible_words[i][3] + possible_words[i][4]

def frequency_calc(possible_words):
    #Calculates frequency ie. how often a letter shows up in a spot
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    frequencies = {}
    for letter in alphabet: #goes through each possible letter
        freq = [0, 0, 0, 0, 0] #Initialise frequency of a letter
        for i in range(0, 5): #Iterates through each letter possition
            for word in possible_words:
                #if the position of letter == letter(var) increase freq 
                if word[i] == letter:  
                    freq[i] +=1
        frequencies.update({letter:freq})
    return frequencies

def wordScores(possible_words,frequencies):
    #Gives the best score
    max_score = 1000000000000000000000
    best_word = "wwwww"  
    scores = {}
    max_freqs = [0, 0, 0, 0, 0]
    for value in frequencies:
        for i in range(0,5):
            if max_freqs[i] < frequencies[value][i]:
                max_freqs[i] = frequencies[value][i]
    #Above gets the highest possible occurance of a single letter in a position
    '''Below the "score" of each word is calculated via frequency of a letter
    at a position - the highest possible frequency at that position. The score
    is the sum of all the positions scores.'''

    #Lower score is better as it indicates it is closer to the max frequency
    #Therefore more likely.
    for words in possible_words:
        score = 1 #reinitialise with every word
        for j in range(0, 5):
            letter = words[j]
            score *= 1 + (frequencies[letter][j]- max_freqs[j]) ** 2 #must square in case of negatives
            scores.update({words:score})
    #return scores

    for word in possible_words:
        if scores[word] < max_score:
            best_word = word
            max_score = scores[word]
    return best_word


def remover(guess,result, possible_words):
    #w= wrong, g=green, y=yellow

    #Getting the bad letters
    bad_letters = []
    bad_positions = []
    for j in range(0,5):
        if result[j] == 'w':
            bad_letters.append(guess[j])
            bad_positions.append(j)
            #print(bad_letters)
    #Getting words that match green
    good_words = possible_words
    letters = []
    positions = []

    cross_letters = []
    cross_positions = []
    
    for i in range(len(result)): #gets letters and positions of greens
        if result[i] == 'g':
            letters.append(guess[i])
            positions.append(i)

    for i in range(len(letters)): #gets the cross letters
        for j in range(len(bad_letters[:])):
            if bad_letters[j] == letters[i]:
                print(bad_letters[j])
                cross_letters.append(bad_letters[j])
                cross_positions.append(bad_positions[j])
                bad_letters.remove(bad_letters[j])
                bad_positions.remove(bad_positions[j])
                



    for i in range(len(letters)): #filters through accepted words with only greens
        good_words = getGoodWords(good_words,positions[i],letters[i])


    #Filtering out all wrong words into unallowed_words
    unallowed_words = []
    for word in possible_words:
        for letter in bad_letters:
            for i in range(0,5):
                if word[i] == letter:
                    unallowed_words.append(word)
    
    #print(good_words)
    #Remove bad words from good words
    for un_word in unallowed_words:
        for g_words in good_words[:]:
            if un_word == g_words:
                good_words.remove(un_word)
    #print(good_words)

    if(len(cross_letters)==0):
        pass
    else:
        unallowed_words2 = possible_words
        for i in range(len(cross_letters)):
            unallowed_words2 = badWords(unallowed_words2,cross_positions[i],cross_letters[i])
        for un_word2 in unallowed_words2:
            for g_words in good_words[:]:
                if un_word2 == g_words:
                    good_words.remove(un_word2)
        #print(unallowed_words2)
    


    #print(unallowed_words2)

    letters = []
    positions = []

    for i in range(len(result)): #gets letters and positions of yellows
        if result[i] == 'y':
            letters.append(guess[i])
            positions.append(i)

    
    for i in range(len(letters)): #filters through accepted words with only greens
        good_words = yellowWords(good_words,positions[i],letters[i])

    return good_words
    

def getGoodWords(possible_words,position,letter):
    new_good_words = []
    for word in possible_words:
        if word[position] == letter:
            new_good_words.append(word)
    return new_good_words

def yellowWords(possible_words,position,letter):
    new_good_words = []
    for word in possible_words:
        for i in range(0,5):
            if i == position:
                pass
            elif word[i] == letter:
                new_good_words.append(word)
            else:
                pass
    return new_good_words

def badWords(possible_words,position,letter):
    new_bad_words = [] 
    for word in possible_words:
        if word[position] == letter:
            new_bad_words.append(word)
    return new_bad_words

def solver(possible_words):
    '''solves the wordle'''
    print('Welcome to the solver!')
    print('Suggested word is:',wordScores(possible_words,frequency_calc(possible_words)))
    print('Enter First Guess')
    guess = input()
    print('Enter Result')
    result = input()
    counter = 1
    while result != "ggggg" and counter < 6:
        possible_words=remover(guess,result, possible_words)
        print(possible_words)
        if len(possible_words) == 0:
            break
        suggestion = wordScores(possible_words, frequency_calc(possible_words))
        print("The suggested word is:", suggestion)
        print("Enter your next guess:")
        guess = input()
        print("Enter your new result:")
        result = input()
        counter += 1

solver(possible_words)


sample = ['adept', 'after', 'agent', 'avert', 'begat', 'cadet', 'cater', 'cheat', 'eaten', 'eaten', 'eater', 'eater', 'extra', 'facet', 'great', 'hater', 'matey', 'taken', 'taker', 'tamer', 'taper', 'terra', 'theta', 'tread', 'treat', 'treat', 'tweak', 'water', 'wheat']
guess = 'eater'
result= 'wgggg'






