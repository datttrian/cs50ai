import csv
import itertools
import sys

PROBS = {
    # Unconditional probabilities for having gene
    "gene": {2: 0.01, 1: 0.03, 0: 0.96},
    "trait": {
        # Probability of trait given two copies of gene
        2: {True: 0.65, False: 0.35},
        # Probability of trait given one copy of gene
        1: {True: 0.56, False: 0.44},
        # Probability of trait given no gene
        0: {True: 0.01, False: 0.99},
    },
    # Mutation probability
    "mutation": 0.01,
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {"gene": {2: 0, 1: 0, 0: 0}, "trait": {True: 0, False: 0}}
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (
                people[person]["trait"] is not None
                and people[person]["trait"] != (person in have_trait)
            )
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = {}
    with open(filename, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (
                    True
                    if row["trait"] == "1"
                    else False if row["trait"] == "0" else None
                ),
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s)
        for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def check_how_many_copies(person, one_gene, two_genes):
    if person in one_gene:
        return 1
    if person in two_genes:
        return 2
    else:
        return 0


def probs_no_parents(copies_gene, has_trait):
    return PROBS["gene"][copies_gene] * PROBS["trait"][copies_gene][has_trait]


def probs_has_parents(person, people, one_gene, two_genes):
    mother = people[person]["mother"]
    mother_genes = check_how_many_copies(mother, one_gene, two_genes)

    father = people[person]["father"]
    father_genes = check_how_many_copies(father, one_gene, two_genes)

    probability_mother_pass_gene = mother_genes / 2
    probability_father_pass_gene = father_genes / 2

    p_father_pass_gene_and_dont_mutate = probability_father_pass_gene * (
        1 - PROBS["mutation"]
    )
    p_father_pass_gene_and_do_mutate = probability_father_pass_gene * PROBS["mutation"]
    p_father_dont_pass_gene_and_dont_mutate = (1 - probability_father_pass_gene) * (
        1 - PROBS["mutation"]
    )
    p_father_dont_pass_gene_and_do_mutate = (1 - probability_father_pass_gene) * PROBS[
        "mutation"
    ]

    p_mother_pass_gene_and_dont_mutate = probability_mother_pass_gene * (
        1 - PROBS["mutation"]
    )
    p_mother_pass_gene_and_do_mutate = probability_mother_pass_gene * PROBS["mutation"]
    p_mother_dont_pass_gene_and_dont_mutate = (1 - probability_mother_pass_gene) * (
        1 - PROBS["mutation"]
    )
    p_mother_dont_pass_gene_and_do_mutate = (1 - probability_mother_pass_gene) * PROBS[
        "mutation"
    ]

    probability = None
    child_genes = check_how_many_copies(person, one_gene, two_genes)

    if child_genes == 0:
        probability = (
            p_father_pass_gene_and_do_mutate * p_mother_dont_pass_gene_and_dont_mutate
            + p_father_pass_gene_and_do_mutate * p_mother_pass_gene_and_do_mutate
            + p_father_dont_pass_gene_and_dont_mutate
            * p_mother_dont_pass_gene_and_dont_mutate
            + p_father_dont_pass_gene_and_dont_mutate * p_mother_pass_gene_and_do_mutate
        )

    # If child_genes = 1, we have 8 scenarios
    elif child_genes == 1:
        probability = (
            p_father_pass_gene_and_dont_mutate * p_mother_dont_pass_gene_and_dont_mutate
            + p_father_pass_gene_and_dont_mutate * p_mother_pass_gene_and_do_mutate
            + p_father_pass_gene_and_do_mutate * p_mother_dont_pass_gene_and_do_mutate
            + p_father_pass_gene_and_do_mutate * p_mother_pass_gene_and_dont_mutate
            + p_father_dont_pass_gene_and_do_mutate
            * p_mother_dont_pass_gene_and_dont_mutate
            + p_father_dont_pass_gene_and_do_mutate * p_mother_pass_gene_and_do_mutate
            + p_father_dont_pass_gene_and_dont_mutate
            * p_mother_pass_gene_and_dont_mutate
            + p_father_dont_pass_gene_and_dont_mutate
            * p_mother_dont_pass_gene_and_do_mutate
        )

    # If child_genes = 2, we have 4 scenarios
    elif child_genes == 2:
        probability = (
            p_father_pass_gene_and_dont_mutate * p_mother_pass_gene_and_dont_mutate
            + p_father_dont_pass_gene_and_do_mutate
            * p_mother_dont_pass_gene_and_do_mutate
            + p_father_dont_pass_gene_and_do_mutate * p_mother_pass_gene_and_dont_mutate
            + p_father_pass_gene_and_dont_mutate * p_mother_dont_pass_gene_and_do_mutate
        )

    return probability


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    probability = 1

    for person in people:
        copies_gene = check_how_many_copies(person, one_gene, two_genes)

        if person in have_trait:
            has_trait = True
        else:
            has_trait = False

        if people[person]["mother"] == None:
            probability *= probs_no_parents(copies_gene, has_trait)
        else:
            probability *= (
                probs_has_parents(person, people, one_gene, two_genes, have_trait)
                * PROBS["trait"][copies_gene][has_trait]
            )

    return probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        copies_gene = check_how_many_copies(person, one_gene, two_genes)
        has_trait = person in have_trait

        probabilities[person]["gene"][copies_gene] += p
        probabilities[person]["trait"][has_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        total_p_genes = sum(probabilities[person]["gene"].values())
        total_p_trait = sum(probabilities[person]["trait"].values())

        for gene in probabilities[person]["gene"]:
            original_value = probabilities[person]["gene"][gene]
            new_value = original_value / total_p_genes
            probabilities[person]["gene"][gene] = new_value

        for trait in probabilities[person]["trait"]:
            original_value = probabilities[person]["trait"][trait]
            new_value = original_value / total_p_trait
            probabilities[person]["trait"][trait] = new_value


if __name__ == "__main__":
    main()
