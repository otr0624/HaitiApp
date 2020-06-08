import random


def rand_id(length=6):
    char_set = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # removes I, O, 1, 0
    return ''.join((random.choice(char_set) for i in range(length)))

#  Once ID database implemented, add "if not in database" logic to enforce unique value
