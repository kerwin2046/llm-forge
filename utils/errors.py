from openai import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    InternalServerError,
    RateLimitError,
)


class FatalAPIError(Exception):
    """不可重试的错误：配置问题，直接报给用户。"""


class RetryableAPIError(Exception):
    """可重试的错误：网络抖动、限流、服务端故障。"""

    def __init__(self, message: str, retry_after: float | None = None) -> None:
        super().__init__(message)
        self.retry_after = retry_after


def classify(exc: Exception) -> FatalAPIError | RetryableAPIError:
    """把 openai 异常转成我们自己的分类。"""
    if isinstance(exc, AuthenticationError):
        return FatalAPIError(
            "API key 无效或未设置，请检查 DEEPSEEK_API_KEY 环境变量。"
        )

    if isinstance(exc, RateLimitError):
        retry_after = _parse_retry_after(exc)
        return RetryableAPIError(f"触发限流 (429)，将在 {retry_after}s 后重试。", retry_after)

    if isinstance(exc, InternalServerError):
        return RetryableAPIError(f"服务端错误 ({exc.status_code})，将重试。")

    if isinstance(exc, (APIConnectionError, APITimeoutError)):
        return RetryableAPIError(f"网络错误：{exc}，将重试。")

    return FatalAPIError(f"未知错误：{exc}")


def _parse_retry_after(exc: RateLimitError) -> float:
    try:
        return float(exc.response.headers.get("Retry-After", 5))
    except Exception:
        return 5.0
