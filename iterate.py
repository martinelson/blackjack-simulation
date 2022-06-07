from games import game
from record import record


def rounds(game_reps, deck, threshold, df, cols, reshuffle_point, strategy, split_enabled):

    while game_reps > 0:
        if split_enabled:
            result = game(deck, threshold, strategy, split_enabled=True)
            df = record(result, df, cols)
        else:
            result = game(deck, threshold, strategy)
            df = record(result, df, cols)
        if len(deck.discard) / len(deck.deck) >= reshuffle_point:
            deck.shuffle_cards()
            deck.cut()
        game_reps -= 1
    return df
