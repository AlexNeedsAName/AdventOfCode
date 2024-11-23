#!/usr/bin/env python3
import argparse

DEBUG=True
def dbg_print(*args, level=1, **kwargs):
    if DEBUG >= level:
        print(*args, **kwargs)


#card_types = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']

WILD_JOKERS = True
if WILD_JOKERS:
    card_types = ['J','2','3','4','5','6','7','8','9','T','Q','K','A']

def get_counts(hand):
    hand_counts = {}
    for card in hand:
        try:
            hand_counts[card] += 1
        except KeyError:
            hand_counts[card] = 1
    return hand_counts

def n_of_a_kind(hand, n):
    if WILD_JOKERS:
        return wild_n_of_a_kind(hand, n)
    counts = get_counts(hand)
    for count in counts.values():
        if count >= n:
            return True
    return False

def wild_n_of_a_kind(hand, n):
    counts = get_counts(hand)
    try:
        jokers = counts['J']
    except KeyError:
        jokers = 0
    for card,count in counts.items():
        if card == 'J' and len(counts) > 1:
            continue
        if count + jokers >= n:
            return True
    return False

def five_of_a_kind(hand):
    return n_of_a_kind(hand, 5)

def four_of_a_kind(hand):
    return n_of_a_kind(hand, 4)

def full_house(hand):
    counts = get_counts(hand)
    if WILD_JOKERS and 'J' in hand:
        return len(counts) == 3
    return len(counts) == 2

def three_of_a_kind(hand):
    return n_of_a_kind(hand, 3)

def get_pairs(hand):
    counts = get_counts(hand)
    pair_count = 0
    for count in counts.values():
        if count >= 2:
            pair_count += 1
    return pair_count

def two_pair(hand):
    return get_pairs(hand) >= 2

def one_pair(hand):
    if WILD_JOKERS and 'J' in hand:
        return True
    return get_pairs(hand) >= 1

def high_card(hand):
    return max(card_types.index(card) for card in hand) + 2


def part1(input_file):
    with open(input_file, 'r') as file:
        hands = []
        for line in file:
            hand, bid = line.strip().split()
            value = 0
            if five_of_a_kind(hand):
                value = 6
            elif four_of_a_kind(hand):
                value = 5
            elif full_house(hand):
                value = 4
            elif three_of_a_kind(hand):
                value = 3
            elif two_pair(hand):
                value = 2
            elif one_pair(hand):
                value = 1

#            value *= len(card_types) ** 6

            ordering = (value, list(card_types.index(card) for card in hand))
            hands.append((ordering, bid, hand))

        hands.sort()
        hands = hands
        total_winnings = 0
        for i,(value,bid,hand) in enumerate(hands):
            rank = i+1
            try:
                winnings = rank * int(bid)
                total_winnings += winnings
            except:
                pass
            print(rank, value,  bid, hand)

    return total_winnings


def part2(input_file):
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            pass
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    DEBUG = args.verbose

    print(part1(args.filename))
    print(part2(args.filename))

