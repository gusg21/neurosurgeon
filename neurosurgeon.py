import pickle, sys, textwrap

def quickwrap(text):
    return "\n".join(textwrap.wrap(text, width=80, initial_indent="", subsequent_indent="\t"))

def print_brain(data, args):
    sorted_assocs = sorted(data.items(), key=lambda item: len(item[1]))
    sorted_assocs.reverse()
    for pair in sorted_assocs:
        line = "{" + pair[0] + "} " + str(pair[1])
        print(quickwrap(line))

def find_connections(data, args):
    word = args[0]
    connected_to = data[word]
    connected_from = []

    for pair in data.items():
        if word in pair[1]:
            connected_from.append(pair[0])
    
    line = str(connected_from) + ">>> " + word + " <<<" + str(connected_to)

    print(quickwrap(line))

def main():
    if len(sys.argv) < 3:
        print("neurosurgeon {pickled brain file} {function name} [args...]")
        return 1

    data: dict = pickle.load(open(sys.argv[1], "rb"))

    f = globals()[sys.argv[2]] # find func to call
    f(data, sys.argv[3:]) # call with rest of params

    return 0


if __name__ == "__main__":
    sys.exit(main())