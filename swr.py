"""Implement Star Wars the roleplaying game's Dice explosion system"""
import random
import matplotlib.pyplot as plt
import numpy as np

def roll_wild():
    """Roll a single wild die

    OUTPUTS
        list[int] (All the results rolled in order)"""
    roll = random.randint(1, 6)
    if roll == 1:
        return [1]
    if roll == 6:
        rec = roll_wild()
        return [6] + rec
    return [roll]


def swr(dice, pips=0, wild_crit_fail_flag=True):
    """Roll with swrpg rules

    INPUTS
        int dice: number of dice
        int pips=0: pip points on top
        wild_crit_fail_flag=True: Does a 1 on the wild die crit-fail?"""

    # The Wild die
    wild_rolls = roll_wild()
    # all other die
    other_die_rolls = [random.randint(1, 6) for i in range(1, dice)]
    combined_rolls = other_die_rolls + wild_rolls

    removed_rolls = []
    # crit fail
    if wild_crit_fail_flag and wild_rolls[-1] == 1:
        removed_rolls.append(1)
        combined_rolls.remove(1)
        # if there are still other dice left
        if combined_rolls:
            removed_rolls.append(max(combined_rolls))
            combined_rolls.remove(max(combined_rolls))

    return (sum(combined_rolls) + pips,
            other_die_rolls,
            wild_rolls,
            pips)

def analysis(dice, wild_crit_fail_flag, repeats):
    """Plot Graphs of the relevant swrs"""
    # raw values
    results = [swr(dice, wild_crit_fail_flag=wild_crit_fail_flag)[0] for i in range(repeats)]
    res_weighted = [(x, sum(1 for el in results if el == x)) for x in set(results)]
    expected = sum(val * weight for val, weight in res_weighted) / repeats
    # clear the top 2nd percentile for plotting (Data is extremely right-skewed)
    summed_right_tail = 0
    for i in range(len(res_weighted) - 1, -1, -1):
        summed_right_tail += res_weighted[i][1]
        if summed_right_tail >= repeats * 0.01:
            stop_at = i
            break
    # print(f"stop_at = {stop_at}")
    # print([el for val, weight in res_weighted[:stop_at] for el in [val] * weight])
    return (np.histogram(
        [el for val, weight in res_weighted[:stop_at] for el in [val] * weight],
        [el - 0.5 for el in range(res_weighted[stop_at][0] + 1)],
        density=True),
            expected,
            [1 + el for el in range(0, res_weighted[stop_at][0]) if el % 2 == 0])

def full_analysis(max_dice, wild_crit_fail_flag, repeats):
    """Full Analysis with plotting"""
    if wild_crit_fail_flag:
        for dice in range(1, max_dice + 1):
            plt.subplot(2, int(np.ceil(max_dice / 2)), dice)
            res, ev, xticks = analysis(dice, True, repeats)
            plt.stairs(*res)
            plt.title(f"{dice}D w Crit-1 E={ev}")
            plt.xticks(xticks, rotation=90)
    else:
        for dice in range(1, max_dice + 1):
            plt.subplot(2, int(np.ceil(max_dice / 2)), dice)
            res, ev, xticks = analysis(dice, False, repeats)
            plt.stairs(*res)
            plt.title(f"{dice}D w/o Crit-1 E={ev}")
            plt.xticks(xticks, rotation=90)
    plt.show()

def beautify_swr_output(total, other, wild, pips):
    if wild:
        print(f"The wild dice rolled {', '.join((str(el) for el in wild))}.")
    if other:
        print(f"The other dice rolled {', '.join((str(el) for el in other))}.\n")
    if pips:
        print(f"Added +{pips} pips.")
    print(f"Total without crit-1= **{sum(other) + sum(wild) + pips}**.")
    print(f"Total with crit-1= **{total}**.")
    return

print("SWRPG Dice Toolkit.")
print("Format: d+p where d=Number of Dice, p=Pips\n"
      "     OR d where d=Number of Dice")
while True:
    inp = input(">>>")
    inp = inp.replace(" ", "")
    if not "+" in inp:
        try:
            beautify_swr_output(*swr(int(inp)))
            continue
        except:
            print("Unrecognized format. no +, value is not an int")
            continue

    # + in format
    inp = inp.split("+")
    if not len(inp) == 2:
        print("Unrecognized format.")
        continue
    # there are dice and pips present
    if inp[0] and inp[1]:
        try:
            beautify_swr_output(*swr(int(inp[0]), int(inp[1])))
            continue
        except:
            raise
            print("Unrecognized format.")
            continue
    if inp[0] and not inp[1]:
        try:
            beautify_swr_output(*swr(int(inp[0])))
            continue
        except:
            raise
            print("Unrecognized format.")
            continue
    if not inp[0] and inp[1]:
        try:
            print(f"No Dice. Total={int(inp[1])}")
            continue
        except:
            print("Unrecognized format.")
            continue
    if not inp[0] and not inp[1]:
        print("Unrecognized format.")
        continue
