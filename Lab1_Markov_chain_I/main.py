from collections import Counter, OrderedDict
import random

letters = Counter(' abcdefghijklmnopqrstuvwxyz')


def create_random_text(n, probabilities):
    return random.choices(tuple(probabilities), weights=probabilities.values(), k=n)


def average_length(text):
    words = text.split(' ')
    return sum(map(len, words)) / len(words)


def create_ngrams(text, n=1):
    ngrams = Counter(text[i:i + n] for i in range(len(text) - n + 1))
    return OrderedDict(sorted(normalize_probabilities(ngrams).items()))


def normalize_probabilities(probabilities):
    total = sum(probabilities.values())
    for key in probabilities:
        probabilities[key] /= total
    return probabilities


def get_conditional_probabilities(text, n):
    conditional_probabilities = {}
    ngrams = create_ngrams(text, n)
    next_ngrams = create_ngrams(text, n + 1)

    for ngram in ngrams:
        conditional_probabilities[ngram] = {}

        for letter in letters:
            new_key = ngram + letter

            if new_key in next_ngrams:
                conditional_probabilities[ngram][letter] = next_ngrams[new_key] / ngrams[ngram]
        normalize_probabilities(conditional_probabilities[ngram])

    return conditional_probabilities


def create_markov(n, degree, start, probabilities):
    result = start
    while len(result) < n and (ngram := result[-degree:]):
        if ngram not in probabilities:
            [generated] = create_random_text(1, letters)
        else:
            [generated] = create_random_text(1, probabilities[ngram])

        result += generated

    return result


# Zad 1


print("Zad. 1")
random_text = ''
random_text = random_text.join(create_random_text(1000, letters))
print("Random text: ", random_text)
print("Average word length:", average_length(random_text))

# Zad 2


f = open("norm_hamlet.txt")
text = f.read()

print("\nZad. 2")
print(create_ngrams(text, 1))

# Zad 3


print("\nZad. 3")
probabilities = create_ngrams(text, 1)
first_order_approximation = ''
first_order_approximation = first_order_approximation.join(create_random_text(1000, probabilities))
print("Random text: ", first_order_approximation)
print("Random sentence with probabilities average word length: ", average_length(first_order_approximation))

# Zad 4


print("\nZad. 4")
most_common = Counter(text).most_common(2)
print("Most common signs: ", most_common)

conditional_probabilities = get_conditional_probabilities(text, 1)
for (letter, _) in most_common:
    print("Probability of occurrence of particular characters after: \"", letter, "\"\n", conditional_probabilities[letter], sep='', end='\n\n')

# Zad 5


print("\nZad. 5")
for i in range(1, 6):
  if i % 2 == 0:
      continue

  print(i, "degree")

  probabilities = get_conditional_probabilities(text, i)
  n_degree_text = create_markov(1000, i, "probability", probabilities)

  print("Text: ", n_degree_text)
  print("Average word length: ", average_length(n_degree_text), end='\n\n')