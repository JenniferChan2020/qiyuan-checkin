import streamlit as st
import json, os
from datetime import date, datetime

# ---------- 数据层 ----------
DATA_FILE = "checkin_data.json"
TASKS = [
    ("没喝奶茶/甜饮料", "抗糖化·护脸"),
    ("吃了深色蔬菜", "补抗氧"),
    ("主食换了一半杂粮", "控血糖"),
    ("23点前护肤躺下", "养肝血"),
    ("运动30分钟", "燃脂·紧致"),
    ("按揉太冲穴2分钟", "疏肝治叹气"),
    ("腹式呼吸5分钟", "补气"),
    ("用脑50分钟休10分钟", "护脑"),
    ("梳头100下", "醒脑"),
    ("吃补气血食材(枣/桂圆/猪肝)", "补血"),
    ("喝够水1500ml", "代谢"),
    ("没熬夜到凌晨", "修复"),
]

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            return json.load(open(DATA_FILE))
        except:
            pass
    return {}

def save_data(d):
    json.dump(d, open(DATA_FILE, "w"), ensure_ascii=False, indent=2)

data = load_data()
today = str(date.today())
done_today = data.get(today, [])

# ---------- Keep 风格 CSS ----------
st.markdown("""
<style>
/* 全局底色 + 字体 */
.stApp { background:#F6F7F9; font-family:-apple-system,"PingFang SC","Roboto",sans-serif; }
.main .block-container { padding:0 0 80px 0; max-width:480px; margin:auto; }

/* 顶部渐变横幅 */
.keep-banner {
    background:linear-gradient(135deg,#00C853 0%,#00E676 100%);
    color:#fff; padding:28px 20px 22px; border-radius:0 0 22px 2222px;
    border-bottom-left-radius:22px; border-bottom-right-radius:22px;
}
.keep-banner h1 { font-size:22px; font-weight:800; margin:0; letter-spacing:1px; }
.keep-banner p { margin:6px 0 0; opacity:.92; font-size:13px; }

/* 卡片 */
.keep-card {
    background:#fff; border-radius:18px; padding:14px 16px; margin:10px 14px;
    box-shadow:0 2px 10px rgba(0,0,0,.05); display:flex; align-items:center; justify-content:space-between;
}
.keep-card .t { font-size:15px; font-weight:600; color:#2B2B33; }
.keep-card .s { font-size:12px; color:#9A9AA5; margin-top:2px; }

/* 隐藏原生 checkbox，画 Keep 绿勾 */
.stCheckbox > label { display:flex; align-items:center; gap:10px; }
.stCheckbox input { appearance:none; -webkit-appearance:none; width:22px; height:22px;
    border:2px solid #D5D7DD; border-radius:7px; outline:none; transition:.15s; position:relative; }
.stCheckbox input:checked { background:#00C853; border-color:#00C853; }
.stCheckbox input:checked::after { content:"✓"; color:#fff; font-size:14px; font-weight:700;
    position:absolute; left:5px; top:1px; }

/* 进度条配色 */
.stProgress > div > div > div { background:#00C853; }

/* tabs 伪装底部导航 */
.stTabs [data-baseweb="tab-list"] { position:fixed; bottom:0; left:0; right:0;
    background:#fff; box-shadow:0 -2px 10px rgba(0,0,0,.06); z-index:99;
    padding:6px 0; justify-content:space-around; max-width:480px; margin:auto; }
.stTabs [data-baseweb="tab"] { font-size:12px; color:#9A9AA5; }
.stTabs [aria-selected="true"] { color:#00C853; font-weight:700; }

/* 移动端单列 */
@media (max-width:640px){ .main .block-container{padding-bottom:70px;} }
</style>
""", unsafe_allow_html=True)

# ---------- 顶部横幅 ----------
st.markdown(f"""
<div class="keep-banner">
  <h1>元气修复 · 自律给我自由</h1>
  <p>{datetime.now().strftime('%Y年%m月%d日')} · 36岁焕新计划</p>
</div>
""", unsafe_allow_html=True)

# ---------- 主体 tabs ----------
tab1, tab2, tab3, tab4, tab5 = st.tabs(["首页","食谱","运动","气血","统计"])

