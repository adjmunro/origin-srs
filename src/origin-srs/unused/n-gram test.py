def map_ngram(s):
    d = dict()
    for i in range(len(s)):
        key = s[i:i + 2]

        if key not in d:
            d[key] = 0

        d[key] += 1

    return d


def ngram(a, b):
    d = map_ngram(a.lower())
    correct = 0
    incorrect = 0

    total = sum(d.values())
    print("Total:", total)

    for i in range(len(b)):
        key = b[i:i + 2].lower()

        if key in d and d[key] > 0:
            #            print(key, d[key])
            d[key] -= 1
            correct += 1
        else:
            incorrect += 1
            print(key)  # can use incorrect(red) or leftover(green) bigrams to locate errors

    incorrect += sum(d.values())
    # correct / total seems to be most accurate measure (but you lose two points for each incorrect character)
    print(f"Correct: {correct}/{total} ({correct / total * 100}%)")
    print(f"Incorrect: {incorrect}/{total} ({incorrect / total * 100}%)")

    if incorrect > 0:
        print(f"Ratio: {correct / incorrect}")


if __name__ == "__main__":
    userIn = input("Attempt to match string: ")
    while (userIn != ""):
        ngram("hello world", userIn)
        userIn = input("\nAttempt to match string: ")
