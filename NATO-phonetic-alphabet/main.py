import pandas

# Read the csv file and convert to dict as per our format
data = pandas.read_csv("nato_phonetic_alphabet.csv")
data_dict = {row.letter: row.code for (index, row) in data.iterrows()}

# Take a word as input from the user and convert to phonetic code.
# In case of non-letters, exception will be generated and user will be
# asked to input the word again.

is_correct = False
while not is_correct:
    try:
        word = input("Enter a word to be converted to phonetic code: ").upper()
        result = [data_dict[letters] for letters in word]
    except KeyError:
        print("Sorry, only letters in the alphabet please.")
        pass
    else:
        print(result)
        is_correct = True
