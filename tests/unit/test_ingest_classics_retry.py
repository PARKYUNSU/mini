"""수집 재시도 · 실패 종료 코드 (docs/experiments/canon_1110 — arXiv 429 로 38편이 조용히 빠졌다)."""
import pytest
import requests

from apps.backfill import ingest_classics as ic


class _Resp:
    def __init__(self, code):
        self.status_code = code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(str(self.status_code), response=self)


@pytest.fixture
def fake_get(monkeypatch):
    calls = []

    def setup(*codes):
        q = list(codes)

        def get(url, **kw):
            calls.append(url)
            c = q.pop(0)
            if isinstance(c, Exception):
                raise c
            return _Resp(c)

        monkeypatch.setattr(ic.requests, "get", get)
        monkeypatch.setattr(ic._get.retry, "sleep", lambda s: None)  # tenacity 대기(1 · 3 · 5분) 건너뜀
        return calls

    return setup


def test_retries_429_and_timeout_then_succeeds(fake_get):
    calls = fake_get(429, requests.Timeout("t"), 200)
    assert ic._get("u").status_code == 200
    assert len(calls) == 3


def test_gives_up_after_all_attempts(fake_get):
    calls = fake_get(*[503] * 10)
    with pytest.raises(requests.HTTPError):
        ic._get("u")
    assert len(calls) == ic._get.retry.stop.max_attempt_number


def test_no_retry_on_404(fake_get):
    calls = fake_get(404, 200)
    with pytest.raises(requests.HTTPError):
        ic._get("u")
    assert len(calls) == 1


def test_meta_failure_returns_none(fake_get):
    fake_get(*[429] * 10)
    assert ic._fetch_arxiv_meta("2302.00093") is None


@pytest.mark.parametrize("n_failed, code", [(0, 0), (2, 1)])
def test_main_exit_code(monkeypatch, n_failed, code):
    monkeypatch.setattr(ic, "run", lambda **kw: n_failed)
    monkeypatch.setattr(ic.sys, "argv", ["ingest_classics", "--dry-run"])
    with pytest.raises(SystemExit) as e:
        ic.main()
    assert e.value.code == code