with tab1:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    # 进度
    done_cnt = sum(1 for i,_ in enumerate(TASKS) if i in done_today)
    st.progress(done_cnt/len(TASKS))
    streak = 0
    d = date.today()
    while str(d) in data and data[str(d)]:
        streak += 1
        d = d.fromordinal(d.toordinal()-1)
    st.caption(f"今日完成 {done_cnt}/{len(TASKS)} · 连续打卡 {streak} 天🔥")
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    for i,(title,sub) in enumerate(TASKS):
        col1, col2 = st.columns([1,5])
        with col1:
            checked = st.checkbox("", value=i in done_today, key=f"t{i}")
        with col2:
            st.markdown(f"<div class='keep-card'><div><div class='t'>{title}</div><div class='s'>{sub}</div></div></div>", unsafe_allow_html=True)
        if checked and i not in done_today:
            done_today.append(i); data[today]=done_today; save_data(data)
        elif not checked and i in done_today:
            done_today.remove(i); data[today]=done_today; save_data(data)

with tab2:
    st.subheader("本周食谱（补气血·抗糖）")
    week = ["周一","周二","周三","周四","周五","周六","周日"]
    meals = [
        "早餐：燕麦+鸡蛋2个+红枣3颗+黑咖｜午餐：杂粮饭+猪肝炒菠菜+紫甘蓝｜晚餐：豆腐+西兰花",
        "早餐：全麦+水煮蛋+桂圆枸杞茶｜午餐：糙米+牛肉+芥蓝｜晚餐：蒸蛋+凉拌黑木耳",
        "早餐：小米粥+核桃+桑葚一把｜午餐：荞麦面+鸡胸+胡萝卜丝｜晚餐：鱼+菠菜",
        "早餐：酸奶+蓝莓+黑芝麻｜午餐：杂粮饭+虾仁+西兰花｜晚餐：冬瓜汤+少量瘦肉",
        "早餐：燕麦+蛋+枣｜午餐：糙米+牛腩+青菜｜晚餐：豆腐脑+凉拌黄瓜",
        "早餐：全麦+蛋+枸杞水｜午餐：红薯+鱼+紫甘蓝｜晚餐：银耳羹+少量坚果",
        "轻断食日：蔬菜汤+鸡蛋1个+水果少量，不碰甜点奶茶",
    ]
    for w,m in zip(week,meals):
        st.marked = st.markdown(f"<div class='keep-card'><div><div class='t'>{w}</div><div class='s'>{m}</div></div></div>", unsafe_allow_html=True)

with tab3:
    st.subheader("7天运动（跟练明细）")
    plan = [
        ("周一 有氧","快走/慢跑30分 + 拉伸10分"),
        ("周二 上肢+核心","俯卧撑3×10 · 平板3×30秒 · 卷腹3×15"),
        ("周三 休息","散步20分 + 全身拉伸"),
        ("周四 下肢+臀","深蹲3×15 · 箭步蹲3×12 · 臀桥3×15"),
        ("周五 HIIT","开合跳30秒×4 · 高抬腿30秒×4 · 休息1分循环"),
        ("周六 瑜伽","猫牛式/婴儿式/下犬 各3组，共30分"),
        ("周日 休息","散步 + 按摩小腿"),
    ]
    for t,d in plan:
        st.markdown(f"<div class='keep-card'><div><div class='t'>{t}</div><div class='s'>{d}</div></div></div>", unsafe_allow_html=True)

with tab4:
    st.subheader("气血 & 脑疲劳专项")
    tips = [
        ("叹气多=肝郁","每天按揉太冲穴（脚背大拇趾与二趾缝间）2分钟，配合深呼吸"),
        ("脑疲劳","用脑50分钟强制休10分钟；看远处20秒×3次（20-20-20）"),
        ("补气","腹式呼吸：吸4 屏2 呼6，早晚各5分钟"),
        ("养面色","木梳从前额梳到后颈100下；23点前卧床"),
        ("补血食材","红枣、桂圆、桑葚、猪肝（每周1-2次）、黑芝麻、菠菜焯水"),
    ]
    for t,d in tips:
        st.markdown(f"<div class='keep-card'><div><div class='t'>{t}</div><div class='s'>{d}</div></div></div>", unsafe_allow_html=True)

with tab5:
    st.subheader("近7天完成率")
    import pandas as pd
    rows=[]
    for i in range(6,-1,-1):
        dd = str(date.fromordinal(date.today().toordinal()-i))
        cnt = len(data.get(dd,[]))
        rows.append((dd, cnt/len(TASKS)))
    df = pd.DataFrame(rows, columns=["日期","完成率"])
    st.bar_chart(df.set_index("日期"))
    st.caption("坚持28天，皮肤代谢周期走完一轮，镜子会说话。")
