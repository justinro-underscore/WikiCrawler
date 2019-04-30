import sys
from collections import Counter
from wikipedia_webcrawler import run_crawler

loops = []

test_words = {
  "Cup": None,
  "Backpack": None,
  "Blackboard": None,
  "Boeing_747": None,
  "Fire": None,
  "Arkansas": None,
  "Brownback": None,
  "Evil": None,
  "Chair": None,
  "Recliner": None,
  "Unity": None,
  "Master": None,
  "Exit": None,
}

def get_index(target, list_of_arrs):
  for i in range(len(list_of_arrs)):
    if target[0] in list_of_arrs[i]:
      return i
  return -1

def wikipedia_tests():
  for word, _ in test_words.items():
    loop = run_crawler(word)
    if all(Counter(loop) != Counter(l) for l in loops):
    # if loop not in loops:
      test_words[word] = len(loops)
      loops.append(loop)
    else:
      test_words[word] = get_index(loop, loops)
      # test_words[word] = loops.index(loop)
    print(loop)
    print(word + ": " + str(test_words[word]))
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
  print("Loops:")
  for i in range(len(loops)):
    print(str(i) + " : " + str(loops[i]))
  print()
  print("Results:")
  for word, index in test_words.items():
    print(str(word) + " : " + str(index))
  print()

def start_search(word, verbose=False):
  run_crawler(word, verbose)

if __name__ == "__main__":
  if len(sys.argv) > 1:
    if len(sys.argv) > 2:
      start_search(sys.argv[1], sys.argv[2] != "0")
    else:
      start_search(sys.argv[1])
  else:
    wikipedia_tests()
    # print("Execution should be:")
    # print("\"python wikipedia_tests.py [starting word]\"")