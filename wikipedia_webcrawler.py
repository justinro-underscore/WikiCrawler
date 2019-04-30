import re
from web_puller import simple_get
from bs4 import BeautifulSoup

# Constants
wiki_link = "https://en.wikipedia.org"
wiki_connector = "/wiki/"
wiki_help_page = "Help:"
wiki_file_page = "File:"

# Gets the loop once we detect it
def get_loop(pages):
  loop = []
  key = pages.pop()
  pages.reverse()
  for p in pages:
    loop.append(p)
    if p == key:
      loop.reverse()
      return loop

# Goes to the page given by the url
def goto_page(url, pages, verbose):
  # Find the title
  raw_html = simple_get(url)
  try:
    html = BeautifulSoup(raw_html, "html.parser")
  except TypeError:
    raise RuntimeError("Error: Page could not be parsed!")
  title = html.find("h1", attrs={"id": "firstHeading", "class": "firstHeading", "lang": "en"}).text

  # Check if we have found a loop
  if title in pages:
    print("\nLoop detected!")
    print("Loop detected at \"" + title + "\"")
    pages.append(title)
    return
  if verbose:
    print(title)
  else:
    print(".", end='', flush=True)
  pages.append(title)

  # Find all paragraphs in the article
  article = html.find("div", attrs={"class": "mw-parser-output"})
  contents = article.findAll(["p", "ol", "ul"], attrs={"class": ""}, recursive=False)
  # Loop through all paragraphs
  for c in contents:
    c = BeautifulSoup(re.sub(r" \(from[^\)]*\)", "", str(c)), "lxml") # Get rid of etymology
    links = c.findAll("a")
    if links is None:
      raise RuntimeError("Page does not exist!")
    for link in links:
      try:
        href = link["href"]
      except:
        continue
      # Check if link is valid
      # Don't go to:
      #  Link not on wikipedia
      #  Help page
      #  File page
      #  Sublink
      if (wiki_connector in href) and \
          (wiki_help_page not in href) and \
          (wiki_file_page not in href) and \
          ("#" not in href):
        return goto_page(wiki_link + href, pages, verbose)
  # If we have gone through all links and they are all invalid, throw error
  raise RuntimeError("No further links!")

# Runs the crawler from a starting word
def run_crawler(word, verbose=False):
  try:
    # When we return, we have found a loop
    if not verbose:
      print(word)
    pages = []
    goto_page(wiki_link + wiki_connector + word, pages, verbose)
    if not verbose:
      print()
    return get_loop(pages)
  except RuntimeError as e: # We have hit a problem
    print("\n" + str(e))
    print("Here's the list of pages we reached:")
    print(pages)