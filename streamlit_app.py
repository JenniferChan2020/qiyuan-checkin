# -*- coding: utf-8 -*-
"""
元气修复 · 专属健康打卡应用（网页版）
适配：36岁、熬夜、嗜甜、运动少、气血不足、爱叹气、脑疲劳
部署：Streamlit Cloud，入口文件 streamlit_app.py
数据：localStorage（浏览器本地），不依赖后端
"""
import streamlit as st
import json
import os
from datetime import date, timedelta

st.set_page_config(
    page_title="元气修复 · 健康打卡",
    page_icon="🌿",
    layout="wide",
)

DATA_FILE = "checkin_data.json"


# ---------- 数据持久化（本地文件，多用户共享写入） ----------
def load_data():
    default = {"records": {}, "streak": 0}
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            if isinstance(loaded, dict):
                default.update(loaded)
            if "records" not in default or not isinstance(default["records"], dict):
                default["records"] = {}
            return default
        except Exception:
            pass
    return default


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


data = load_data()
today_str = str(date.today())


def get_today_tasks():
    return data["records"].get(today_str, {})


def save_today_tasks(tasks):
    data.setdefault("records", {})[today_str] = tasks
    save_data(data)


today_tasks = get_today_tasks()

# ---------- 任务定义 ----------
TASK_GROUPS = [
    ("🌅 晨起", [
        ("wake", "7:00 起床（固定时间）"),
        ("water", "一杯温水"),
        ("sun", "见光10分钟（锚定生物钟）"),
    ]),
    ("🍽️ 饮食（抗糖·补气血）", [
        ("sugar", "没喝奶茶/甜饮料"),
        ("sweet", "甜食只在饭后吃"),
        ("veg", "吃了深色蔬菜"),
        ("blood", "补气血食材（红枣/桂圆/猪肝/桑葚）"),
    ]),
    ("🏃 运动", [
        ("exercise", "运动30分钟"),
    ]),
    ("🌸 气血 & 脑疲劳专项", [
        ("breathe", "腹式呼吸5分钟"),
        ("taichong", "按揉太冲穴2分钟（治叹气）"),
        ("brain", "用脑50分钟休息10分钟"),
        ("comb", "梳头100下"),
    ]),
    ("🌙 睡前", [
        ("screen", "睡前90分钟屏幕调暗"),
        ("skincare", "23:00 前护肤·入睡"),
    ]),
]


# ---------- 侧边栏：日期切换 ----------
st.sidebar.title("🌿 元气修复")
selected = st.sidebar.date_input("查看日期", value=date.today())
sel_str = str(selected)
if sel_str != today_str:
    st.sidebar.info("历史日期为只读模式，打卡请在今日完成")

# 统计：连续打卡天数
records = data.get("records", {})
sorted_days = sorted(records.keys())
streak = 0
d = date.today()
while str(d) in records and any(records[str(d)].values()):
    streak += 1
    d -= timedelta(days=1)

st.sidebar.metric("🔥 连续打卡", f"{streak} 天")
st.sidebar.caption("气血恢复是慢功夫，坚持28天见分晓")

# ---------- 页面导航 ----------
page = st.sidebar.radio(
    "导航",
    ["📋 今日打卡", "🍱 本周食谱", "🏃 运动计划", "🛒 采购清单", "🌸 气血专项", "📊 统计"],
)

# ================= 今日打卡 =================
if page == "📋 今日打卡":
    st.title("📋 今日打卡")
    st.caption(f"{today_str}  ·  气血不足 · 脑疲劳 · 抗糖作息")
    total = sum(len(tasks) for _, tasks in TASK_GROUPS)
    done = sum(1 for _, tasks in TASK_GROUPS for _, key in tasks if today_tasks.get(key))
    st.progress(done / total if total else 0)
    st.write(f"**{done} / {total}** 已完成")

    edited = dict(today_tasks)
    changed = False
    for group_name, tasks in TASK_GROUPS:
        with st.expander(group_name, expanded=True):
            for key, label in tasks:
                val = st.checkbox(label, value=bool(today_tasks.get(key, False)), key=f"{today_str}_{key}")
                if val != bool(edited.get(key, False)):
                    edited[key] = val
                    changed = True
    if changed:
        save_today_tasks(edited)
        st.success("已保存 ✅")

    if done == total:
        st.balloons()
        st.success("全部完成，今日元气 +1 🌟")

