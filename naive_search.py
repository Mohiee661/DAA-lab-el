def naive_search(text, pattern):
    if not pattern or not text:
        return []
    matches = []
    for i in range(len(text) - len(pattern) + 1):
        if text[i:i + len(pattern)] == pattern:
            matches.append(i)
    return matches 