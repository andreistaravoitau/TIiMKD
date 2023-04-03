from collections import Counter
import random


def generate_random_words(probabilities):
    return random.choices(tuple(probabilities), weights=probabilities.values())


def create_ngrams(text, n):
    words = text.split(' ')

    if n == 0:
        return normalize_probabilities(Counter(words))

    ngrams = Counter(tuple(words[i:i + n]) for i in range(len(words) - n + 1))

    return normalize_probabilities(ngrams)


def normalize_probabilities(probabilities):
    total = sum(probabilities.values())

    for key in probabilities:
        probabilities[key] /= total

    return probabilities


def get_conditional_probabilities(text, n):
    conditional_probabilities = {}
    ngrams = create_ngrams(text, n)
    next_ngrams = create_ngrams(text, n + 1)

    for ngram in next_ngrams:
        conditional_probabilities[ngram] = {}
        main = ngram[:n]
        last = ngram[-1]

        if main not in conditional_probabilities:
            conditional_probabilities[main] = {}

        conditional_probabilities[main][last] = next_ngrams[ngram] / ngrams[main]

    for ngram in conditional_probabilities:
        normalize_probabilities(conditional_probabilities[ngram])

    return conditional_probabilities


def create_markov(text, n, k, start=None):
    if start==None:
        ngram = generate_random_words(create_ngrams(text, 0))
    else:
        ngram = start

    for degree in range(1, n):
        ngram.extend(generate_random_words(get_conditional_probabilities(text, degree)[tuple(ngram)]))

    probabilities = get_conditional_probabilities(text, n)

    result = ngram.copy()

    for i in range(k-n):
        result.extend(generate_random_words(probabilities[tuple(ngram)]))
        ngram = (*ngram[1:], result[-1])

    return ' '.join(result)


f = open("norm_wiki_sample.txt")
text = f.read()

print("Zad. 3")
print("1st degree:")

print(create_markov(text, 1, 100))

print("\n2nd degree:")
print(create_markov(text, 2, 100))

print("\n2nd degree starting with \"probability\":")
print(create_markov(text, 2, 100, ["probability"]))
