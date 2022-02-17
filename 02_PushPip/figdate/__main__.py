from figdate import date
import sys
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU')

print(date(*sys.argv[1:]))
