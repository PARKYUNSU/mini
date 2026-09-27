"""
PDF 파싱 모듈 (PdfParser)
- PyMuPDF4LLM으로 마크다운 변환(표·레이아웃 우선)
- 일부 PDF에서 멀티컬럼 분석이 극단적으로 느리거나 멈춤 → 서브프로세스 타임아웃 후 폴백
"""

import contextlib
import multiprocessing as mp
import os
import sys
import tempfile
from pathlib import Path
from typing import Optional, Union

import pymupdf4llm


def _mupdf_stderr_suppressed() -> bool:
    """MuPDF ``syntax error: invalid key in dict`` 등 stderr 스팸 억제 (기본 켬)."""
    return (os.getenv("PDF_PARSE_MUPDF_STDERR") or "1").strip().lower() in (
        "1",
        "true",
        "yes",
        "on",
    )


@contextlib.contextmanager
def _suppress_stderr_fd():
    """C 라이브러리(MuPDF)가 fd 2에 쓰는 로그까지 잠시 막는다 (POSIX)."""
    if sys.platform == "win32" or not _mupdf_stderr_suppressed():
        yield
        return
    stderr_fd = 2
    devnull = open(os.devnull, "wb")
    try:
        saved = os.dup(stderr_fd)
        os.dup2(devnull.fileno(), stderr_fd)
        yield
    finally:
        try:
            os.dup2(saved, stderr_fd)
        finally:
            os.close(saved)
        devnull.close()


def _fitz_plain_text(pdf_path: str) -> str:
    """레이아웃 무시 빠른 추출 (폴백)."""
    import fitz

    with _suppress_stderr_fd():
        doc = fitz.open(pdf_path)
        try:
            parts: list[str] = []
            for page in doc:
                t = page.get_text("text")
                if t:
                    parts.append(t)
            return "\n\n".join(parts)
        finally:
            doc.close()


def _pymupdf4llm_worker(pdf_path: str, table_strategy: str, out_path: str) -> None:
    """자식 프로세스 전용: pymupdf4llm (부모 타임아웃으로 종료 가능)."""
    try:
        with _suppress_stderr_fd():
            md_text = pymupdf4llm.to_markdown(pdf_path, table_strategy=table_strategy)
        Path(out_path).write_text(md_text or "", encoding="utf-8")
    except Exception as e:
        Path(out_path).write_text("", encoding="utf-8")
        Path(out_path + ".err").write_text(repr(e), encoding="utf-8")


class PdfParser:
    """PDF를 마크다운으로 변환하는 클래스 (수식·표 보존, 타임아웃·폴백)"""

    def __init__(
        self,
        table_strategy: str = "lines_strict",
    ):
        """
        Args:
            table_strategy: 표 감지 전략 (lines_strict: 표 구조 보존에 유리)
        """
        self.table_strategy = table_strategy

    def to_markdown(self, pdf_path: Union[str, Path]) -> Optional[str]:
        """
        PDF 파일을 마크다운 텍스트로 변환합니다.

        - ``PDF_PARSE_TIMEOUT_SEC``(기본 240) 초과 시 pymupdf4llm 중단 후 순수 텍스트 폴백
        - ``PDF_PARSE_SUBPROCESS=0`` 이면 예전처럼 동일 프로세스(타임아웃 없음)

        Returns:
            변환된 마크다운 문자열, 실패 시 None
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            print(f"  ❌ PDF 파일 없음: {pdf_path}")
            return None

        timeout_sec = 240
        try:
            timeout_sec = max(30, int(os.getenv("PDF_PARSE_TIMEOUT_SEC", "240")))
        except ValueError:
            timeout_sec = 240

        use_sp = (os.getenv("PDF_PARSE_SUBPROCESS") or "1").strip().lower() in (
            "1",
            "true",
            "yes",
            "on",
        )

        md_text: Optional[str] = None
        if use_sp:
            md_text = self._to_markdown_subprocess(pdf_path, timeout_sec)
        else:
            md_text = self._to_markdown_inline(pdf_path)

        if not (md_text or "").strip():
            print("  ⚠️  PyMuPDF4LLM 결과 없음 → fitz 순수 텍스트 폴백", flush=True)
            md_text = _fitz_plain_text(str(pdf_path))

        if not md_text:
            return None
        if "\x00" in md_text:
            md_text = md_text.replace("\x00", "")
        return md_text if md_text.strip() else None

    def _to_markdown_inline(self, pdf_path: Path) -> Optional[str]:
        try:
            with _suppress_stderr_fd():
                return pymupdf4llm.to_markdown(
                    str(pdf_path),
                    table_strategy=self.table_strategy,
                )
        except Exception as e:
            print(f"  ❌ PDF 파싱 실패 (inline): {e}")
            return None

    def _to_markdown_subprocess(self, pdf_path: Path, timeout_sec: int) -> Optional[str]:
        ctx = mp.get_context("spawn")
        fd, out_path = tempfile.mkstemp(suffix=".md", text=True)
        os.close(fd)
        err_path = out_path + ".err"
        if os.path.isfile(err_path):
            try:
                os.unlink(err_path)
            except OSError:
                pass

        proc = ctx.Process(
            target=_pymupdf4llm_worker,
            args=(str(pdf_path), self.table_strategy, out_path),
        )
        proc.start()
        proc.join(timeout=timeout_sec)

        if proc.is_alive():
            proc.terminate()
            proc.join(timeout=15)
            if proc.is_alive():
                try:
                    proc.kill()
                except AttributeError:
                    pass
            try:
                os.unlink(out_path)
            except OSError:
                pass
            print(
                f"  ⚠️  pymupdf4llm 타임아웃({timeout_sec}s, 복잡 레이아웃 PDF) → fitz 순수 텍스트 폴백",
                flush=True,
            )
            return _fitz_plain_text(str(pdf_path))

        raw = ""
        try:
            raw = Path(out_path).read_text(encoding="utf-8")
        except OSError as e:
            print(f"  ❌ PDF 출력 읽기 실패: {e}", flush=True)
        finally:
            try:
                os.unlink(out_path)
            except OSError:
                pass

        if os.path.isfile(err_path):
            try:
                err = Path(err_path).read_text(encoding="utf-8", errors="replace")
                os.unlink(err_path)
                if not raw.strip() and err:
                    print(f"  ❌ PDF 파싱 실패 (subprocess): {err[:300]}", flush=True)
                    return _fitz_plain_text(str(pdf_path))
            except OSError:
                pass

        return raw or None
