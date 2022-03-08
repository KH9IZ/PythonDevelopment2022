import shlex
import cmd
import readline
from collections import defaultdict

from pynames import LANGUAGE, GENDER
from pynames.utils import get_all_generators

class NamesCmd(cmd.Cmd):
    language = 'native'
    promt = ">._.>>"
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
    def do_eof(self, arg):
        print('QQ')
        return 1
    
    def do_generate(self, arg):
        """Generates name by given race"""
        race, *args = arg.split()
        if type(race) is str: race = race.lower()
        arg1 = args[0] if len(args) > 0 else None
        arg2 = args[1] if len(args) > 1 else None
        if type(arg1) is str: arg1 = arg1.lower()
        if type(arg2) is str: arg2 = arg2.lower()
        if arg1 in GENDER.ALL:
            gender = arg1
            subrace = arg2
        elif arg2 in GENDER.ALL:
            subrace = arg1
            gender = arg2
        elif arg2 is not None:
            print("Unknown gender.")
            return
        else:
            subrace = None
            gender = None

        if race not in self.races.keys():
            print(f"Unknown race '{race}'.")
            return
        subraces = self.races[race]
        if subrace is None:
            Gen = next(iter(subraces.values()))
        elif subrace not in subraces.keys():
            print("Unknonw subrace.")
            return
        else:
            Gen = subraces[subrace]
    
        if gender == 'male' or gender is None:
            gender = 'm'
        elif gender == 'f':
            gender = 'f'
        else:
            print("Unknown gender. (there is only two genders!)")
            return
       

        gen = Gen()
        try:
            print(gen.get_name_simple(gender, self.language))
        except KeyError:
            print(gen.get_name_simple(gender, 'native'))
        

    def complete_generate(self, prefix, s, start_prefix, end_prefix):
        ...
    
    def do_info(self, arg):
        """Gives info about generator"""
        race, *args = arg.split()
        

        show_langs = False
        gender = ['m', 'f']
        subrace = None
        for arg in args:
            arg = arg.lower()
            if arg == 'language':
                show_langs = True
            elif arg in ('male', 'female'):
                gender = arg[0]
            else:
                subrace = arg

        race = race.lower()
        if race not in self.races.keys():
            print(f"Unknown race {race}")
            return
        race = self.races[race]


        if subrace is None:
            Gen = next(iter(race.values()))
        else:
            if subrace not in race.keys():
                print(f"Unknown subrace {subrace}")
                return
            Gen = race[subrace]

        gen = Gen()
        if show_langs:
            print(' '.join(gen.languages))
        else:
            print(gen.get_names_number(gender))


    def complete_info(self, prefix, s, start_prefix, end_prefix):
        ...
    
    



NamesCmd().cmdloop()
