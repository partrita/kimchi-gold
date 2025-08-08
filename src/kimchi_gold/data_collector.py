"""
금 가격 데이터를 수집하고 CSV 파일에 저장하는 모듈입니다.
"""

import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from .configuration import GOLD_PRICE_DATA_CSV_FILE, CSV_COLUMN_HEADERS
from .data_models import GoldPriceData
from .price_fetcher import fetch_current_gold_market_data

# 로깅 설정
logger = logging.getLogger(__name__)


def check_if_date_already_logged(
    csv_file_path: Path = GOLD_PRICE_DATA_CSV_FILE, 
    target_date_to_check: Optional[datetime] = None
) -> bool:
    """
    지정된 날짜가 이미 파일에 기록되어 있으면 True 반환
    
    Args:
        csv_file_path: 확인할 CSV 파일 경로
        target_date_to_check: 확인할 날짜 (기본값: 오늘)
        
    Returns:
        날짜가 기록되어 있으면 True, 없으면 False
    """
    if not csv_file_path.exists():
        logger.debug(f"File {csv_file_path} does not exist")
        return False
        
    if target_date_to_check is None:
        target_date_to_check = datetime.now()
        
    target_date_string = target_date_to_check.strftime("%Y-%m-%d")
    
    try:
        with csv_file_path.open("r", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader, None)  # 헤더 스킵
            for data_row in csv_reader:
                if data_row and data_row[0].startswith(target_date_string):
                    logger.debug(f"Found existing data for {target_date_string}")
                    return True
        logger.debug(f"No data found for {target_date_string}")
        return False
        
    except Exception as file_read_error:
        logger.error(f"Error reading file {csv_file_path}: {file_read_error}")
        return False


def save_gold_price_data_to_csv(
    gold_price_data_object: GoldPriceData, 
    output_csv_file_path: Path = GOLD_PRICE_DATA_CSV_FILE
) -> None:
    """
    GoldPriceData 객체를 CSV 파일에 저장합니다.
    
    Args:
        gold_price_data_object: 저장할 금 가격 데이터
        output_csv_file_path: 저장할 CSV 파일 경로
        
    Raises:
        IOError: 파일 쓰기 실패 시
    """
    try:
        file_already_exists = output_csv_file_path.exists()
        
        with output_csv_file_path.open(mode="a", encoding="utf-8", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            
            # 파일이 없으면 헤더 작성
            if not file_already_exists:
                csv_writer.writerow(CSV_COLUMN_HEADERS)
                logger.debug(f"Created new CSV file with headers: {output_csv_file_path}")
                
            # 데이터 행 작성
            data_row_for_csv = gold_price_data_object.convert_to_csv_row_format()
            csv_writer.writerow(data_row_for_csv)
            logger.info(f"Data written to {output_csv_file_path}: {data_row_for_csv}")
            
    except Exception as file_write_error:
        logger.error(f"Failed to write data to {output_csv_file_path}: {file_write_error}")
        raise IOError(f"파일 쓰기 실패: {file_write_error}")


def collect_and_save_current_gold_market_data(
    output_csv_file_path: Path = GOLD_PRICE_DATA_CSV_FILE, 
    skip_if_data_already_exists: bool = True
) -> bool:
    """
    현재 금 가격 데이터를 수집하고 CSV 파일에 저장합니다.
    
    Args:
        output_csv_file_path: 데이터를 저장할 CSV 파일 경로
        skip_if_data_already_exists: 오늘 날짜 데이터가 이미 있으면 스킵할지 여부
        
    Returns:
        성공적으로 수집했으면 True, 실패하면 False
    """
    try:
        # 오늘 날짜 데이터 존재 여부 확인
        if skip_if_data_already_exists and check_if_date_already_logged(output_csv_file_path):
            logger.info("오늘 날짜 데이터가 이미 존재합니다. 수집을 스킵합니다.")
            return True
            
        # 금 가격 데이터 수집
        logger.info("금 가격 데이터 수집 시작")
        current_gold_market_data = fetch_current_gold_market_data()
        
        # CSV 파일에 저장
        save_gold_price_data_to_csv(current_gold_market_data, output_csv_file_path)
        
        logger.info(
            f"데이터 수집 완료: 김치 프리미엄 {current_gold_market_data.kimchi_premium_percent:.2f}%"
        )
        return True
        
    except Exception as collection_error:
        logger.error(f"데이터 수집 실패: {collection_error}")
        return False


# 하위 호환성을 위한 레거시 함수들
def write_to_csv(row_data: List[str], csv_file_path: Path = GOLD_PRICE_DATA_CSV_FILE) -> None:
    """
    레거시 호환성을 위한 함수 - 새로운 코드에서는 save_gold_price_data_to_csv() 사용 권장
    """
    try:
        file_already_exists = csv_file_path.exists()
        with csv_file_path.open(mode="a", encoding="utf-8", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            if not file_already_exists:
                csv_writer.writerow(CSV_COLUMN_HEADERS)
            csv_writer.writerow(row_data)
    except Exception as legacy_write_error:
        logger.error(f"Legacy write_to_csv failed: {legacy_write_error}")
        raise


def collect_data() -> None:
    """
    레거시 호환성을 위한 함수 - 새로운 코드에서는 collect_and_save_current_gold_market_data() 사용 권장
    """
    collection_success = collect_and_save_current_gold_market_data()
    if collection_success:
        if check_if_date_already_logged(GOLD_PRICE_DATA_CSV_FILE):
            print("오늘 데이터가 이미 존재합니다. 수집을 중단합니다.")
        else:
            print("수집 완료")
    else:
        print("수집 실패")


# 하위 호환성을 위한 별칭들
collect_current_gold_data = collect_and_save_current_gold_market_data
write_gold_data_to_csv = save_gold_price_data_to_csv
is_today_logged = check_if_date_already_logged


def main():
    """
    메인 실행 함수
    """
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        collection_success = collect_and_save_current_gold_market_data()
        if collection_success:
            print("금 가격 데이터 수집이 성공적으로 완료되었습니다.")
            return 0
        else:
            print("금 가격 데이터 수집에 실패했습니다.")
            return 1
    except Exception as main_execution_error:
        print(f"예기치 못한 오류 발생: {main_execution_error}")
        return 1


if __name__ == "__main__":
    exit(main())
