import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd
import datetime, os
from config import CSV_PATH

# 日本語フォント（Windows用）
rcParams['font.family'] = 'MS Gothic'

def generate_monthly_graph():
    if not os.path.exists(CSV_PATH):
        return None

    df = pd.read_csv(CSV_PATH)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date

    # 直近30日
    today = datetime.date.today()
    month_ago = today - datetime.timedelta(days=29)
    df_month = df[df["date"] >= month_ago]

    # 日ごとの集計（NaN→0, 数値型に変換）
    meal_daily = (
        df_month[df_month["type"]=="meal"]
        .groupby("date")["meal_eaten"]
        .sum()
        .fillna(0)
        .astype(float)
    )
    weight_daily = (
        df_month[df_month["type"]=="weight"]
        .groupby("date")["value"]
        .last()
    )

    # 値を数値化（"3.5kg"→3.5）
    weight_daily = weight_daily.str.replace("kg", "", regex=False).astype(float)

    fig, ax1 = plt.subplots(figsize=(12,4))
    ax1.set_title("月次 猫の実食量と体重推移")
    ax1.set_xlabel("日付")
    ax1.set_ylabel("実食量(g)")

    # 棒グラフとして描画（棒幅を0.6に調整）
    ax1.bar(meal_daily.index, meal_daily.values, width=0.6, color="orange", label="実食量(g)")

    # 体重は折れ線
    ax2 = ax1.twinx()
    ax2.set_ylabel("体重(kg)")
    ax2.plot(weight_daily.index, weight_daily.values, marker="o", color="blue", label="体重(kg)")

    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()

    img_path = os.path.join(os.path.dirname(__file__), "..", "data", "monthly_summary.png")
    plt.savefig(img_path)
    plt.close(fig)
    return img_path
