import pandas as pd
from cards import Cards
from iterate import rounds
from record import new_file
from record import append_file
from analysis import batch_means

# Path to return results
path_val = 'results/value.txt'
# Creating files, or removing previous content, if created
new_file(path_val)
# Can change to any value from 0 to 1.0
reshuffle_point = 0.50
# Can add any value to this list
hit_threshold = [16]
# value strategy = 1, situation split strategy = 2, basic comprehensive = 3
strategy = 3
# Can change the split to False or True
split_enabled = True

for threshold in hit_threshold:
    # Creating deck of cards, the amount of reps, and initializing dataframe for each value strategy
    deck = Cards()
    deck.cut()
    # Change the amount of games played here
    game_reps = 150000
    data_cols = ['Winner', 'Dealer_Score', 'Dealer_Top_Card', 'Player_Score', 'Player_1', 'Player_2', 'Player_Return']
    results_df = pd.DataFrame(columns=data_cols)

    # For each value strategy, performing game
    results_df = rounds(game_reps, deck, threshold, results_df, data_cols, reshuffle_point, strategy, split_enabled)

    # Saving results to respective csv game log
    results_df.to_csv(f'results/games/value/strat_{threshold}.csv', index=False)

    # Saving batch means results to respective csv log
    result_txt_val = batch_means(results_df, threshold, f'results/batches/value/batch_{threshold}.csv')

    print(result_txt_val)
    # Writing out results to txt files created
    append_file(path_val, result_txt_val)

if __name__ == '__main__':
    print('PyCharm')
