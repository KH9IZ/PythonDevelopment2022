import re
import shlex
import cmd
import readline
from collections import defaultdict

from pynames import LANGUAGE, GENDER
from pynames.utils import get_all_generators

class NamesCmd(cmd.Cmd):
    language = 'native'
    prompt = ">._.>> "
    races = defaultdict(dict)
    for subrace in get_all_generators():
        temp = subrace.__name__.replace("Generator", "")
        temp = temp.replace("Fullname", "")
        temp = temp.replace("Names", "").lower()
        
        races[subrace.__module__.split('.')[2]][temp] = subrace
    

    def do_language(self, lang):
        """Changes default generation language"""
        if lang.lower() not in LANGUAGE.ALL:
            print(f"Usupported language. "
                  f"Languages available: {','.join(l.upper() for l in LANGUAGE.ALL)}")
            return
        self.language = lang.lower()

    def complete_language(self, prefix, s, start_prefix, end_prefix):
        return [l.upper() for l in LANGUAGE.ALL if l.startswith(prefix.lower())]
    
    def do_generate(self, arg):
        """Generates name by given race"""
        args = arg.split()
        try:
            gen = self.get_generator(args)()
        except ValueError as e:
            print(e.args[0])
            return

        gender = 'm'
        if 'female' in args:
            gender = 'f'

        if self.language not in gen.languages:
            print(gen.get_name_simple(gender, 'native'))
        else:
            print(gen.get_name_simple(gender, self.language))


    def complete_generate(self, prefix, s, start_prefix, end_prefix):
        args = s.split()

        if len(args) == 1 or len(args) == 2 and prefix:
            return [race for race in self.races.keys() if race.startswith(prefix)]

        if len(args) == 2 or len(args) == 3 and prefix:
            race = self.races.get(args[1], {})

            return [subrace for subrace in race.keys() if subrace.startswith(prefix)]

        if len(args) == 3 or len(args) == 4 and prefix:
            return [gen for gen in ('male', 'female') if gen.startswith(prefix)]

        return []
    
    def do_info(self, arg):
        """Gives info about generator"""
        args = arg.split()

        try:
            gen = self.get_generator(args)()
        except ValueError as e:
            print(e.args[0])
            return

        show_langs = 'language' in args
        if 'male' in args:
            gender = 'm'
        elif 'female' in args:
            gender = 'f'
        else:
            gender = ['m', 'f']

        if show_langs:
            print(' '.join(gen.languages))
        else:
            print(gen.get_names_number(gender))


    def complete_info(self, prefix, s, start_prefix, end_prefix):
        return self.complete_generate(prefix, s, start_prefix, end_prefix) + ['language'] if 'language'.startswith(prefix) else []

    def get_generator(self, args):
        race = {}
        gen = None
        for arg in args:
            if arg in self.races.keys():
                race = self.races[arg]
            elif t := next((subrace for subrace in race.keys() if subrace.startswith(arg)), False):
                gen = race[t]

        if not race:
            raise ValueError(f"Unknown race{': ' + next(iter(race)) if len(race) > 0 else ''}.")
        if gen is None:
            gen = next(iter(race.values()))
        return gen
    
    def do_eof(self, arg):
        return True
    
    def precmd(self, args):
        return args.lower()


NamesCmd().cmdloop()
