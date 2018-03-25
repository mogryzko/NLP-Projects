
import sys, json, os

wordDict = {}


def recurse(tree):
    if len(tree) == 3:
        # It is a binary rule.
        recurse(tree[1])
        recurse(tree[2])
    elif len(tree) == 2:
        # It is a unary rule.
        s = tree[1]
        if wordDict[s] < 5:
            tree[1] = unicode('_RARE_')
    return


def replaceWords(tree):
    recurse(tree)
    return tree


def countWords(openCounts):
    # counts word occurances from training file and adds them to a global dictionary
    for l in openCounts:
        words = l.split()
        if words[1] == "UNARYRULE":
            if wordDict.setdefault(words[3], 0):
                wordDict[words[3]] += int(words[0])
            else:
                wordDict[words[3]] = int(words[0])


def main(trainFile, outputFile):
    openCounts = open('cfg.counts', 'r')
    countWords(openCounts) # fill global dictionary
    openCounts.close()
    newFile = open(outputFile, 'w')
    for l in open(trainFile, 'r'):
        t = json.loads(l)
        t_RARE = json.dumps(replaceWords(t))
        newFile.write(t_RARE + '\n')
    newFile.close()


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print "Incorrect number of arguments"
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])