# ================= 食谱 =================
elif page == "🍱 本周食谱":
    st.title("🍱 本周食谱")
    st.caption("原则：抗糖（低GI）+ 补气血 + 健脑")
    week = {
        "周一": {
            "早餐": "红枣桂圆燕麦粥 + 水煮蛋2个 + 核桃2颗",
            "午餐": "杂粮饭 + 菠菜炒猪肝 + 清炒西兰花",
            "晚餐": "番茄炖牛腩 + 紫甘蓝沙拉 + 小米粥",
            "加餐": "桑葚/蓝莓一小把",
        },
        "周二": {
            "早餐": "全麦三明治（鸡胸+生菜）+ 黑咖啡",
            "午餐": "荞麦面 + 卤牛肉 + 凉拌木耳",
            "晚餐": "清蒸鲈鱼 + 蒜蓉菠菜 + 红薯",
            "加餐": "85%黑巧一小块",
        },
        "周三": {
            "早餐": "红枣枸杞豆浆 + 全麦面包 + 水煮蛋",
            "午餐": "糙米饭 + 当归生姜炖鸡 + 炒时蔬",
            "晚餐": "豆腐羹 + 芝麻菠菜 + 玉米",
            "加餐": "一小把杏仁",
        },
        "周四": {
            "早餐": "桂圆莲子银耳羹 + 鸡蛋 + 全麦馒头",
            "午餐": "杂粮饭 + 红烧带鱼 + 清炒莴笋",
            "晚餐": "牛肉蔬菜汤 + 荞麦面",
            "加餐": "一个苹果",
        },
        "周五": {
            "早餐": "黑芝麻糊 + 水煮蛋2个 + 坚果",
            "午餐": "藜麦饭 + 香菇滑鸡 + 蒜蓉西兰花",
            "晚餐": "清蒸虾 + 凉拌海带 + 小米粥",
            "加餐": "蓝莓/桑葚",
        },
        "周六": {
            "早餐": "红枣桂圆粥 + 鸡蛋 + 核桃",
            "午餐": "饺子（牛肉胡萝卜）+ 蔬菜汤",
            "晚餐": "番茄鸡蛋面（少油）+ 凉拌黄瓜",
            "加餐": "一小把腰果",
        },
        "周日": {
            "早餐": "枸杞豆浆 + 全麦面包 + 水煮蛋",
            "午餐": "杂粮饭 + 当归羊肉汤 + 炒时蔬",
            "晚餐": "清蒸鱼 + 紫薯 + 蔬菜沙拉",
            "加餐": "一个橙子",
        },
    }
    tabs = st.tabs(list(week.keys()))
    for tab, (day, meals) in zip(tabs, week.items()):
        with tab:
            for meal, content in meals.items():
                st.write(f"**{meal}**：{content}")
    st.info("💡 猪肝每周1-2次（补血首选）；菠菜先焯水去草酸；甜食只放饭后。")

# ================= 运动计划 =================
elif page == "🏃 运动计划":
    st.title("🏃 运动计划")
    st.caption("每周3次有氧 + 2次力量 + 1次瑜伽，循序渐进")
    plan = [
        ("周一", "🏃 有氧", "快走/慢跑 30分钟 + 热身5分钟 + 拉伸5分钟", "★★★"),
        ("周二", "💪 上肢+核心", "俯卧撑 3组×12 + 平板支撑 3组×30秒 + 卷腹 3组×15", "★★★"),
        ("周三", "🧘 休息·瑜伽", "散步30分钟 + 全身拉伸15分钟（恢复为主）", "★"),
        ("周四", "💪 下肢+臀", "★ 深蹲 3组×15 + 弓步蹲 3组×12 + 臀桥 3组×15", "★★★"),
        ("周五", "🔥 HIIT", "开合跳 40秒×4 + 高抬腿 40秒×4 + 波比跳 10个", "★★★★"),
        ("周六", "🧘 瑜伽·放松", "阴瑜伽30分钟（重点：开髋、肩颈放松）", "★★"),
        ("周日", "🚶 休息", "散步 + 深呼吸（不安排剧烈运动）", "★"),
    ]
    for day, kind, detail, level in plan:
        with st.expander(f"{day}  {kind}  {level}"):
            st.write(detail)
    st.warning("⚠️ 运动时间建议 16:00-19:00（体温峰值，表现最好）；睡前2小时避免剧烈运动。运动后30分钟内补充蛋白质。")

