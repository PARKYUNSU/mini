"""
arXiv 논문 수집 모듈 (ArxivFetcher)
- arXiv API를 통해 cs.AI 카테고리 논문 검색 및 메타데이터 추출
- PDF 다운로드 URL 제공
- 네트워크 요청에 tenacity 재시도 (1분→3분→5분, 최대 3회)
"""

import random
import sys
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.parse import urlencode

import requests

# retry_utils (프로젝트 루트)
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from retry_utils import retry_on_network_error


# arXiv API 네임스페이스 (Atom 1.0)
ATOM_NS = "http://www.w3.org/2005/Atom"
OPENSEARCH_NS = "http://a9.com/-/spec/opensearch/1.1/"
ARXIV_NS = {
    "atom": ATOM_NS,
    "arxiv": "http://arxiv.org/schemas/atom",
}


@dataclass
class PaperMetadata:
    """논문 메타데이터 데이터 클래스"""

    paper_id: str
    title: str
    authors: list[str]
    abstract: str
    published: str
    pdf_url: str


class ArxivFetcher:
    """arXiv API에서 논문을 검색하고 메타데이터를 추출하는 클래스"""

    BASE_URL = "http://export.arxiv.org/api/query"

    def __init__(
        self,
        category: str = "cs.AI",
        limit: int = 3,
        min_delay: float = 3.0,
        max_delay: float = 5.0,
    ):
        """
        Args:
            category: arXiv 카테고리 (기본: cs.AI)
            limit: 한 번에 가져올 논문 수
            min_delay: 최소 딜레이(초)
            max_delay: 최대 딜레이(초)
        """
        self.category = category
        self.limit = limit
        self.min_delay = min_delay
        self.max_delay = max_delay
        self._session = requests.Session()
        self._session.headers.update(
            {"User-Agent": "arXivPaperCollector/1.0 (AI Research Pipeline)"}
        )

    def _random_delay(self) -> None:
        """IP 차단 방지를 위한 랜덤 딜레이"""
        delay = random.uniform(self.min_delay, self.max_delay)
        time.sleep(delay)

    @retry_on_network_error
    def _get_with_retry(self, url: str, timeout: int = 30, stream: bool = False):
        """네트워크 재시도 적용 GET 요청"""
        resp = self._session.get(url, timeout=timeout, stream=stream)
        # HTTP 4xx(특히 429)도 예외로 승격해야 tenacity가 재시도를 수행할 수 있음.
        resp.raise_for_status()
        return resp

    def _parse_entry(self, entry: ET.Element) -> Optional[PaperMetadata]:
        """Atom XML entry 요소에서 PaperMetadata 추출"""
        try:
            ns = "{" + ATOM_NS + "}"
            # 논문 ID (예: http://arxiv.org/abs/2401.12345 -> 2401.12345)
            id_elem = entry.find(f"{ns}id")
            if id_elem is None or id_elem.text is None:
                return None
            paper_id = id_elem.text.split("/abs/")[-1].strip()

            # 제목
            title_elem = entry.find(f"{ns}title")
            title = title_elem.text.strip().replace("\n", " ") if title_elem is not None and title_elem.text else ""

            # 저자 목록
            authors = []
            for author in entry.findall(f"{ns}author"):
                name_elem = author.find(f"{ns}name")
                if name_elem is not None and name_elem.text:
                    authors.append(name_elem.text.strip())

            # 요약
            summary_elem = entry.find(f"{ns}summary")
            abstract = summary_elem.text.strip().replace("\n", " ") if summary_elem is not None and summary_elem.text else ""

            # 출판일
            published_elem = entry.find(f"{ns}published")
            published = published_elem.text.strip() if published_elem is not None and published_elem.text else ""

            # PDF URL (Atom feed의 link 요소에서 title="pdf"인 것의 href)
            pdf_url = ""
            for link in entry.findall(f"{ns}link"):
                if link.get("title") == "pdf":
                    pdf_url = link.get("href", "")
                    break
            if not pdf_url:
                pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"

            return PaperMetadata(
                paper_id=paper_id,
                title=title,
                authors=authors,
                abstract=abstract,
                published=published,
                pdf_url=pdf_url,
            )
        except (AttributeError, IndexError, KeyError) as e:
            print(f"  ⚠️  메타데이터 파싱 실패: {e}")
            return None

    def fetch_metadata_list(self) -> list[PaperMetadata]:
        """
        arXiv API에서 논문 메타데이터 목록을 가져옵니다.
        (start=0, limit=self.limit)

        Returns:
            PaperMetadata 리스트 (실패 시 빈 리스트)
        """
        return self.fetch_metadata_batch(start=0, limit=self.limit)

    def _build_search_query(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> str:
        """
        search_query 문자열 생성.
        submittedDate 형식: [YYYYMMDDhhmm TO YYYYMMDDhhmm] (arXiv API, GMT)
        - 0600 = 00:00 UTC 권장 (arXiv 예시)
        """
        base = f"cat:{self.category}"
        if start_date and end_date:
            # "2023-01-01" -> "202301010600", "2023-12-31" -> "202312312359"
            start_ts = start_date.replace("-", "") + "0600"
            end_ts = end_date.replace("-", "") + "2359"
            base = f"{base} AND submittedDate:[{start_ts} TO {end_ts}]"
        return base

    def get_search_total_results(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Optional[int]:
        """
        동일 검색식에 대해 arXiv API가 보고하는 총 결과 수(opensearch:totalResults).
        백필 진행률·완주 여부 확인용. (네트워크/파싱 실패 시 None)
        """
        search_query = self._build_search_query(start_date, end_date)
        params = {
            "search_query": search_query,
            "start": 0,
            "max_results": 1,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
        url = f"{self.BASE_URL}?{urlencode(params)}"
        try:
            response = self._get_with_retry(url, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"⚠️  API 총건수 조회 실패: {e}")
            return None
        try:
            root = ET.fromstring(response.content)
            el = root.find(f".//{{{OPENSEARCH_NS}}}totalResults")
            if el is not None and el.text and el.text.strip():
                return int(el.text.strip())
            for elem in root.iter():
                if elem.tag.endswith("totalResults") and elem.text and elem.text.strip():
                    return int(elem.text.strip())
        except (ET.ParseError, ValueError) as e:
            print(f"⚠️  API 총건수 파싱 실패: {e}")
        return None

    def fetch_metadata_batch(
        self,
        start: int = 0,
        limit: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> list[PaperMetadata]:
        """
        arXiv API에서 페이징으로 논문 메타데이터를 가져옵니다.
        (백필/대량 수집용)

        Args:
            start: 오프셋 (0부터 시작)
            limit: 가져올 개수 (None이면 self.limit 사용)
            start_date: 수집 시작일 (YYYY-MM-DD, 기간 기반 백필용)
            end_date: 수집 종료일 (YYYY-MM-DD, 기간 기반 백필용)

        Returns:
            PaperMetadata 리스트 (실패 시 빈 리스트)
        """
        batch_limit = limit if limit is not None else self.limit
        search_query = self._build_search_query(start_date, end_date)
        params = {
            "search_query": search_query,
            "start": start,
            "max_results": batch_limit,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
        url = f"{self.BASE_URL}?{urlencode(params)}"

        try:
            self._random_delay()
            print("📡 arXiv API 요청 중...")
            response = self._get_with_retry(url, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            # 429 같은 레이트리밋은 run_backfill에서 재대기/복구하도록 예외로 올린다.
            print(f"❌ API 요청 실패: {e}")
            raise

        try:
            root = ET.fromstring(response.content)
            entries = root.findall(f".//{{{ATOM_NS}}}entry", namespaces=None)
            papers = []
            for entry in entries:
                meta = self._parse_entry(entry)
                if meta:
                    papers.append(meta)
            return papers
        except ET.ParseError as e:
            print(f"❌ XML 파싱 실패: {e}")
            return []

    def download_pdf(self, pdf_url: str, save_path: str) -> bool:
        """
        PDF를 다운로드하여 지정 경로에 저장합니다.

        Args:
            pdf_url: PDF 다운로드 URL
            save_path: 저장할 로컬 경로

        Returns:
            성공 여부
        """
        try:
            self._random_delay()
            response = self._get_with_retry(pdf_url, timeout=60, stream=True)
            response.raise_for_status()
            with open(save_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        except requests.RequestException as e:
            print(f"  ❌ PDF 다운로드 실패: {e}")
            return False
        except OSError as e:
            print(f"  ❌ 파일 저장 실패: {e}")
            return False
