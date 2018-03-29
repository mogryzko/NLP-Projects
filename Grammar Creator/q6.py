# CKY algorithm for vertical markovization
# author: Max Ogryzko mvo2102


import sys, json, os, math, time

binaryCounts = {} # {trigram: count}
unaryCounts = {} # {unigram: count}
symbolCount = {} # {nonterminal: count}
trigrams = {} # {nonterminal: [trigram1,trigram2,...]}
seenWords = [] # [word1, word2, ...]
binarySymbols = [] # [nonterminals seen in binary rules]
unarySymbols = [] # [nonterminals seen in unary rules]


# find trigram probability
def qBinary(X, Y1, Y2):
    prob = binaryCounts[(X,Y1,Y2)]/symbolCount[X]
    return prob

# find unigram probability
def qUnary(X, w):
    prob = unaryCounts[(X,w)]/symbolCount[X]
    return prob


# create tree in json format using back pointers
def createTree(i, j, X, tree, words):
    tree.append(X)
    if i == j:
        tree.append(words[i-1])
    else:
        left = bp[(i, j, X)][0]
        right = bp[(i, j, X)][1]
        tree.append([])
        tree.append([])
        createTree(left[0], left[1], left[2], tree[1], words)
        createTree(right[0], right[1], right[2], tree[2], words)
    return tree

# initialize dynamic programming table
def initializePi(words):
    # fill dictionary with 0's
    for l in range(1, len(words) + 1):
        for i in range(1, len(words) + 2 - l):
            j = i + l - 1
            for X in symbolCount:
                pi[(i, j, X)] = 0

    # initialize base values
    for X in unarySymbols:
        for i in range(1, len(words) + 1):
            if words[i - 1] in seenWords:
                if (X, words[i - 1]) in unaryCounts:
                    pi[(i, i, X)] = qUnary(X, words[i - 1])
            else:
                if (X, '_RARE_') in unaryCounts:
                    pi[(i, i, X)] = qUnary(X, '_RARE_')


# perform CKY algorithm to choose best tree and then return the tree in json format
def CKY(words):
    global pi
    pi = {}
    global bp
    bp = {}
    # Initialize Pi dictionary
    initializePi(words)

    # CYK algorithm
    for l in range(1, len(words)):
        for i in range(1, len(words) + 1 - l):
            j = i+l
            for X in binarySymbols:
                for t in trigrams[X]:
                    if t[0] == X:
                        for s in range(i,j):
                            val = qBinary(t[0], t[1], t[2]) * pi[(i, s, t[1])] * pi[(s + 1, j, t[2])]
                            if pi[(i, j, X)] < val:
                                pi[(i, j, X)] = val
                                bp[(i, j, X)] = ((i, s, t[1]), (s + 1, j, t[2]))

    # return tree:
    tree = []
    if pi[(1,len(words),'S')] != 0: # normal, full tree
        tree = createTree(1,len(words),'S',tree,words)
    else: # max of all X in N
        val = float("-inf")
        symbol = ''
        for X in symbolCount:
            if (1,len(words), X) in pi:
                if val < pi[(1,len(words), X)]:
                    val = pi[(1,len(words), X)]
                    symbol = X
        createTree(1,len(words),symbol,tree,words)
    return tree


# counts symbols, unary and binary rules and adds them to their respective global objects
def fillObjects(openCounts):
    for l in openCounts:
        words = l.split()
        symbol = words[2]
        if words[1] == "NONTERMINAL":
            # count nonterminal symbols (not words)
            symbolCount[symbol] = float(words[0])
        if words[1] == "BINARYRULE":
            # It is a binary rule.
            y1, y2 = (words[3], words[4])
            key = (symbol, y1, y2)
            binaryCounts[key] = float(words[0])
            trigrams.setdefault(symbol, [key])
            trigrams[symbol] += [key]
            if symbol not in binarySymbols:
                binarySymbols.append(symbol)
        elif words[1] == "UNARYRULE":
            # It is a unary rule.
            y1 = words[3]
            if words[3] not in seenWords:
                seenWords.append(words[3])
            key = (symbol, y1)
            unaryCounts[key] = float(words[0])
            if symbol not in unarySymbols:
                unarySymbols.append(symbol)


def main(trainFile, testFile, outputFile):
    openCounts = open('cfg.counts', 'r')
    fillObjects(openCounts) # fill global dictionaries
    openCounts.close()
    output = open(outputFile, 'w')
    for s in open(testFile, 'r'):
        words = s.split()
        tree = CKY(words)
        output.write(json.dumps(tree) + '\n')
    output.close()


if __name__ == "__main__":

    if len(sys.argv) != 4:
        print "Incorrect number of arguments"
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
