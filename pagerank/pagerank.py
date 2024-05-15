import os
import random
import re
import sys

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
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Get the number of pages in the corpus
    N = len(corpus)

    # Initialize the probabilities dictionary with each page set to 0
    probabilities = dict.fromkeys(corpus.keys(), 0)

    # Check if the current page has outgoing links
    if corpus[page]:
        # Get the list of linked pages from the current page
        linked_pages = corpus[page]
        # Count the number of linked pages
        num_links = len(linked_pages)
        # Update probabilities for each page
        for p in probabilities:
            # Assign a base probability to all pages
            probabilities[p] = (1 - damping_factor) / N
            # Add the transition probability for linked pages
            if p in linked_pages:
                probabilities[p] += damping_factor / num_links
    else:
        # If the current page has no outgoing links, distribute the probability equally among all pages
        for p in probabilities:
            probabilities[p] = 1 / N

    # Return the dictionary of probabilities
    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize the PageRank dictionary. Each page starts with a PageRank of 0.
    page_rank = dict.fromkeys(corpus.keys(), 0)

    # Get a list of all pages in the corpus.
    pages = list(corpus.keys())

    # Choose a random starting page from the list of pages.
    current_page = random.choice(pages)

    # Perform n samples to estimate the PageRank.
    for _ in range(n):
        # Increase the count for the current page, indicating it was visited.
        page_rank[current_page] += 1

        # Get the transition model for the current page, which gives the probability distribution of the next page.
        next_page_distribution = transition_model(corpus, current_page, damping_factor)

        # Choose the next page based on the transition model probabilities.
        next_page = random.choices(
            list(next_page_distribution.keys()),
            weights=next_page_distribution.values(),
            k=1,
        )[0]

        # Move to the next page.
        current_page = next_page

    # Convert the counts to probabilities by dividing by the total number of samples (n).
    for page in page_rank:
        page_rank[page] /= n

    # Return the dictionary containing the PageRank values.
    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    page_rank = dict.fromkeys(corpus.keys(), 1 / N)
    new_page_rank = dict.fromkeys(corpus.keys(), 0)
    converged = False

    while not converged:
        converged = True

        for page in corpus:
            rank_sum = 0
            for possible_page in corpus:
                if page in corpus[possible_page]:
                    rank_sum += page_rank[possible_page] / len(corpus[possible_page])
                if not corpus[possible_page]:
                    rank_sum += page_rank[possible_page] / N
            new_page_rank[page] = (1 - damping_factor) / N + damping_factor * rank_sum

        for page in page_rank:
            if abs(new_page_rank[page] - page_rank[page]) > 0.001:
                converged = False
            page_rank[page] = new_page_rank[page]

    return page_rank


if __name__ == "__main__":
    main()
