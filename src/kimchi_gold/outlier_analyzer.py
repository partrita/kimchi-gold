"""
김치 프리미엄 데이터의 이상치를 분석하는 모듈입니다.
"""

import logging
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from .configuration import GOLD_PRICE_DATA_CSV_FILE

# 로깅 설정
logger = logging.getLogger(__name__)


def calculate_statistical_outlier_boundaries(
    data_series: pd.Series, interquartile_range_multiplier: float = 1.5
) -> tuple[float, float]:
    """
    데이터 시리즈에서 이상치 경계값을 계산합니다.

    Args:
        data_series: 분석할 데이터 시리즈
        interquartile_range_multiplier: IQR 배수 (기본값: 1.5)

    Returns:
        (lower_boundary, upper_boundary) 튜플
    """
    first_quartile = data_series.quantile(0.25)
    third_quartile = data_series.quantile(0.75)
    interquartile_range = third_quartile - first_quartile

    lower_boundary = (
        first_quartile - interquartile_range_multiplier * interquartile_range
    )
    upper_boundary = (
        third_quartile + interquartile_range_multiplier * interquartile_range
    )

    return lower_boundary, upper_boundary


def filter_dataframe_by_recent_dates(
    source_dataframe: pd.DataFrame, date_column_name: str, days_to_look_back: int = 365
) -> pd.DataFrame:
    """
    데이터프레임에서 최근 N일 내의 데이터만 필터링합니다.

    Args:
        source_dataframe: 필터링할 데이터프레임
        date_column_name: 날짜 컬럼명
        days_to_look_back: 뒤로 갈 일수 (기본값: 365일)

    Returns:
        필터링된 데이터프레임
    """
    if source_dataframe.empty:
        return source_dataframe

    processed_dataframe = source_dataframe.copy()

    # The date column should already be datetime type from pd.read_csv(parse_dates=...)

    # 기준 날짜 계산
    current_date = datetime.now().date()
    cutoff_date = current_date - timedelta(days=days_to_look_back)

    # 날짜 필터링
    filtered_dataframe = processed_dataframe[
        (processed_dataframe[date_column_name].dt.date >= cutoff_date)
        & (processed_dataframe[date_column_name].dt.date <= current_date)
    ].copy()

    logger.debug(
        f"필터링 결과: 전체 {len(source_dataframe)} 행 → {len(filtered_dataframe)} 행"
    )
    return filtered_dataframe


def determine_if_latest_value_is_outlier(
    input_dataframe: pd.DataFrame,
    target_column_name: str,
    date_column_name: str = "날짜",
    analysis_period_days: int = 365,
    iqr_multiplier_threshold: float = 1.5,
) -> bool:
    """
    특정 컬럼의 최근 데이터를 기준으로 사분위수를 계산하고,
    가장 최근 데이터가 이상치인지 여부를 반환합니다.

    Args:
        input_dataframe: 데이터프레임
        target_column_name: 확인할 컬럼명
        date_column_name: 날짜 컬럼명 (기본값: '날짜')
        analysis_period_days: 분석할 과거 일수 (기본값: 365일)
        iqr_multiplier_threshold: IQR 배수 (기본값: 1.5)

    Returns:
        가장 최근 데이터가 이상치면 True, 아니면 False

    Raises:
        ValueError: 데이터가 없거나 컬럼이 없을 때
    """
    if input_dataframe.empty:
        logger.warning("비어있는 데이터프레임입니다")
        return False

    if target_column_name not in input_dataframe.columns:
        raise ValueError(f"컬럼 '{target_column_name}'을 찾을 수 없습니다")

    if date_column_name not in input_dataframe.columns:
        raise ValueError(f"날짜 컬럼 '{date_column_name}'을 찾을 수 없습니다")

    # 최근 데이터만 필터링
    recent_period_data = filter_dataframe_by_recent_dates(
        input_dataframe, date_column_name, analysis_period_days
    )

    if recent_period_data.empty:
        logger.warning(f"최근 {analysis_period_days}일 내 데이터가 없습니다")
        return False

    if len(recent_period_data) < 4:  # 사분위수 계산에 최소 4개 데이터 필요
        logger.warning(
            f"사분위수 계산에 충분한 데이터가 없습니다 (현재: {len(recent_period_data)}개)"
        )
        return False

    # 이상치 경계값 계산
    target_column_data = recent_period_data[target_column_name]
    lower_boundary, upper_boundary = calculate_statistical_outlier_boundaries(
        target_column_data, iqr_multiplier_threshold
    )

    # 가장 최근 값 확인
    most_recent_value = recent_period_data.iloc[-1][target_column_name]

    is_outlier_detected = (most_recent_value < lower_boundary) or (
        most_recent_value > upper_boundary
    )

    logger.info(
        f"이상치 분석 결과 - 컬럼: {target_column_name}, "
        f"최신값: {most_recent_value:.2f}, 범위: [{lower_boundary:.2f}, {upper_boundary:.2f}], "
        f"이상치: {is_outlier_detected}"
    )

    return is_outlier_detected


