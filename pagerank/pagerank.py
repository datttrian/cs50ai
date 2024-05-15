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
    # Get the total number of pages in the corpus
    N = len(corpus)

    # Initialize the probabilities dictionary with keys from the corpus and values set to 0
    probabilities = dict.fromkeys(corpus.keys(), 0)

    # If the current page has outgoing links
    if corpus[page]:
        linked_pages = corpus[page]
        num_links = len(linked_pages)

        # Calculate the probability distribution
        for p in probabilities:
            # Base probability for each page when no specific link is chosen
            probabilities[p] = (1 - damping_factor) / N

            # Additional probability if the page is linked directly from the current page
            if p in linked_pages:
                probabilities[p] += damping_factor / num_links

    # If the current page has no outgoing links, distribute probability equally
    else:
        for p in probabilities:
            probabilities[p] = 1 / N

    # Return the calculated probability distribution
    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize the PageRank dictionary with each page having a rank of 0
    page_rank = dict.fromkeys(corpus.keys(), 0)

    # Convert corpus keys to a list to easily pick a random start page
    pages = list(corpus.keys())

    # Choose a random page as the starting point
    current_page = random.choice(pages)

    # Simulate n steps of the random surfer
    for _ in range(n):
        # Increment the rank count for the current page
        page_rank[current_page] += 1

        # Get the probability distribution for the next page to visit
        next_page_distribution = transition_model(corpus, current_page, damping_factor)

        # Randomly choose the next page based on the probability distribution
        next_page = random.choices(
            list(next_page_distribution.keys()),
            weights=next_page_distribution.values(),
            k=1,
        )[0]

        # Move to the next page
        current_page = next_page

    # Normalize the rank counts to get the final PageRank values
    for page in page_rank:
        page_rank[page] /= n

    # Return the computed PageRank values
    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Get the total number of pages in the corpus
    N = len(corpus)

    # Initialize the PageRank for each page to 1/N
    page_rank = dict.fromkeys(corpus.keys(), 1 / N)

    # Initialize the new PageRank dictionary with zero values
    new_page_rank = dict.fromkeys(corpus.keys(), 0)

    # Iterate until the PageRank values converge
    converged = False
    while not converged:
        converged = True

        for page in corpus:
            rank_sum = 0

            # Calculate the rank sum from pages that link to the current page
            for possible_page in corpus:
                if page in corpus[possible_page]:
                    rank_sum += page_rank[possible_page] / len(corpus[possible_page])

                # Handle pages with no outgoing links by considering a random jump
                if not corpus[possible_page]:
                    rank_sum += page_rank[possible_page] / N

            # Compute the new PageRank value for the current page
            new_page_rank[page] = (1 - damping_factor) / N + damping_factor * rank_sum

        # Check for convergence
        for page in page_rank:
            if abs(new_page_rank[page] - page_rank[page]) > 0.001:
                converged = False

            # Update the PageRank values
            page_rank[page] = new_page_rank[page]

    # Return the converged PageRank values
    return page_rank


if __name__ == "__main__":
    main()
