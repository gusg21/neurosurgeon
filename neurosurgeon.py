import pickle, sys, textwrap

def quickwrap(text):
    return "\n".join(textwrap.wrap(text, width=80, initial_indent="", subsequent_indent="\t"))

# print the whole thing nicely. pipe this to a file pls
def n_print_brain(data, _):
    sorted_assocs = sorted(data.items(), key=lambda item: len(item[1]))
    sorted_assocs.reverse()
    for pair in sorted_assocs:
        line = "{" + pair[0] + "} " + str(pair[1])
        print(quickwrap(line))

# words it knows the most associations for. pass a number to cut it off
def n_favorite_words(data, args):
    max_count = 1000000000
    if len(args) > 0:
        max_count = int(args[0])

    sorted_assocs = sorted(data.items(), key=lambda item: len(item[1]))
    sorted_assocs.reverse()
    sorted_assocs = sorted_assocs[:max_count]
    line = ""
    for pair in sorted_assocs:
        line += "{" + pair[0] + "}, "
    print(quickwrap(line))

def n_zapf(data, _):
    sorted_assocs = sorted(data.items(), key=lambda item: len(item[1]))
    sorted_assocs.reverse()
    for pair in sorted_assocs:
        print(pair[0] + ", " + str(len(pair[1])))

# counts words it knows
def n_word_count(data, _):
    print("Known words: " + str(len(data)))

# count words it knows AND words it has seen but knows no associations for
def n_super_word_count(data, _):
    unique_words = []
    sorted_assocs = sorted(data.items(), key=lambda item: len(item[1]))
    sorted_assocs.reverse()

    debug_counter = 0
    has_found_unique = False
    for pair in sorted_assocs:
        if pair[0] not in unique_words:
            unique_words.append(pair[0])
            has_found_unique = True

        for word in pair[1]:
            if word not in unique_words:
                unique_words.append(word)
                has_found_unique = True
            debug_counter += 1
            if debug_counter % 100 == 0:
                if has_found_unique:
                    print("#", end="", flush=True)
                else:
                    print(".", end="", flush=True)
                has_found_unique = False

    print("\n")
    print("Known words (including associateds): " + str(len(unique_words)))

# find the connections for a single word
def n_find_connections(data, args):
    word = args[0]
    connected_to = data[word]
    connected_from = []

    for pair in data.items():
        if word in pair[1]:
            connected_from.append(pair[0])
    
    line = str(connected_from) + ">>> " + word + " <<<" + str(connected_to)

    print(quickwrap(line))

def main():
    func_prefix = "n_"

    if len(sys.argv) < 3:
        print("neurosurgeon {pickled brain file} {function name} [args...]")
        # print available functions
        print("available functions: ")
        funcs = filter(lambda x: x.startswith(func_prefix), globals()) # only n_*
        funcs = [name[len(func_prefix):] for name in funcs] # chop off n_
        print("\t" + ", ".join(funcs)) # display
        return 1

    # load the brain
    data: dict = pickle.load(open(sys.argv[1], "rb"))

    # WILDLY unsafe :^)
    f = globals()[func_prefix + sys.argv[2]] # find func to call
    f(data, sys.argv[3:]) # call with rest of params

    return 0


if __name__ == "__main__":
    sys.exit(main())