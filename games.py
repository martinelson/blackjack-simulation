from play import value_play_hand, situation_play_hand, basic_play_hand, soft_play_hand
from scoring import get_current_score

# Dealer has to stay if value of cards are 17 or higher so dealer threshold is unchanged.
DEALER_THRESHOLD = 16


def natural_blackjack(player_score, dealer_score):
    if player_score == 21 and dealer_score != 21:
        return "Player", 1.5
    if dealer_score == 21 and player_score != 21:
        return "Dealer", -1
    if player_score == 21 and dealer_score == 21:
        return "Stand-Off", 0
    return "None", 0


def compare_score(player_score, dealer_score):
    winner = "Stand-Off"
    player_return = 0
    if player_score > dealer_score:
        winner = "Player"
        player_return = 1
    if player_score < dealer_score:
        if dealer_score > 21:
            winner = "Player"
            player_return = 1
        else:
            winner = "Dealer"
            player_return = -1
    return winner, player_return


def check_to_split(player_card, dealer_card):
    player_val = player_card[1]
    dealer_val = dealer_card[1]
    dealer_name = dealer_card[0]
    if player_val == 10 or player_val == 5:
        return False
    if (dealer_val >= 8 or "Ace" in dealer_name) and player_val <= 7:
        return False
    if player_val == 4 and (dealer_val <= 4 or dealer_val == 7):
        return False
    if player_val == 9 and (dealer_val == 7 or dealer_val == 10 or "Ace" in dealer_name):
        return False
    if player_val == 6 and dealer_val == 7:
        return False
    return True


def game(cards, threshold, strategy, split_enabled=False):
    # Dealing cards from Card class
    player_hand, dealer_hand = cards.deal()
    # Calculating scores
    player_hand, player_score = get_current_score(player_hand)
    dealer_hand, dealer_score = get_current_score(dealer_hand)
    # Getting player's initial cards and dealer's face up card
    player_1_card = player_hand[0]
    player_2_card = player_hand[1]
    dealer_top_card = dealer_hand[0]
    # Double down not available until strategy 3
    double_down = False

    # Checking for Natural Blackjacks
    natural_result, player_return = natural_blackjack(player_score, dealer_score)
    if natural_result != "None":
        return [natural_result, dealer_score, dealer_top_card, player_score, player_1_card, player_2_card,
                player_return]

    # Testing split hand strategy for the player
    if split_enabled:
        # Cards are within a nested list [[CARD NAME, CARD VALUE], [CARD NAME, CARD VALUE]]
        # Checking for pairs to split
        if player_hand[0][0].split(' ')[0] == player_hand[1][0].split(' ')[0]:
            split_hand = True
            # Testing if player should actually split while performing basic strategy
            if strategy == 3:
                split_hand = check_to_split(player_1_card, dealer_top_card)

            if split_hand:
                left_player_hand = [player_1_card]
                right_player_hand = [player_2_card]
                left_player_hand, left_player_score = get_current_score(left_player_hand)
                right_player_hand, right_player_score = get_current_score(right_player_hand)
                # Double down not available until strategy 3
                l_double_down = False
                r_double_down = False
                if strategy == 2:
                    final_left_score = situation_play_hand(left_player_hand, left_player_score, cards, threshold,
                                                           dealer_top_card)
                    final_right_score = situation_play_hand(right_player_hand, right_player_score, cards, threshold,
                                                            dealer_top_card)
                    final_dealer_score = value_play_hand(dealer_hand, dealer_score, cards, DEALER_THRESHOLD)

                else:
                    final_left_score, l_double_down = basic_play_hand(left_player_hand, left_player_score, cards,
                                                                      threshold, dealer_top_card, already_split=True)
                    final_right_score, r_double_down = basic_play_hand(right_player_hand, right_player_score, cards,
                                                                       threshold, dealer_top_card, already_split=True)
                    final_dealer_score = soft_play_hand(dealer_hand, dealer_score, cards, DEALER_THRESHOLD)

                # left hand results
                if final_left_score > 21:
                    l_winner = "Dealer"
                    l_return = -1
                else:
                    l_winner, l_return = compare_score(final_left_score, final_dealer_score)

                # right hand results
                if final_right_score > 21:
                    r_winner = "Dealer"
                    r_return = -1
                else:
                    r_winner, r_return = compare_score(final_right_score, final_dealer_score)

                # If double down was taken, bet multiplied by 2
                if l_double_down:
                    l_return *= 2
                if r_double_down:
                    r_return *= 2

                # combining results
                split_result = [f'{l_winner} / {r_winner}', final_dealer_score, dealer_top_card,
                                [final_left_score, final_right_score], player_1_card, player_2_card, l_return+r_return]
                return split_result

    # Playing out hands for the player and dealer
    # Player goes first
    if strategy == 1:
        final_player_score = value_play_hand(player_hand, player_score, cards, threshold)
    elif strategy == 2:
        final_player_score = situation_play_hand(player_hand, player_score, cards, threshold, dealer_top_card)
    else:
        final_player_score, double_down = basic_play_hand(player_hand, player_score, cards, threshold, dealer_top_card)

    # Ending round if player busts
    if final_player_score > 21:
        if double_down:
            player_return = -2
        else:
            player_return = -1
        return ["Dealer", dealer_score, dealer_top_card, final_player_score, player_1_card, player_2_card,
                player_return]

    # Dealer takes their turn
    if strategy == 3:
        final_dealer_score = soft_play_hand(dealer_hand, dealer_score, cards, DEALER_THRESHOLD)
    else:
        final_dealer_score = value_play_hand(dealer_hand, dealer_score, cards, DEALER_THRESHOLD)

    # Determining winner of the hand
    winner, player_return = compare_score(final_player_score, final_dealer_score)
    if double_down:
        player_return *= 2
    return [winner, final_dealer_score, dealer_top_card, final_player_score, player_1_card, player_2_card,
            player_return]
