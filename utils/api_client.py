class CompanyAPIClient:
    """
    사내 Reference 자료 혹은 Template API Client (Mock)
    
    실제 API 연동시에는 requests나 httpx를 사용하세요.
    """

    def __init__(self):
        # Mock Data (예시 템플릿 데이터)
        self.templates = {
            "회의록": "회의록 양식: \n- 회의 일시\n- 장소\n- 참석자\n- 주요 안건\n- 논의 내용\n- 결론 및 조치 사항",
            "출장 보고서": "출장 보고서 양식: \n- 출장지\n- 출장 기간\n- 출장 목적\n- 주요 활동\n- 결과 및 향후 계획",
            "경조사 신청": "경조사 신청서 양식: \n- 신청인\n- 관계\n- 경조사 종류\n- 일시 및 장소\n- 기타 사항",
        }

    def search_templates(self, query: str) -> str:
        """
        사용자 질의어로 템플릿 검색
        """
        for keyword, template in self.templates.items():
            if keyword in query:
                return template
        return None
