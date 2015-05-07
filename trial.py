
y = 'chinked'
guesses = 2*len(y)
letters ="abcdefghijklmnopqrstuvwxyz"
for i in range(guesses):
    
    
    print "You have " ,guesses," guesses left."
    x = raw_input("Please guess a letter")
    if x in y:
        print "Good guess "
        letters = letters.split(x)
        
        letters = letters[0] + letters[1]
        print "Available letters",letters
    
        
    else:
        guesses = guesses - 1
        print "Available letters",letters
    