def perform_kimchi_premium_outlier_analysis(
    data_csv_file_path: Path = GOLD_PRICE_DATA_CSV_FILE,
    analysis_column_name: str = "김치프리미엄(%)",
    historical_analysis_days: int = 365,
    statistical_threshold_multiplier: float = 1.5,
) -> Optional[bool]:
    """
    김치 프리미엄 데이터의 이상치 분석을 수행합니다.

    Args:
        data_csv_file_path: 분석할 CSV 파일 경로
        analysis_column_name: 분석할 컬럼명
        historical_analysis_days: 분석할 과거 일수
        statistical_threshold_multiplier: IQR 배수

    Returns:
        이상치면 True, 정상이면 False, 오류시 None
    """
    try:
        logger.info(f"김치 프리미엄 이상치 분석 시작: {data_csv_file_path}")

        # 데이터 로드
        if not data_csv_file_path.exists():
            logger.error(f"데이터 파일이 없습니다: {data_csv_file_path}")
            return None

        historical_data_dataframe = pd.read_csv(data_csv_file_path, parse_dates=['날짜'])
        logger.debug(f"데이터 로드 완료: {len(historical_data_dataframe)} 행")

        # 이상치 분석 수행
        outlier_analysis_result = determine_if_latest_value_is_outlier(
            input_dataframe=historical_data_dataframe,
            target_column_name=analysis_column_name,
            analysis_period_days=historical_analysis_days,
            iqr_multiplier_threshold=statistical_threshold_multiplier,
        )

        logger.info(f"분석 완료: 이상치 여부 = {outlier_analysis_result}")
        return outlier_analysis_result

    except FileNotFoundError:
        logger.error(f"파일을 찾을 수 없습니다: {data_csv_file_path}")
        return None
    except pd.errors.EmptyDataError:
        logger.error(f"비어있는 데이터 파일: {data_csv_file_path}")
        return None
    except Exception as analysis_error:
        logger.error(f"데이터 분석 중 오류 발생: {analysis_error}")
        return None


# 하위 호환성을 위한 레거시 함수들
def check_kimchi_premium_outlier() -> bool:
    """
    레거시 호환성을 위한 함수 - 새로운 코드에서는 perform_kimchi_premium_outlier_analysis() 사용 권장
    """
    analysis_result = perform_kimchi_premium_outlier_analysis()
    return analysis_result if analysis_result is not None else False


# 하위 호환성을 위한 별칭들
analyze_kimchi_premium_outlier = perform_kimchi_premium_outlier_analysis
is_outlier = determine_if_latest_value_is_outlier
calculate_outlier_bounds = calculate_statistical_outlier_boundaries
filter_recent_data = filter_dataframe_by_recent_dates


def main():
    """
    메인 실행 함수
    """
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    try:
        analysis_result = perform_kimchi_premium_outlier_analysis()

        if analysis_result is None:
            print("오류: 데이터를 분석할 수 없습니다.")
            return 1
        elif analysis_result:
            print("True")
            print("김치 프리미엄이 이상치입니다!")
        else:
            print("False")
            print("김치 프리미엄이 정상 범위에 있습니다.")

        return 0

    except Exception as main_execution_error:
        print(f"예기치 못한 오류: {main_execution_error}")
        return 1


if __name__ == "__main__":
    exit(main())
