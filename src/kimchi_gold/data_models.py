"""
kimchi-gold 프로젝트의 데이터 모델을 정의하는 모듈입니다.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class GoldPriceData:
    """금 가격 관련 데이터를 담는 데이터 클래스"""
    domestic_price: float           # 국내 금 가격 (원/g)
    international_price: float      # 국제 금 가격 (달러/온스)
    usd_krw_rate: float            # 환율 (원/달러)
    international_krw_per_g: float  # 국제 금 가격을 원/g으로 환산
    kimchi_premium_amount: float    # 김치 프리미엄 금액 (원/g)
    kimchi_premium_percent: float   # 김치 프리미엄 비율 (%)
    data_collection_timestamp: datetime = None  # 데이터 수집 시간

    def __post_init__(self):
        if self.data_collection_timestamp is None:
            self.data_collection_timestamp = datetime.now()

    def convert_to_csv_row_format(self, date_string_format: str = "%Y-%m-%d") -> List[str]:
        """CSV 파일에 저장할 수 있는 형태의 리스트로 변환"""
        return [
            self.data_collection_timestamp.strftime(date_string_format),
            f"{self.domestic_price:.2f}",
            f"{self.international_price:.2f}",
            f"{self.usd_krw_rate:.2f}",
            f"{self.kimchi_premium_amount:.2f}",
            f"{self.kimchi_premium_percent:.2f}",
        ]

    def __str__(self) -> str:
        """사용자 친화적인 문자열 표현"""
        return (
            f"국내 금가격         : {self.domestic_price:>12,.2f} 원/g\n"
            f"국제 금 1g 원화환산 : {self.international_krw_per_g:>12,.2f} 원/g\n"
            f"김치프리미엄        : {self.kimchi_premium_amount:>12,.2f} 원/g "
            f"({self.kimchi_premium_percent:+.2f}%)"
        )

    # 하위 호환성을 위한 별칭들
    @property
    def timestamp(self):
        return self.data_collection_timestamp

    def to_csv_row(self, date_format: str = "%Y-%m-%d") -> List[str]:
        return self.convert_to_csv_row_format(date_format)


@dataclass
class ChartGenerationConfiguration:
    """차트 생성 설정을 담는 데이터 클래스"""
    display_months: int = 12
    source_data_filename: str = "kimchi_gold_price_log.csv"
    chart_figure_size: tuple = (12, 15)
    chart_visual_style: str = "seaborn-v0_8-whitegrid"

    @property
    def generated_output_filename(self) -> str:
        """출력 파일명 생성"""
        return f"kimchi_gold_price_recent_{self.display_months}months.png"

    # 하위 호환성을 위한 별칭들
    @property
    def months(self):
        return self.display_months

    @property
    def data_filename(self):
        return self.source_data_filename

    @property
    def figsize(self):
        return self.chart_figure_size

    @property
    def style(self):
        return self.chart_visual_style

    @property
    def output_filename(self):
        return self.generated_output_filename


# 하위 호환성을 위한 별칭
ChartConfig = ChartGenerationConfiguration
