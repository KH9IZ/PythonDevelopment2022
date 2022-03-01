import textdistance as td


def bullscows(guess: str, secret: str) -> (int, int):
    bulls = td.hamming.similarity(guess, secret)
    cows = td.bag.similarity(quess, secret)
    return (bulls, cows)
