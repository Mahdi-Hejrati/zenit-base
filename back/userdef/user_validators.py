
def notEmptyValidator(val: str):
    if not val:
        raise ValueError('must not be Empty')
    return val

