"""Unit tests for ic_basilisk_toolkit.prng — deterministic PRNG.

These are pure-Python unit tests (no canister required).
Run: pytest tests/test_prng.py -v
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ic_basilisk_toolkit.prng import PRNG

# ---------------------------------------------------------------------------
# Determinism & reproducibility
# ---------------------------------------------------------------------------


class TestDeterminism:
    """Same seed must always produce the same sequence."""

    def test_same_seed_same_sequence(self):
        a = PRNG(seed=123)
        b = PRNG(seed=123)
        for _ in range(1000):
            assert a._next_raw() == b._next_raw()

    def test_different_seeds_differ(self):
        a = PRNG(seed=1)
        b = PRNG(seed=2)
        results_a = [a._next_raw() for _ in range(100)]
        results_b = [b._next_raw() for _ in range(100)]
        assert results_a != results_b

    def test_state_save_restore(self):
        rng = PRNG(seed=42)
        for _ in range(50):
            rng._next_raw()
        saved = rng.state
        val1 = rng.next_int(0, 1000)

        rng2 = PRNG(seed=1)
        rng2.state = saved
        val2 = rng2.next_int(0, 1000)
        assert val1 == val2

    def test_zero_seed_becomes_one(self):
        rng = PRNG(seed=0)
        assert rng.state == 1  # zero would break xorshift

    def test_negative_seed_masked(self):
        rng = PRNG(seed=-1)
        assert rng.state > 0
        # Should still produce values
        rng.next_int(0, 10)


# ---------------------------------------------------------------------------
# next_int
# ---------------------------------------------------------------------------


class TestNextInt:
    def test_range_inclusive(self):
        rng = PRNG(seed=7)
        results = {rng.next_int(0, 3) for _ in range(1000)}
        assert results == {0, 1, 2, 3}

    def test_single_value(self):
        rng = PRNG(seed=99)
        for _ in range(100):
            assert rng.next_int(5, 5) == 5

    def test_swapped_bounds(self):
        rng = PRNG(seed=10)
        val = rng.next_int(100, 0)
        assert 0 <= val <= 100

    def test_large_range(self):
        rng = PRNG(seed=42)
        for _ in range(200):
            v = rng.next_int(0, 10**15)
            assert 0 <= v <= 10**15

    def test_negative_range(self):
        rng = PRNG(seed=42)
        for _ in range(200):
            v = rng.next_int(-100, -50)
            assert -100 <= v <= -50


# ---------------------------------------------------------------------------
# next_float
# ---------------------------------------------------------------------------


class TestNextFloat:
    def test_range_zero_to_one(self):
        rng = PRNG(seed=42)
        for _ in range(10000):
            v = rng.next_float()
            assert 0.0 <= v < 1.0

    def test_distribution_not_degenerate(self):
        """Floats should span the range, not cluster at one end."""
        rng = PRNG(seed=42)
        vals = [rng.next_float() for _ in range(1000)]
        assert min(vals) < 0.1
        assert max(vals) > 0.9
        mean = sum(vals) / len(vals)
        assert 0.4 < mean < 0.6  # roughly uniform


# ---------------------------------------------------------------------------
# choice / choices / sample / shuffle
# ---------------------------------------------------------------------------


class TestSequenceOps:
    def test_choice_covers_all(self):
        rng = PRNG(seed=42)
        items = ["a", "b", "c"]
        results = {rng.choice(items) for _ in range(500)}
        assert results == {"a", "b", "c"}

    def test_choice_empty_raises(self):
        rng = PRNG(seed=1)
        try:
            rng.choice([])
            assert False, "Should have raised"
        except IndexError:
            pass

    def test_choices_length(self):
        rng = PRNG(seed=42)
        result = rng.choices(["x", "y", "z"], k=10)
        assert len(result) == 10
        assert all(r in ("x", "y", "z") for r in result)

    def test_choices_allows_repeats(self):
        rng = PRNG(seed=42)
        result = rng.choices(["a"], k=5)
        assert result == ["a"] * 5

    def test_sample_no_repeats(self):
        rng = PRNG(seed=42)
        items = list(range(20))
        result = rng.sample(items, k=10)
        assert len(result) == 10
        assert len(set(result)) == 10  # all unique
        assert all(r in items for r in result)

    def test_sample_full_population(self):
        rng = PRNG(seed=42)
        items = [1, 2, 3, 4, 5]
        result = rng.sample(items, k=5)
        assert sorted(result) == [1, 2, 3, 4, 5]

    def test_sample_too_large_raises(self):
        rng = PRNG(seed=1)
        try:
            rng.sample([1, 2], k=5)
            assert False, "Should have raised"
        except ValueError:
            pass

    def test_sample_does_not_mutate_input(self):
        rng = PRNG(seed=42)
        original = [1, 2, 3, 4, 5]
        copy = list(original)
        rng.sample(original, k=3)
        assert original == copy

    def test_shuffle_permutes(self):
        rng = PRNG(seed=42)
        items = list(range(20))
        original = list(items)
        rng.shuffle(items)
        assert sorted(items) == original  # same elements
        assert items != original  # very unlikely to stay in order

    def test_shuffle_deterministic(self):
        a = list(range(50))
        b = list(range(50))
        PRNG(seed=77).shuffle(a)
        PRNG(seed=77).shuffle(b)
        assert a == b


# ---------------------------------------------------------------------------
# weighted_choice
# ---------------------------------------------------------------------------


class TestWeightedChoice:
    def test_heavily_weighted(self):
        """Item with weight 1000 should dominate over weight 1."""
        rng = PRNG(seed=42)
        counts = {"rare": 0, "common": 0}
        for _ in range(10000):
            pick = rng.weighted_choice(["rare", "common"], [1, 1000])
            counts[pick] += 1
        assert counts["common"] > counts["rare"] * 10

    def test_single_item(self):
        rng = PRNG(seed=42)
        for _ in range(100):
            assert rng.weighted_choice(["only"], [1.0]) == "only"

    def test_mismatched_lengths_raises(self):
        rng = PRNG(seed=1)
        try:
            rng.weighted_choice(["a", "b"], [1.0])
            assert False, "Should have raised"
        except ValueError:
            pass

    def test_all_items_reachable(self):
        rng = PRNG(seed=42)
        items = ["a", "b", "c"]
        weights = [1.0, 1.0, 1.0]
        results = {rng.weighted_choice(items, weights) for _ in range(1000)}
        assert results == {"a", "b", "c"}


# ---------------------------------------------------------------------------
# Stress / edge cases
# ---------------------------------------------------------------------------


class TestStress:
    def test_million_values_no_crash(self):
        rng = PRNG(seed=1)
        for _ in range(1_000_000):
            rng._next_raw()
        assert rng.state > 0

    def test_no_zero_state(self):
        """xorshift must never reach state 0 (would get stuck)."""
        rng = PRNG(seed=42)
        for _ in range(100_000):
            rng._next_raw()
            assert rng.state != 0

    def test_large_seed(self):
        rng = PRNG(seed=(1 << 63))
        val = rng.next_int(0, 100)
        assert 0 <= val <= 100
