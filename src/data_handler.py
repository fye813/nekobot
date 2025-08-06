import csv, os, datetime
from config import CSV_PATH

# 初期化
if not os.path.exists(CSV_PATH):
    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp","user","type","value","flag_complete",
            "meal_given","meal_left","meal_eaten"
        ])

def append_csv(user, type_, value, flag=True, meal_given=None, meal_left=None):
    meal_eaten = None
    if meal_given is not None:
        left = meal_left or 0
        meal_eaten = meal_given - left
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CSV_PATH, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp,user,type_,value,flag,meal_given,meal_left,meal_eaten])

def update_meal_left(left_g:int):
    rows = []
    updated = False
    with open(CSV_PATH,"r",encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    for row in reversed(rows):
        if row["type"] == "meal":
            given = int(row["meal_given"]) if row["meal_given"] else 0
            eaten = given - left_g
            row["meal_left"] = str(left_g)
            row["meal_eaten"] = str(eaten)
            row["value"] = f"給与{given}g/残{left_g}g/実食{eaten}g"
            updated = True
            break
    if updated:
        with open(CSV_PATH,"w",encoding="utf-8",newline="") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
    return updated

def daily_summary(date_str:str):
    if not os.path.exists(CSV_PATH):
        return "記録なし"
    with open(CSV_PATH,"r",encoding="utf-8") as f:
        reader = csv.DictReader(f)
        records = [r for r in reader if r["timestamp"].startswith(date_str)]
    meal = [r for r in records if r["type"]=="meal"]
    water = [r for r in records if r["type"]=="water"]
    toilet = [r for r in records if r["type"]=="toilet"]
    weight = [r for r in records if r["type"]=="weight"]

    total_given = sum(int(r["meal_given"] or 0) for r in meal)
    total_left = sum(int(r["meal_left"] or 0) for r in meal)
    total_eaten = sum(int(r["meal_eaten"] or 0) for r in meal)
    latest_weight = weight[-1]["value"] if weight else "なし"

    msg = f"🐾 {date_str} の記録\n"
    msg += f"✅ 餌やり: 給与{total_given}g / 残{total_left}g / 実食{total_eaten}g\n" if meal else "❌ 餌やり: 実施無\n"
    msg += f"✅ 水替え: {len(water)}回\n" if water else "❌ 水替え: 実施無\n"
    msg += f"✅ トイレ掃除: {len(toilet)}回\n" if toilet else "❌ トイレ掃除: 実施無\n"
    msg += f"✅ 体重測定: 最新 {latest_weight}\n" if weight else "❌ 体重測定: 実施無\n"
    return msg
