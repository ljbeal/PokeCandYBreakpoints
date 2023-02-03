import click

from levels import EXPGroup

groupmsg = """
Exp group for the pokemon,
as defined on https://bulbapedia.bulbagarden.net/wiki/Experience
"""


@click.command()
@click.option('--group', default='medium', help=groupmsg)
@click.option('--exp', help='Current exp amount')
@click.option('--lvl', help='Current pokemon level')
@click.option('--target', default=100, help='Target level (Default 100)')
@click.option('--verbose', default=False, help='verbose, prints more info if True')
def calculate(group: str,
              exp: int = None,
              lvl: int = None,
              target: int = 100,
              verbose: bool = False):

    if lvl is None and exp is None:
        raise ValueError('please provide a level, or exp value!')

    grp = EXPGroup(group)

    if exp is None:
        exp = grp.get_exp(int(lvl))
    else:
        exp = int(exp)

    if lvl is None:
        lvl = grp.get_lvl(int(exp))
    else:
        lvl = int(lvl)

    print(f'Targeting lvl {target} for a pokemon in group {grp.name} '
          f'with {exp} exp (lvl {lvl}):')

    def exp_to_level(lvl, exp):
        return grp.get_exp(lvl) - exp

    temp_lvl = lvl
    temp_exp = exp
    # next_lvl = exp_to_level(temp_lvl + 1, temp_exp)

    used = {}

    def add_use(item):
        try:
            used[item] += 1
        except KeyError:
            used[item] = 1

    while temp_lvl != int(target):
        next_lvl = exp_to_level(temp_lvl + 1, temp_exp)

        if next_lvl <= 30000:
            temp_exp += 30000

            temp_lvl = grp.get_lvl(temp_exp)

            if verbose:
                print(f'using XL candy, level is now {temp_lvl}')
            add_use('XL Candy')
        else:
            temp_lvl += 1

            if verbose:
                print(f'using rare candy, level is now {temp_lvl}')
            add_use('Rare Candy')

    print(used)
