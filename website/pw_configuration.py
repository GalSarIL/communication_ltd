from flask import flash


def password_check(passwd):
    specialSym = ['$', '@', '#', '%', '!']
    val = True

    if len(passwd) != 10:
        flash('Password length should 10 characters', category='error')
        val = False

    if not any(char.isdigit() for char in passwd):
        flash('Password should have at least one numeral', category='error')
        val = False

    if not any(char.isupper() for char in passwd):
        flash('Password should have at least one uppercase letter', category='error')
        val = False

    if not any(char.islower() for char in passwd):
        flash('Password should have at least one lowercase letter', category='error')
        val = False

    if not any(char in specialSym for char in passwd):
        flash('Password should have at least one of the symbols $@#%!', category='error')
        val = False
    print(val)
    return val
