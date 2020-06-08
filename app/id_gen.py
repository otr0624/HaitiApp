import random


def rand_id(length=6):
    char_set = "ABCDEFGHJKLMNPQRTUVWXYZ2346789"  # removes lookalikes I/1, O/0, 5/S
    return ''.join((random.choice(char_set) for i in range(length)))

#  Once ID database implemented, add "if not in database" logic to enforce unique value
