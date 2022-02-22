# Wordle-Solver-1.0

A wordle solver using English letter frequencies and vowel concentration

# How to use:

There is no UI so you must manually enter the characters
1. Enter the letters that are eliminated from your guess (Leave this empty on the first guess)
2. Enter the letters you know are in the word
3. Enter the letters you know and that are in the right position (Enter with spaces where the letters are unknown to function)
4. Enter the letters yoy know are in the word but not in the right position (With the number being the position you know the number is not in)

Once all of these are completed, run the program

The program will print multiple results, the one you should follow for maximum efficiency is the "Valids"
The words are listed by the top n best guesses (n can be changed by changing the "TopBlank" variable

Although it is a Wordle solver, there is a bit of skill in recognizing when the word might contain a repitition
There are repititions if all of the "Valids" sections words are negative
The repition cut off variable is by default set to 5, this number simply tells the amount of letters we know aren't in the word before the program should consider words with repititions. Thus, increasing the value of the cutoff will prevent repititions from being returned, while lowering the value below the amount of eliminated letters will enable them.

# How the program works:

The program uses two basic principles to calculate the best guesses.
1. The more unique vowels that are not eliminated, the better
2. The more common the letters are in the word in English, the better

Using these two principles in combination with the elimination of words and a databank of all English words, the program filters out invalid words and sorts them by there value. Each words value is determined by the frequency of each letter. Every letter (using the "EnglishLetFreq.txt") is given a value. Each word contains five letters and the sum of these values is the words score. If the word has an eliminated letter in it, instead of removing the word entirely, the letter is simply made a massive negative (-1000), this makes it easier to determine where an error could have been made in inputting the correct letters and positions.

Then, using the positional data provided by the player, the system further filters down the list until only a few guess remain. All of these guesses are sorted by value and then are printed. 
