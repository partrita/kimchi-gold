import csv
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from kimchi_gold.config import DATA_FILE
from kimchi_gold.now_price import calc_kimchi_premium, PriceScrapingError


def is_today_logged(filename: Path) -> bool:
    """오늘 날짜(YYYY-MM-DD)가 이미 파일에 기록되어 있으면 True 반환"""
    if not filename.exists():
        return False
    today_str: str = datetime.now().strftime("%Y-%m-%d")
    with filename.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            next(reader, None)  # 헤더 스킵
        except StopIteration:
            return False # 파일이 비어있는 경우
        for row in reader:
            if row and row[0].startswith(today_str):
                return True
    return False


def write_to_csv(row: List[str], filename: Path = DATA_FILE) -> None:
    file_exists: bool = filename.exists() and filename.stat().st_size > 0
    with filename.open(mode="a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            # 헤더 작성
            writer.writerow(
                [
                    "날짜",
                    "국내금(원/g)",
                    "국제금(달러/온스)",
                    "환율(원/달러)",
                    "김치프리미엄(원/g)",
                    "김치프리미엄(%)",
                ]
            )
        writer.writerow(row)


def collect_data() -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if is_today_logged(DATA_FILE):
        print("오늘 데이터가 이미 존재합니다. 수집을 중단합니다.")
        return
    try:
        result: Tuple[float, float, float, float, float, float] = calc_kimchi_premium()
        domestic, international, _, usdkrw, diff, premium = result
        today: str = datetime.now().strftime("%Y-%m-%d")
        row: List[str] = [
            today,
            f"{domestic:.2f}",
            f"{international:.2f}",
            f"{usdkrw:.2f}",
            f"{diff:.2f}",
            f"{premium:.2f}",
        ]
        write_to_csv(row)
        print(f"수집 완료: {row}")
    except PriceScrapingError as e:
        print(f"수집 실패: {e}")
    except Exception as e:
        print(f"알 수 없는 오류로 수집 실패: {e}")

if __name__ == "__main__":
    collect_data()
