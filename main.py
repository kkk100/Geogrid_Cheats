import util_functions as uf
from colorama import Fore, Style

def guess_advisor(category1: str, category2: str) -> None:
    correct = uf.get_correct_answers(category1, category2)
    print(Fore.GREEN + "Correct guesses:" + Style.RESET_ALL)
    for i in correct:
        print(i)
    rarest, status = uf.determine_rarest(category1, category2)
    if status == 0:
        print(uf.rainbow("Direct rarest match found:"))
    elif status == 1:
        print(Fore.LIGHTMAGENTA_EX + "Indirect rarest match found!" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Rarest match not found:" + Style.RESET_ALL)
    for i in rarest:
        print(i)
guess_advisor("Flag with black", "More than 20 Olympic medals")