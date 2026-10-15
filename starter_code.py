"""
Assignment 3: Search Performance Analysis

Implements linear search, iterative binary search, recursive binary search,
correctness tests, benchmarking, and preprocessing-cost analysis.
"""

import json
import time
import random


# ============================================================================
# PART 1: Linear Search
# ============================================================================

def linear_search(data, target):
    """Return the index of target using sequential search, or -1 if absent."""
    for i, value in enumerate(data):
        if value == target:
            return i
    return -1


# ============================================================================
# PART 2: Binary Search (Iterative)
# ============================================================================

def binary_search_iterative(data, target):
    """Search sorted data iteratively; return index or -1 if absent."""
    left = 0
    right = len(data) - 1

    while left <= right:
        mid = (left + right) // 2

        if data[mid] == target:
            return mid
        elif data[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


# ============================================================================
# PART 3: Binary Search (Recursive)
# ============================================================================

def binary_search_recursive(data, target, left=None, right=None):
    """Search sorted data recursively; return index or -1 if absent."""
    if left is None:
        left = 0
    if right is None:
        right = len(data) - 1

    # Base case: the search range is empty.
    if left > right:
        return -1

    mid = (left + right) // 2

    if data[mid] == target:
        return mid
    elif data[mid] < target:
        return binary_search_recursive(data, target, mid + 1, right)
    else:
        return binary_search_recursive(data, target, left, mid - 1)


# ============================================================================
# BENCHMARKING & TESTING
# ============================================================================

def load_dataset(filename):
    """Load a dataset from the datasets directory."""
    with open(f"datasets/{filename}", "r") as f:
        return json.load(f)


def load_test_cases():
    """Load test cases for validation."""
    with open("datasets/test_cases.json", "r") as f:
        return json.load(f)


def test_search_correctness():
    """Test all three search implementations."""
    print("=" * 70)
    print("TESTING SEARCH CORRECTNESS")
    print("=" * 70)

    sorted_data = [1, 3, 5, 7, 9, 11, 13, 15]
    unsorted_data = [7, 2, 9, 1, 5, 13, 3, 11]

    tests = [
        ("Linear search on unsorted data",
         linear_search(unsorted_data, 9), 2),
        ("Linear search - item not found",
         linear_search(unsorted_data, 99), -1),
        ("Binary iterative on sorted data",
         binary_search_iterative(sorted_data, 9), 4),
        ("Binary iterative - item not found",
         binary_search_iterative(sorted_data, 10), -1),
        ("Binary recursive on sorted data",
         binary_search_recursive(sorted_data, 13), 6),
        ("Binary recursive - item not found",
         binary_search_recursive(sorted_data, 8), -1),
    ]

    for number, (description, result, expected) in enumerate(tests, start=1):
        status = "PASS" if result == expected else "FAIL"
        print(f"Test {number}: {description}")
        print(f"  Expected: {expected}, Got: {result} -> {status}")

    print()


def benchmark_algorithm(search_func, data, targets):
    """Return average search time in seconds."""
    start = time.perf_counter()

    for target in targets:
        search_func(data, target)

    end = time.perf_counter()
    return (end - start) / len(targets)


def benchmark_all_datasets():
    """Benchmark all three search algorithms on all four datasets."""
    print("=" * 70)
    print("BENCHMARKING SEARCH ALGORITHMS")
    print("=" * 70)

    datasets = {
        "customer_ids.json": "Unsorted Customer IDs (100K)",
        "product_catalog.json": "Pre-sorted Product Catalog (50K)",
        "config_settings.json": "Small Config Settings (500)",
        "dictionary_words.json": "Dictionary Words (10K)",
    }

    test_cases = load_test_cases()

    for filename, description in datasets.items():
        print(f"\nDataset: {description}")
        print("-" * 70)

        data = load_dataset(filename)
        dataset_key = filename.replace(".json", "")

        targets = (
            test_cases[dataset_key]["present"][:50]
            + test_cases[dataset_key]["absent"][:50]
        )
        random.shuffle(targets)

        linear_time = benchmark_algorithm(linear_search, data, targets)
        print(f"Linear Search: {linear_time * 1000:.4f} ms per search")

        if "unsorted" in description.lower() or "small config" in description.lower():
            sort_start = time.perf_counter()
            sorted_data = sorted(data)
            sort_time = time.perf_counter() - sort_start
            print(f"Time to sort data: {sort_time * 1000:.2f} ms (one-time cost)")
        else:
            sorted_data = data

        binary_iter_time = benchmark_algorithm(
            binary_search_iterative, sorted_data, targets
        )
        print(
            "Binary Search (Iterative): "
            f"{binary_iter_time * 1000:.4f} ms per search"
        )

        binary_rec_time = benchmark_algorithm(
            binary_search_recursive, sorted_data, targets
        )
        print(
            "Binary Search (Recursive): "
            f"{binary_rec_time * 1000:.4f} ms per search"
        )

        if binary_iter_time > 0:
            speedup = linear_time / binary_iter_time
            print(f"Binary speedup: {speedup:.2f}x faster than linear")


def analyze_preprocessing_costs():
    """Analyze when sorting the 100K customer IDs becomes worthwhile."""
    print("=" * 70)
    print("PREPROCESSING COST ANALYSIS")
    print("=" * 70)

    data = load_dataset("customer_ids.json")
    test_cases = load_test_cases()
    targets = test_cases["customer_ids"]["present"][:100]

    sort_start = time.perf_counter()
    sorted_data = sorted(data)
    sort_time = time.perf_counter() - sort_start

    linear_time = benchmark_algorithm(linear_search, data, targets)
    binary_time = benchmark_algorithm(
        binary_search_iterative, sorted_data, targets
    )

    print("Dataset: Customer IDs (100,000 unsorted entries)")
    print(f"One-time sort cost: {sort_time * 1000:.2f} ms")
    print(f"Linear search time: {linear_time * 1000:.4f} ms per search")
    print(f"Binary search time: {binary_time * 1000:.4f} ms per search")

    time_saved = linear_time - binary_time
    print(f"Time saved per search: {time_saved * 1000:.4f} ms")

    if time_saved > 0:
        break_even = sort_time / time_saved
        print(f"Break-even point: approximately {break_even:.0f} searches")


if __name__ == "__main__":
    test_search_correctness()
    benchmark_all_datasets()
    analyze_preprocessing_costs()
