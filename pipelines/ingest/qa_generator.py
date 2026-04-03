"""
파인튜닝 데이터 생성 모듈 (QaGenerator)
- Gemini API로 논문 기반 Q&A 생성 후 JSONL 저장
"""

import json
import os
from pathlib import Path
from typing import Optional, Union

import google.generativeai as genai


class QaGenerator:
    """논문 본문에서 Q&A 세트를 생성하여 파인튜닝용 JSONL로 저장하는 클래스"""

    PROMPT_TEMPLATE = """다음은 AI/ML 분야 학술 논문의 마크다운 본문입니다.

이 논문을 읽고, 반드시 아래 JSON 형식만 출력하세요. 다른 텍스트는 절대 포함하지 마세요.

JSON 형식 (이 구조만 정확히 따르세요):
{{"instruction": "실제 사용자가 논문에 대해 물어볼 법한 구체적인 질문 1개", "output": "질문에 대한 전문적이고 상세한 답변"}}

- instruction: 논문의 핵심(기여점, 방법론, 실험 결과 등)을 묻는 자연스러운 질문. 사용자가 검색창에 입력할 법한 구체적인 문장.
- output: instruction의 질문에 대한 전문적이고 상세한 답변만 작성. 질문을 반복하지 말고 답변만 담으세요.

---

논문 본문:
{content}
"""

    def __init__(
        self,
        output_path: Union[str, Path] = "./finetune_datasets/qa_data.jsonl",
        model_name: str = "gemini-2.5-flash",
        system_prompt: str = "당신은 최신 AI 논문을 분석하는 수석 연구원입니다.",
    ):
        """
        Args:
            output_path: JSONL 저장 경로
            model_name: Gemini 모델명
            system_prompt: 시스템 프롬프트 (최종 JSONL에 합쳐서 저장)
        """
        self.output_path = Path(output_path)
        parent = self.output_path.parent
        if parent != Path("."):
            os.makedirs(parent, exist_ok=True)
        self.model_name = model_name
        self.system_prompt = system_prompt
        self._configure_api()

    def _configure_api(self) -> None:
        """API 키를 .env에서 로드하여 설정"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY가 설정되지 않았습니다. .env 파일에 GEMINI_API_KEY=your_key 를 추가하세요."
            )
        genai.configure(api_key=api_key)

    def _truncate_content(self, content: str, max_chars: int = 120000) -> str:
        """Gemini 입력 제한을 위한 본문 축약"""
        if len(content) <= max_chars:
            return content
        return content[:max_chars] + "\n\n[... 본문이 길어 생략됨 ...]"

    def generate_qa(self, markdown_content: str) -> Optional[dict]:
        """
        논문 본문을 입력으로 Q&A 1세트를 생성합니다.

        Args:
            markdown_content: 마크다운 본문

        Returns:
            {"system", "instruction", "output"} 형태 딕셔너리, 실패 시 None
        """
        try:
            truncated = self._truncate_content(markdown_content)
            prompt = self.PROMPT_TEMPLATE.format(content=truncated)

            generation_config = genai.types.GenerationConfig(
                response_mime_type="application/json",
            )
            model = genai.GenerativeModel(
                self.model_name,
                generation_config=generation_config,
            )
            response = model.generate_content(prompt)

            if not response.text:
                return None

            parsed = json.loads(response.text.strip())
            instruction = parsed.get("instruction", "").strip()
            output = parsed.get("output", "").strip()

            if not instruction or not output:
                return None

            return {
                "system": self.system_prompt,
                "instruction": instruction,
                "output": output,
            }
        except json.JSONDecodeError as e:
            print(f"  ❌ Q&A 생성 실패 (JSON 파싱): {e}")
            return None
        except Exception as e:
            print(f"  ❌ Q&A 생성 실패: {e}")
            return None

    def save_qa(self, qa_record: dict) -> bool:
        """
        Q&A 레코드를 JSONL 파일에 append 저장합니다.

        Args:
            qa_record: {"system", "instruction", "output"} 형태 딕셔너리

        Returns:
            저장 성공 여부
        """
        try:
            line = json.dumps(qa_record, ensure_ascii=False) + "\n"
            with open(self.output_path, "a", encoding="utf-8") as f:
                f.write(line)
            return True
        except (OSError, TypeError) as e:
            print(f"  ❌ Q&A 저장 실패: {e}")
            return False
