import textdistance as td
import random


def bullscows(guess: str, secret: str) -> (int, int):
    bulls = td.hamming.similarity(guess, secret)
    cows = td.bag.similarity(guess, secret)
    return (bulls, cows)


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret = random.choice(words)
    guess = ''
    b = 1
    cntr = 0
    while b != len(secret) or b != len(guess):
        guess = ask("Введите слово: ", words)
        cntr += 1
        b, c = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", b, c)
    return cntr

