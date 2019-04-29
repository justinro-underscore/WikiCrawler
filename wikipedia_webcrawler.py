import sys
from web_puller import simple_get
from bs4 import BeautifulSoup

# Constants
wiki_link = "https://en.wikipedia.org"
wiki_connector = "/wiki/"
wiki_help_page = "Help:"
wiki_file_page = "File:"

# Holds the titles of all the pages we have traversed
pages = []

# Gets the loop once we detect it
def get_loop():
  loop = []
  key = pages.pop()
  pages.reverse()
  for p in pages:
    loop.append(p)
    if p == key:
      loop.reverse()
      return loop

# Gets the first links from a list of paragraphs
def get_links_from_p(list_of_p):
  for p in list_of_p:
    if len(p.select("a")) > 0:
      return p.select("a")

# Goes to the page given by the url
def goto_page(url):
  # Find the title
  raw_html = simple_get(url)
  html = BeautifulSoup(raw_html, "html.parser")
  title = html.find("h1", attrs={"id": "firstHeading", "class": "firstHeading", "lang": "en"}).text

  # Check if we have found a loop
  if title in pages:
    print("\nLoop detected!")
    print("Loop detected at \"" + title + "\"\n")
    pages.append(title)
    return
  print(title)
  pages.append(title)

  # Find the next page to go to
  article = html.find("div", attrs={"class": "mw-parser-output"})
  links = get_links_from_p(article.findAll("p", attrs={"class": ""}))
  for link in links:
    href = link["href"]
    # Check if link is valid
    if (wiki_connector in href) and \
        (wiki_help_page not in href) and \
        (wiki_file_page not in href):
      return goto_page(wiki_link + href)
  # If we have gone through all links and they are all invalid, throw error
  raise RuntimeError("No further links!")

if __name__ == "__main__":
  if len(sys.argv) > 1:
    try:
      # When we return, we have found a loop
      goto_page(wiki_link + wiki_connector + sys.argv[1])
      print(get_loop())
    except RuntimeError as e: # We have hit a problem
      print("\n" + str(e))
      print("Here's the list of pages we reached:")
      print(pages)
  else:
    print("Please provide object to search for (Usually must be capitalized)")