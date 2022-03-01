import textdistance as td
import random


def bullscows(guess: str, secret: str) -> (int, int):
    bulls = td.hamming.similarity(guess, secret)
    cows = td.bag.similarity(quess, secret)
    return (bulls, cows)


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret = random.choice(words)
    b = 0
    cntr = 0
    while (b != len(guess := ask("Введите слово: ", words))):
        cntr += 1
        b, c = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", b, c)
    return cntr

