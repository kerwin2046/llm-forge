import random
import time
from collections.abc import Callable
from typing import TypeVar

from utils.errors import FatalAPIError, RetryableAPIError, classify

T = TypeVar("T")

DEFAULT_MAX_RETRIES = 3
DEFAULT_BASE_DELAY = 1.0
DEFAULT_MAX_DELAY = 30.0


def with_retry(
    fn: Callable[[], T],
    max_retries: int = DEFAULT_MAX_RETRIES,
    base_delay: float = DEFAULT_BASE_DELAY,
    max_delay: float = DEFAULT_MAX_DELAY,
) -> T:
    """
    执行 fn()，遇到可重试错误时指数退避重试。
    遇到不可重试错误时立即抛出 FatalAPIError。
    """
    last_exc: Exception | None = None

    for attempt in range(max_retries + 1):
        try:
            return fn()
        except (FatalAPIError, RetryableAPIError):
            raise
        except Exception as exc:
            classified = classify(exc)

            if isinstance(classified, FatalAPIError):
                raise classified from exc

            last_exc = classified

            if attempt == max_retries:
                break

            wait = _calc_wait(classified, attempt, base_delay, max_delay)
            print(f"\n[retry] {classified} 第 {attempt + 1}/{max_retries} 次，等待 {wait:.1f}s...")
            time.sleep(wait)

    raise RuntimeError(f"重试 {max_retries} 次后仍然失败。最后错误：{last_exc}") from last_exc


def _calc_wait(
    exc: RetryableAPIError,
    attempt: int,
    base_delay: float,
    max_delay: float,
) -> float:
    if exc.retry_after is not None:
        return exc.retry_after

    exponential = base_delay * (2 ** attempt)
    jitter = random.uniform(0, 0.5 * exponential)
    return min(exponential + jitter, max_delay)
