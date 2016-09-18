# Lex namespace identifiers - alphanumeric, and can't start with a digit.
def lex_namespace(word):
    if word.isalnum():
        if word[0].isdigit():
            print('NAME ERROR: name begins with digit')
            exit(0)
        else:
            return True
    else:
        print('NAME ERROR: unknown input after .n instruction')
        return False

# Lookup if an identifer name exists in TAPE.NAMES
def try_lookup(word, names):
    if word in names:
        return True

# Lookup the value of a known identifier name.
def lookup_by_name(name, lookup):
    for i in lookup:
        if name in i:
            value = i[name]
            return value