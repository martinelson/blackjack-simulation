# Blackjack Simulator

## How to run
1. cd into the file directory
2. run pip install requirements.txt, or ensure your environment has the requirements downloaded
3. execute python main.py
4. The user can edit the following variables to see different results
   1. reshuffle_point: any value between 0 and 1
   2. hit_threshold: can add any value to the list
   3. strategy: integer 1, 2, or 3 corresponding with the different strategies available
   4. split_enabled: True or False
   5. game_reps: Enter the amount of games to simulate

## File Descriptions

### 1. cards.py
- Creates the Cards class
- Initializes a nested list of the card name and value within an entire self.deck list
- Initializes a discard list to put used cards
- shuffle_cards() adds discarded cards back to the deck and shuffles the list via random.shuffle()
- cut() takes the last 60-75 cards of the deck and moves it to the discard
- deal() creates a player and dealer list and adds two cards to each list, removing them from the deck and adding them to self.discard
- hit() takes one card from the deck and returns it

### 2. scoring.py
- get_current_score() sums all the card values in a players hand, adjusting the value if an Ace is in the hand

### 3. games.py
- natural_blackjack() checks if a player or a dealer have a natural blackjack
- compare_score() checks to see who has the highest score and returns the winner, or stand-off if tied
- check_to_split() only called if the basic strategy 3 is used, goes through a checklist to see if a player should split accoring to the strategy
- game() runs the round by finding a final score, initiating splits, calls the right strategy from play.py file, and returning the data of each round 

### 4. play.py
- hit_and_append() gets a new card from the hit() function within the Cards class, it then appends the card to the hand, and updates the score
- soft_play_hand() checks to see if the dealer has a soft 17 (Ace and Six) and hits accordingly as well as until the value of 16 is surpassed
- value_play_hand() calls hit_and_append until a threshold value has been reached
- situation_play_hand() checks if the player has a value greater than or equal to 12 and if the dealer's face-up card is worth more than or equal to 2 and less than or equal to 5. If so, the player stands, if not, the player hits
- basic_play_hand() follows a common strategy by standing, hitting, or doubling down when specific scenarios are met.

### 5. iterate.py
- rounds() loops through as many game rounds the user dictates, returning the result from the game() function and adding it to a dataframe through the record() function in record.py. Also checks if the reshuffle point has been reached, and if so, calls the shuffle_cards() function of the Cards class, and calls cut() from the class as well. 

### 6. record.py
- new_file() creates a file if not created, if it is created, it clears the contents
- append_file() adds a line to an already existing .txt file
- record() adds a new row onto a pandas dataframe

### 7. analysis.py
- batch_means() takes a dataframe of game records, splits the dataframe into batches and analyzes the confidence interval range of the mean player_return

### 8. main.py
- Creates the path to record the results of the batch_means() analysis and calls the new_file() function to carry out the function
- establishes baseline adjustable variables resuffle_point, hit_threshold, strategy, split_enabled
- for each value threshold specified in hit_threshold, a new deck instance is created from the Cards class and the deck is cut. The game_reps value is created to establish how many games will be in each simulation run. The columns for the dataframe are established and an empty result dataframe is created. The round() function is called and the results are saved to a csv file, batch_means() is then called and the result is appended to the text file created from new_file()
