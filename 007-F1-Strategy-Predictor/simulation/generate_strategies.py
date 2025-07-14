import itertools

TOTAL_LAPS = 52

MIN_STINT_LAPS = 5

compound_lifespans = {
    "SOFT": 25,
    "MEDIUM": 35,
    "HARD": 45
}

def generate_legal_strategies(available_tyres):
    """
    available_tyres: list of dicts with keys:
        - compound: "SOFT", "MEDIUM", "HARD"
        - used_laps: how many laps the tyre has already run (0 if new)
    
    Returns: list of legal strategies (list of (compound, usable_laps, used_laps))
    """
    all_strategies = []

    usable_tyres = []
    for t in available_tyres:
        max_life = compound_lifespans[t['compound'].upper()]
        remaining_life = max_life - t['used_laps']
        if remaining_life >= MIN_STINT_LAPS:
            usable_tyres.append(t)

    for stint_count in range(2, 5):
        for combo in itertools.permutations(usable_tyres, stint_count):
            compounds = [t['compound'] for t in combo]
            used_laps_list = [t['used_laps'] for t in combo]
            distinct = set(compounds)

            if len(distinct) < 2:
                continue

            max_laps = [compound_lifespans[t['compound'].upper()] - t['used_laps'] for t in combo]

            if sum(max_laps) < TOTAL_LAPS:
                continue

            laps_per_stint = distribute_laps(TOTAL_LAPS, len(combo), max_laps)

            strategy = [(compounds[i], laps_per_stint[i], used_laps_list[i]) for i in range(len(combo))]
            all_strategies.append(strategy)

    return all_strategies

def distribute_laps(total_laps, n, max_laps):
    base = total_laps // n
    extra = total_laps % n
    result = []

    for i in range(n):
        stint = base + (1 if i < extra else 0)
        result.append(min(stint, max_laps[i]))

    while sum(result) < total_laps:
        for i in range(n):
            if result[i] < max_laps[i]:
                result[i] += 1
                if sum(result) == total_laps:
                    break

    return result