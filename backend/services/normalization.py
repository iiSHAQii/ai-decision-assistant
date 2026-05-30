from backend.services.providers.base import Direction


def min_max_normalize(
    values: list[float | None],
    direction: Direction,
) -> list[float | None]:
    """Min-max normalize values to [0, 1] across the input list.

    - "higher_is_better": preserves order, smallest -> 0, largest -> 1
    - "lower_is_better": inverts, smallest -> 1, largest -> 0
    - "already_normalized": passthrough, clamped to [0, 1]

    None values pass through as None. If all non-None inputs are equal,
    each non-None entry gets 0.5 (no differentiation).
    """
    if direction == "already_normalized":
        return [None if v is None else max(0.0, min(1.0, v)) for v in values]

    nums = [v for v in values if v is not None]
    if not nums:
        return [None] * len(values)

    lo, hi = min(nums), max(nums)
    if hi == lo:
        return [None if v is None else 0.5 for v in values]

    spread = hi - lo
    out: list[float | None] = []
    for v in values:
        if v is None:
            out.append(None)
            continue
        norm = (v - lo) / spread
        if direction == "lower_is_better":
            norm = 1.0 - norm
        out.append(norm)
    return out
