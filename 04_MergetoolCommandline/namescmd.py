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
        races[subrace.__module__.split('.')[2]][subrace.__name__] = subrace
    

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
        ...
    
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
        ...
    
    def get_generator(self, args):
        race = {}
        gen = None
        for arg in args:
            if arg in self.races.keys():
                race = self.races[arg]
            elif arg in race.keys():
                gen = race[args]

        if not race:
            raise Exception(f"Unknown race{': ' + race[0] if len(race) > 0 else ''}.")
        if gen is None:
            gen = next(iter(race.values()))
        return gen
    
    def do_eof(self, arg):
        return True
    
    def precmd(self, args):
        return args.lower()


NamesCmd().cmdloop()
