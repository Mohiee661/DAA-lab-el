import time
from kmp import kmp_search
from naive_search import naive_search


def load_signatures(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def load_data(filename):
    with open(filename, 'r') as f:
        return f.read()


def detect_intrusions(data, signatures, search_func):
    results = {}
    for signature in signatures:
        matches = search_func(data, signature)
        if matches:
            results[signature] = matches
    return results


def main():
    signatures_file = 'signatures.txt'
    data_file = 'sample_log.txt'
    signatures = load_signatures(signatures_file)
    data = load_data(data_file)

    # Detect using KMP
    start_time = time.time()
    kmp_results = detect_intrusions(data, signatures, kmp_search)
    kmp_time = time.time() - start_time

    # Detect using Naive Search
    start_time = time.time()
    naive_results = detect_intrusions(data, signatures, naive_search)
    naive_time = time.time() - start_time

    print("KMP Results:")
    for signature, matches in kmp_results.items():
        print(f"Signature: {signature}, Matches at positions: {matches}")
    print(f"KMP Time: {kmp_time:.6f} seconds")

    print("\nNaive Search Results:")
    for signature, matches in naive_results.items():
        print(f"Signature: {signature}, Matches at positions: {matches}")
    print(f"Naive Search Time: {naive_time:.6f} seconds")


if __name__ == "__main__":
    main() 