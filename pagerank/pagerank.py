import os
import pdb
import re
import sys

import numpy as np

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    dist = dict()
    for next_page in corpus.keys():
        if next_page in corpus[page]:
            dist[next_page] = damping_factor / len(corpus[page]) + (1 - damping_factor) / len(corpus)

        else:
            dist[next_page] = (1 - damping_factor) / len(corpus)

    return dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    sample_corpus = {_page: (_pages if len(corpus[_page]) > 0 else corpus.keys()) for _page, _pages in corpus.items()}

    amounts = dict()

    for page in sample_corpus.keys():
        amounts[page] = 0

    actual_page = np.random.choice(list(sample_corpus.keys()))

    for i in range(n):
        amounts[actual_page] += 1
        actual_page = np.random.choice(list(sample_corpus.keys()), p=list(transition_model(sample_corpus, actual_page, damping_factor).values()))

    dist = {_page: (_amt / n) for _page, _amt in amounts.items()}
    return dist

# Function to compute new pageRank on iterative approach


def new_pr_iter(corpus, dist_dict, page, damping_factor):
    new_pr = (1 - damping_factor) / len(corpus)
    for link in corpus[page]:
        new_pr += damping_factor * dist_dict[link] / len(corpus[link])

    return new_pr

# Function that detects if iterative approach is not changing pageRanks (in more than 0.001)


def no_change(corpus, dist_dict, damping_factor):
    for _page in corpus:

        new_pr = new_pr_iter(corpus, dist_dict, _page, damping_factor)

        if abs(new_pr - dist_dict[_page]) >= 0.001:
            return False

    return True


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    iter_corpus = {_page: (_pages if len(corpus[_page]) > 0 else corpus.keys()) for _page, _pages in corpus.items()}

    dist = {_page: 1 / len(iter_corpus) for _page in iter_corpus}

    actual_page = np.random.choice(list(corpus.keys()))

    while not no_change(iter_corpus, dist, damping_factor):
        new_pr = new_pr_iter(iter_corpus, dist, actual_page, damping_factor)
        dist[actual_page] = new_pr
        actual_page = np.random.choice(list(iter_corpus.keys()),
                                       p=list(transition_model(iter_corpus, actual_page, damping_factor).values()))
    return dist


if __name__ == "__main__":
    main()
