import time


class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.buckets = {}

    def is_allowed(self, key: str) -> bool:
        current_time = time.time()

        if key not in self.buckets:
            self.buckets[key] = {
                "tokens": self.capacity,
                "last_refill": current_time
            }

        bucket = self.buckets[key]

        time_passed = current_time - bucket["last_refill"]
        tokens_to_add = time_passed * self.refill_rate

        bucket["tokens"] = min(
            self.capacity,
            bucket["tokens"] + tokens_to_add
        )

        bucket["last_refill"] = current_time

        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            return True

        return False


login_rate_limiter = TokenBucketRateLimiter(
    capacity=5,
    refill_rate=1 / 12
)