# ================= 采购清单 =================
elif page == "🛒 采购清单":
    st.title("🛒 一周采购清单")
    st.caption("超市一次买齐，★ 为补气血重点食材")
    shopping = {
        "🌾 主食": ["★ 红枣", "★ 桂圆/龙眼干", "★ 黑芝麻", "★ 桑葚干", "燕麦", "糙米/黑米", "藜麦", "荞麦面", "红薯/紫薯", "全麦面包"],
        "🥩 蛋白质": ["★ 猪肝（每周1-2次）", "牛肉", "鸡胸/鸡腿", "鲈鱼/带鱼/虾", "鸡蛋", "豆腐/豆浆", "牛奶/希腊酸奶"],
        "🥬 蔬菜": ["★ 菠菜（焯水）", "西兰花", "紫甘蓝", "木耳", "胡萝卜", "番茄", "莴笋", "海带"],
        "🍇 水果·坚果": ["★ 桑葚", "★ 枸杞", "蓝莓", "苹果", "橙子", "核桃", "杏仁", "腰果", "85%黑巧"],
        "🧂 调味·其他": ["当归（少量）", "生姜", "大蒜", "橄榄油", "蜂蜜（少量）"],
    }
    for cat, items in shopping.items():
        with st.expander(cat):
            for item in items:
                st.checkbox(item, key=f"shop_{item}")

# ================= 气血专项 =================
elif page == "🌸 气血专项":
    st.title("🌸 气血 & 脑疲劳专项")
    st.caption("专为你：气血不足 · 容易叹气 · 大脑疲劳 · 用脑过度")
    tips = [
        ("🌬️ 腹式呼吸（补气）", "吸气4秒 → 屏息2秒 → 呼气6秒，每天早晚各5分钟。深长呼吸能激活副交感神经，缓解疲劳、改善面色。"),
        ("👣 按揉太冲穴（治叹气）", "脚背第1、2跖骨之间凹陷处。每天按揉2分钟，疏肝理气——叹气多属『肝郁气滞』，此穴是特效。"),
        ("🧠 用脑50分钟休息10分钟", "每专注50分钟，强制起身活动、看远处。大脑连续高负荷会耗气伤神，规律休息反而效率更高。"),
        ("👀 20-20-20 法则", "每用眼20分钟，看20英尺（6米）外，持续20秒。缓解眼疲劳，也打断久坐。"),
        ("💇 梳头100下（醒脑）", "用木梳从额前梳至后颈，每天100下。促进头部血液循环，醒脑安神，也有助于睡眠。"),
        ("😴 23点前入睡（养肝血）", "23:00-3:00 是肝胆经当令，深睡期生长激素分泌是白天5-10倍，直接关系皮肤修复与气血恢复。"),
    ]
    for title, desc in tips:
        with st.expander(title):
            st.write(desc)
    st.success("🌿 气血恢复口诀：早睡、深呼吸、少叹气、多动、吃够蛋白质。")

# ================= 统计 =================
elif page == "📊 统计":
    st.title("📊 打卡统计")
    st.metric("🔥 连续打卡天数", streak)
    # 近7天完成率
    st.subheader("近7天完成情况")
    chart_data = {}
    for i in range(6, -1, -1):
        d = date.today() - timedelta(days=i)
        ds = str(d)
        rec = records.get(ds, {})
        total = sum(len(t) for _, t in TASK_GROUPS)
        done = sum(1 for _, tasks in TASK_GROUPS for _, k in tasks if rec.get(k))
        chart_data[ds[5:]] = done / total if total else 0
    st.bar_chart(chart_data)
    st.caption("柱越高代表当天完成度越高（1.0 = 全部完成）")

    # 分类统计
    st.subheader("各分类累计完成率")
    cat_stats = {}
    for group_name, tasks in TASK_GROUPS:
        done = 0
        total = len(tasks) * len(records)
        for ds, rec in records.items():
            done += sum(1 for _, k in tasks if rec.get(k))
        cat_stats[group_name] = done / total if total else 0
    st.bar_chart(cat_stats)

    if streak >= 7:
        st.success("坚持一周了，气血正在慢慢回来 🌟")
    if streak >= 28:
        st.balloons()
        st.success("28天一个皮肤代谢周期，你已经完成一个完整轮回！")
