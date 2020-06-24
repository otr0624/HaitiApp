import random
from datetime import date


def rand_id(length=6):
    char_set = "ABCDEFGHJKLMNPQRTUVWXYZ2346789"  # removes lookalikes I/1, O/0, 5/S
    return ''.join((random.choice(char_set) for i in range(length)))

#  Once ID database implemented, add "if not in database" logic to enforce unique value


def calculate_age(born):
    if born:
        today = date.today()
        age_in_years = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        age_in_months = (today.month - born.month - (today.day < born.day)) % 12
        if age_in_years >= 2:
            return str(age_in_years) + " years"
        else:
            return str(age_in_months) + " months"
    else:
        return "Unknown"
