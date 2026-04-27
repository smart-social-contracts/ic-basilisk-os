"""
Basilisk Toolkit — Deterministic Pseudo-Random Number Generator.

IC canisters have no system entropy, so ``random.random()`` and
``uuid.uuid4()`` don't work.  This module provides a seeded,
reproducible xorshift64-based PRNG suitable for canister code.

Usage::

    from ic_basilisk_toolkit.prng import PRNG

    rng = PRNG(seed=42)
    rng.next_int(0, 100)      # -> deterministic int in [0, 100]
    rng.next_float()           # -> float in [0.0, 1.0)
    rng.choice(["a", "b"])     # -> deterministic pick
    rng.sample(items, k=3)     # -> k items without replacement
    rng.shuffle(items)          # -> in-place shuffle
"""

from typing import List, Sequence, TypeVar

T = TypeVar("T")

_MASK64 = (1 << 64) - 1


class PRNG:
    """Xorshift64-based deterministic PRNG.

    Same seed always produces the same sequence, making data generation
    fully reproducible across canister upgrades and replicas.
    """

    def __init__(self, seed: int = 1):
        self._state = (seed & _MASK64) or 1

    @property
    def state(self) -> int:
        return self._state

    @state.setter
    def state(self, value: int):
        self._state = (value & _MASK64) or 1

    def _next_raw(self) -> int:
        """Advance state and return raw 64-bit value."""
        x = self._state
        x ^= (x << 13) & _MASK64
        x ^= (x >> 7) & _MASK64
        x ^= (x << 17) & _MASK64
        self._state = x & _MASK64
        return self._state

    def next_int(self, lo: int, hi: int) -> int:
        """Return a random integer in [lo, hi] inclusive."""
        if lo > hi:
            lo, hi = hi, lo
        span = hi - lo + 1
        return lo + (self._next_raw() % span)

    def next_float(self) -> float:
        """Return a float in [0.0, 1.0)."""
        return (self._next_raw() & ((1 << 53) - 1)) / (1 << 53)

    def choice(self, seq: Sequence[T]) -> T:
        """Pick one element from *seq*."""
        if not seq:
            raise IndexError("cannot choose from empty sequence")
        return seq[self._next_raw() % len(seq)]

    def choices(self, seq: Sequence[T], k: int) -> List[T]:
        """Pick *k* elements with replacement."""
        if not seq:
            raise IndexError("cannot choose from empty sequence")
        return [seq[self._next_raw() % len(seq)] for _ in range(k)]

    def sample(self, seq: Sequence[T], k: int) -> List[T]:
        """Pick *k* unique elements without replacement."""
        pool = list(seq)
        if k > len(pool):
            raise ValueError("sample larger than population")
        result: List[T] = []
        for _ in range(k):
            idx = self._next_raw() % len(pool)
            result.append(pool.pop(idx))
        return result

    def shuffle(self, lst: list) -> None:
        """In-place Fisher-Yates shuffle."""
        for i in range(len(lst) - 1, 0, -1):
            j = self._next_raw() % (i + 1)
            lst[i], lst[j] = lst[j], lst[i]

    def weighted_choice(self, seq: Sequence[T], weights: Sequence[float]) -> T:
        """Pick one element weighted by *weights*."""
        if len(seq) != len(weights):
            raise ValueError("seq and weights must be same length")
        total = sum(weights)
        r = self.next_float() * total
        cumulative = 0.0
        for item, w in zip(seq, weights):
            cumulative += w
            if r < cumulative:
                return item
        return seq[-1]
