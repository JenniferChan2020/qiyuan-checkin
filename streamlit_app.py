# -*- coding: utf-8 -*-
"""
元气修复 · 健康打卡（网页版 v3）
配色：浅灰 + 淡粉 | 功能性 Emoji 图标 | 打卡项带时间、按时间分组
特性：
  - 首页打卡项带「时间点」，按 晨起/上午/下午/傍晚/睡前 分组，时间后显示当天星期几
  - 打卡项 可搜索 / 可添加 / 可编辑 / 可删除
  - 运动 Tab：每天的具体动作逐项拆分，可勾选打卡
"""
import streamlit as st
import json, os
from datetime import date, datetime

DATA_FILE = "checkin_data.json"

WEEKDAY_CN = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

# ---------------- 默认打卡清单（带时间点）----------------
# time: 建议完成时间；group: 时间段分组；icon: 功能性图标
DEFAULT_TASKS = [
    {"time": "07:00", "group": "🌅 晨起",   "icon": "🌅", "title": "起床（固定时间）",   "sub": "锚定生物钟",       "cat": "作息"},
    {"time": "07:10", "group": "🌅 晨起",   "icon": "💧", "title": "一杯温水",           "sub": "唤醒代谢",         "cat": "作息"},
    {"time": "07:30", "group": "🌅 晨起",   "icon": "☀️", "title": "见光10分钟",         "sub": "调节褪黑素",       "cat": "作息"},
    {"time": "08:00", "group": "🌅 晨起",   "icon": "🍳", "title": "早餐（蛋白质+主食）","sub": "补气血·供脑",     "cat": "饮食"},
    {"time": "09:00", "group": "☀️ 上午",   "icon": "🧠", "title": "用脑50分钟休息10分钟","sub": "护脑·防过劳",     "cat": "用脑"},
    {"time": "10:00", "group": "☀️ 上午",   "icon": "💧", "title": "喝水500ml",          "sub": "代谢",            "cat": "饮食"},
    {"time": "12:00", "group": "☀️ 上午",   "icon": "🥗", "title": "午餐（主食换杂粮）", "sub": "控血糖",          "cat": "饮食"},
    {"time": "12:30", "group": "☀️ 上午",   "icon": "🍇", "title": "甜食只在饭后吃",     "sub": "抗糖化",          "cat": "饮食"},
    {"time": "15:00", "group": "🌤️ 下午",   "icon": "🥬", "title": "吃深色蔬菜",         "sub": "补抗氧",          "cat": "饮食"},
    {"time": "15:30", "group": "🌤️ 下午",   "icon": "👀", "title": "20-20-20 护眼",      "sub": "用眼休息",        "cat": "用脑"},
    {"time": "17:00", "group": "🌤️ 下午",   "icon": "🏃", "title": "运动30分钟",         "sub": "燃脂·紧致",       "cat": "运动"},
    {"time": "17:40", "group": "🌤️ 下午",   "icon": "💪", "title": "运动后补蛋白质",     "sub": "修复肌肉",        "cat": "运动"},
    {"time": "19:00", "group": "🌆 傍晚",   "icon": "🍲", "title": "晚餐（早·清淡）",    "sub": "控晚糖",          "cat": "饮食"},
    {"time": "20:30", "group": "🌙 睡前",   "icon": "🫁", "title": "腹式呼吸5分钟",      "sub": "补气·安神",       "cat": "气血"},
    {"time": "21:00", "group": "🌙 睡前",   "icon": "👣", "title": "按揉太冲穴2分钟",    "sub": "疏肝治叹气",      "cat": "气血"},
    {"time": "21:30", "group": "🌙 睡前",   "icon": "💆", "title": "梳头100下",          "sub": "醒脑·助眠",       "cat": "作息"},
    {"time": "21:30", "group": "🌙 睡前",   "icon": "📵", "title": "屏幕调暗",           "sub": "褪黑素保护",      "cat": "作息"},
    {"time": "22:00", "group": "🌙 睡前",   "icon": "🛌", "title": "23:00前护肤入睡",    "sub": "养肝血·修复",     "cat": "作息"},
]

# 时间段分组顺序
GROUP_ORDER = ["🌅 晨起", "☀️ 上午", "🌤️ 下午", "🌆 傍晚", "🌙 睡前"]

# 一周运动计划：每天拆成若干具体动作，逐项打卡
WEEK_PLAN = [
    ("周一", "🏃 有氧", "★", [
        "热身5分钟（开合跳/原地踏步）",
        "快走/慢跑 30分钟",
        "拉伸5分钟",
    ]),
    ("周二", "💪 上肢+核心", "★★", [
        "热身5分钟",
        "俯卧撑 3组×12",
        "平板支撑 3组×30秒",
        "卷腹 3组×15",
    ]),
    ("周三", "🧘 休息·恢复", "★", [
        "散步30分钟",
        "全身拉伸15分钟",
        "深呼吸3分钟",
    ]),
    ("周四", "💪 下肢+臀", "★★", [
        "热身5分钟",
        "深蹲 3组×15",
        "箭步蹲 3组×12（每侧）",
        "臀桥 3组×15",
    ]),
    ("周五", "🔥 HIIT", "★★★", [
        "热身5分钟",
        "开合跳 40秒×4",
        "高抬腿 40秒×4",
        "波比跳 10个",
        "拉伸5分钟",
    ]),
    ("周六", "🧘 瑜伽·放松", "★★", [
        "猫牛式 3组",
        "婴儿式 3组",
        "下犬式 3组",
        "婴儿式放松3分钟",
    ]),
    ("周日", "🚶 轻活动", "★", [
        "散步 + 深呼吸",
        "全身轻拉伸",
        "按摩小腿",
    ]),
]

# 可选的图标池(功能性 emoji 图标)
ICON_POOL = "🌅☀️🌤️🌆🌙💧🍳🥗🍇🥬🍲🫁👣💆🧠👀🏃💪📵🛌🍵✨🌿🥑🐟🌰🍎"


# ---------------- 数据层 ----------------
def load_json(f, default):
    if os.path.exists(f):
        try:
            with open(f, encoding="utf-8") as fh:
                return json.load(fh)
        except Exception:
            pass
    return default


def save_json(f, d):
    with open(f, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=2)


# 打卡项清单
if "tasks" not in st.session_state:
    if os.path.exists(DATA_FILE):
        try:
            st.session_state.tasks = json.load(open(DATA_FILE, encoding="utf-8"))
        except Exception:
            st.session_state.tasks = list(DEFAULT_TASKS)
    else:
        st.session_state.tasks = list(DEFAULT_TASKS)
    if not isinstance(st.session_state.tasks, list) or not st.session_state.tasks:
        st.session_state.tasks = list(DEFAULT_TASKS)
    save_json(DATA_FILE, st.session_state.tasks)

# 通用打卡记录 {日期: [勾选的打卡项索引]}
if "records" not in st.session_state:
    st.session_state.records = {}
# 运动打卡记录 {日期: [完成动作索引]} —— 与通用记录分开，避免索引串号
if "ex_records" not in st.session_state:
    st.session_state.ex_records = {}
if "kw" not in st.session_state:
    st.session_state.kw = ""


def persist_tasks():
    save_json(DATA_FILE, st.session_state.tasks)


today = str(date.today())
weekday_today = WEEKDAY_CN[date.today().weekday()]  # 今天的星期几
done_today = st.session_state.records.get(today, [])
ex_done_today = st.session_state.ex_records.get(today, [])

# 今天的训练（根据星期几取对应一天）
today_plan_idx = date.today().weekday()  # 0=周一
today_plan = WEEK_PLAN[today_plan_idx]


# ---------------- 淡粉主题 CSS（无卡通水豚）----------------
st.markdown("""
<style>
.stApp { background:#F2F3F5; font-family:-apple-system,"PingFang SC","Roboto","Noto Sans CJK SC",sans-serif; }
.main .block-container { max-width:540px; margin:auto; padding:0 0 90px 0; }

/* 顶部横幅 */
.kb-banner {
    background:linear-gradient(135deg,#FFE3EC 0%,#FFD0DE 55%,#F2F3F5 100%);
    border-radius:0 0 26px 26px; padding:24px 22px 18px; text-align:center;
    box-shadow:0 3px 14px rgba(240,140,170,.18);
}
.kb-banner h1 { font-size:20px; font-weight:800; color:#6B4A55; margin:6px 0 2px; }
.kb-banner p { font-size:12px; color:#A88A96; margin:0; }
.stProgress > div > div > div { background:linear-gradient(90deg,#FF9BB5,#FFB6C8); border-radius:8px; }

/* 搜索框 / 按钮 */
.stTextInput > div > input {
    background:#fff; border:1.5px solid #FFD0DE; border-radius:14px; color:#6B4A55;
    padding:10px 14px; font-size:15px;
}
.stTextInput > div > input:focus { border-color:#FF9BB5; box-shadow:none; }
.stButton > button {
    background:#FFE3EC; color:#C56B85; border:1.5px solid #FFD0DE; border-radius:14px;
    font-weight:600; transition:.15s;
}
.stButton > button:hover { background:#FFD0DE; }

/* 时间段分组标题 */
.kb-group { color:#6B4A55; font-size:14px; font-weight:800; margin:18px 16px 4px;
    display:flex; align-items:center; gap:6px; }
.kb-group .gw { font-size:12px; color:#C56B85; background:#FFE3EC; padding:2px 10px; border-radius:10px; margin-left:auto; }

/* 打卡卡片 */
.kb-card {
    background:#fff; border-radius:18px; padding:12px 14px; margin:8px 12px;
    box-shadow:0 2px 10px rgba(150,120,130,.08);
    display:flex; align-items:center; gap:11px;
}
.kb-card .capy { font-size:26px; width:34px; text-align:center; flex-shrink:0; }
.kb-card .txt { flex:1; min-width:0; }
.kb-card .t { font-size:15px; font-weight:600; color:#4A3B42; }
.kb-card .s { font-size:12px; color:#A88A96; margin-top:2px; }
.kb-card .time { font-size:13px; font-weight:700; color:#E96B8F; }
.kb-card .del { color:#D88; font-size:17px; cursor:pointer; padding:4px 6px; }

/* 圆形复选框 */
.kb-check { appearance:none; -webkit-appearance:none; width:26px; height:26px;
    border:2px solid #E8C8D2; border-radius:50%; outline:none; cursor:pointer;
    position:relative; background:#fff; transition:.15s; flex-shrink:0; }
.kb-check:checked { background:#FF9BB5; border-color:#FF9BB5; }
.kb-check:checked::after { content:"✓"; color:#fff; font-size:15px; font-weight:800;
    position:absolute; left:6px; top:1px; }

.kb-card.done .t { text-decoration:line-through; color:#B5A6AC; }
.kb-card.done .s { color:#C8BCBF; }
.kb-tag { font-size:11px; background:#FFE3EC; color:#C56B85; padding:2px 8px; border-radius:10px; }

/* 底部导航 tabs */
.stTabs [data-baseweb="tab-list"] { position:fixed; bottom:0; left:0; right:0;
    background:#fff; box-shadow:0 -2px 12px rgba(150,120,130,.12); z-index:99;
    max-width:540px; margin:auto; padding:6px 0; justify-content:space-around; }
.stTabs [data-baseweb="tab"] { font-size:11px; color:#A88A96; gap:3px; }
.stTabs [aria-selected="true"] { color:#E96B8F; font-weight:700; }

@media (max-width:640px){ .main .block-container{padding-bottom:80px;} }
.kb-h { color:#6B4A55; font-size:17px; font-weight:800; margin:16px 14px 4px; text-align:center; }
</style>
""", unsafe_allow_html=True)


# ---------------- 顶部横幅 ----------------
st.markdown(f"""
<div class="kb-banner">
  <h1>元气修复 · 健康打卡</h1>
  <p>{datetime.now().strftime('%Y年%m月%d日')} {weekday_today} · 慢慢来，比较快</p>
</div>
""", unsafe_allow_html=True)


# ================= 首页：今日打卡（按时间分组）=================
def render_home():
    # 进度
    total = len(st.session_state.tasks)
    done_cnt = sum(1 for i, t in enumerate(st.session_state.tasks) if i in done_today)
    st.progress(done_cnt / total if total else 0)
    streak = 0
    d = date.today()
    while str(d) in st.session_state.records and st.session_state.records[str(d)]:
        streak += 1
        d = d.fromordinal(d.toordinal() - 1)
    st.caption(f"今日完成 {done_cnt}/{total} · 连续打卡 {streak} 天 🔥")

    # 搜索框
    st.session_state.kw = st.text_input(
        "🔍 搜索打卡项（名称 / 分类）", value=st.session_state.kw,
        placeholder="如：运动、气血、饮食…")
    kw = st.session_state.kw.strip().lower()

    # 添加新项
    with st.expander("➕ 添加打卡项"):
        c1, c2 = st.columns([1, 2])
        with c1:
            new_icon = st.selectbox("图标", list(ICON_POOL))
            new_time = st.text_input("建议时间", value="12:00")
        with c2:
            new_title = st.text_input("名称")
        new_sub = st.text_input("说明（选填）")
        new_cat = st.selectbox("分类", ["作息", "饮食", "运动", "气血", "用脑"])
        if st.button("✅ 确认添加", use_container_width=True):
            if new_title.strip():
                st.session_state.tasks.append({
                    "time": new_time.strip() or "12:00",
                    "group": "🌤️ 下午",
                    "icon": new_icon, "title": new_title.strip(),
                    "sub": new_sub.strip(), "cat": new_cat,
                })
                persist_tasks()
                st.rerun()

    # 按时间排序（冒泡保证稳定）
    indexed = list(enumerate(st.session_state.tasks))
    indexed.sort(key=lambda x: x[1].get("time", "99:99"))

    # 按时间段分组渲染
    rendered_groups = set()
    for i, t in indexed:
        if kw and kw not in t["title"].lower() and kw not in t.get("cat", "").lower():
            continue
        grp = t.get("group", "🌤️ 下午")
        if grp not in rendered_groups:
            rendered_groups.add(grp)
            # 该分组已完成数
            group_tasks = [x for x in indexed if x[1].get("group") == grp]
            group_done = sum(1 for x in group_tasks if x[0] in done_today)
            st.markdown(
                f"<div class='kb-group'>{grp}<span class='gw'>{group_done}/{len(group_tasks)}</span></div>",
                unsafe_allow_html=True)
        _render_task_card(i, t)

    _render_editor()


def _render_task_card(i, t):
    is_done = i in done_today
    time_label = f"{t.get('time','')} {weekday_today}"
    col_check, col_body, col_del = st.columns([0.5, 4.2, 0.6])
    with col_check:
        checked = st.checkbox(
            f"完成 {t['title']}", value=is_done, key=f"chk_{i}",
            label_visibility="hidden")
        if checked and not is_done:
            done_today.append(i); st.session_state.records[today] = done_today; persist_tasks()
        elif not checked and is_done:
            done_today.remove(i); st.session_state.records[today] = done_today; persist_tasks()
    with col_body:
        st.markdown(f"""<div class='kb-card {"done" if is_done else ""}'>
          <div class='capy'>{t.get('icon','🌿')}</div>
          <div class='txt'><div class='t'>{t['title']}</div>
          <div class='s'><span class='time'>{time_label}</span> · {t.get('sub','')} <span class='kb-tag'>{t.get('cat','')}</span></div></div>
        </div>""", unsafe_allow_html=True)
    with col_del:
        if st.button("🗑️", key=f"del_{i}", help="删除"):
            st.session_state.tasks.pop(i)
            persist_tasks()
            for k in st.session_state.records:
                st.session_state.records[k] = [
                    x if x < i else x - 1 for x in st.session_state.records[k] if x != i]
            st.rerun()


def _render_editor():
    if "edit_idx" in st.session_state and st.session_state.edit_idx < len(st.session_state.tasks):
        idx = st.session_state.edit_idx
        t = st.session_state.tasks[idx]
        st.divider()
        st.markdown("**✏️ 编辑打卡项**")
        t["icon"] = st.selectbox("图标", list(ICON_POOL), index=ICON_POOL.index(t.get("icon", "🌿")), key="e_icon")
        t["time"] = st.text_input("建议时间", value=t.get("time", "12:00"), key="e_time")
        t["title"] = st.text_input("名称", value=t["title"], key="e_title")
        t["sub"] = st.text_input("说明", value=t.get("sub", ""), key="e_sub")
        t["cat"] = st.selectbox("分类", ["作息", "饮食", "运动", "气血", "用脑"], index=["作息", "饮食", "运动", "气血", "用脑"].index(t.get("cat", "饮食")), key="e_cat")
        if st.button("💾 保存修改", use_container_width=True):
            st.session_state.tasks[idx] = t
            persist_tasks()
            del st.session_state.edit_idx
            st.rerun()
    # 每张卡片的编辑按钮（放卡片下方不破坏 flex 布局）
    for i in range(len(st.session_state.tasks)):
        if st.session_state.get(f"edit_{i}"):
            st.session_state.edit_idx = i
            st.rerun()


# ================= 食谱 =================
def render_meals():
    st.markdown('<div class="kb-h">🍱 本周食谱 · 补气血抗糖</div>', unsafe_allow_html=True)
    meals = [
        ("周一", "🍳 燕麦+蛋2个+红枣3颗+黑咖｜🍲 杂粮饭+猪肝炒菠菜+西兰花｜🥗 番茄炖牛腩+紫甘蓝+小米粥"),
        ("周二", "🍳 全麦三明治+黑咖｜🍲 荞麦面+卤牛肉+木耳｜🥗 清蒸鲈鱼+蒜蓉菠菜+红薯"),
        ("周三", "🍳 红枣枸杞豆浆+全麦+蛋｜🍲 糙米+当归炖鸡+时蔬｜🥗 豆腐羹+芝麻菠菜+玉米"),
        ("周四", "🍳 桂圆莲子银耳羹+蛋+馒头｜🍲 杂粮饭+红烧带鱼+莴笋｜🥗 牛肉汤+荞麦面"),
        ("周五", "🍳 黑芝麻糊+蛋2个+坚果｜🍲 藜麦饭+香菇滑鸡+西兰花｜🥗 清蒸虾+海带+小米粥"),
        ("周六", "🍳 红枣桂圆粥+蛋+核桃｜🍲 牛肉胡萝卜饺子+汤｜🥗 番茄鸡蛋面+黄瓜"),
        ("周日", "🍳 枸杞豆浆+全麦+蛋｜🍲 杂粮饭+当归羊肉汤+时蔬｜🥗 清蒸鱼+紫薯+沙拉"),
    ]
    for w, m in meals:
        st.markdown(f"<div class='kb-card'><div class='capy'>🍱</div><div class='txt'><div class='t'>{w}</div><div class='s'>{m}</div></div></div>", unsafe_allow_html=True)
    st.info("💡 猪肝每周1-2次（补血首选）；菠菜先焯水；甜食只放饭后。")


# ================= 运动：逐项打卡 =================
def render_exercise():
    st.markdown('<div class="kb-h">🏃 运动计划 · 逐项打卡</div>', unsafe_allow_html=True)

    # 一周总览（哪些天已完成）
    cols = st.columns(7)
    for ci, (w, _, _, _) in enumerate(WEEK_PLAN):
        day_str = _weekday_to_date(w)
        done_days = sum(1 for _ in range(1))  # placeholder
        cols[ci].caption(f"{w[:2]}")
    st.caption(" ")

    # 今天的训练（可打卡主体）
    day_name, kind, level, actions = today_plan
    st.markdown(f"<div class='kb-card'><div class='capy'>{kind.split()[0]}</div>"
                f"<div class='txt'><div class='t'>{day_name} · {kind[2:]}</div>"
                f"<div class='s'>难度 {level} · 完成 {len(ex_done_today)}/{len(actions)} 个动作</div></div></div>",
                unsafe_allow_html=True)
    st.progress(len(ex_done_today) / len(actions) if actions else 0)

    for ai, act in enumerate(actions):
        col_check, col_body = st.columns([0.5, 5])
        is_done = ai in ex_done_today
        with col_check:
            checked = st.checkbox(
                f"完成 {act}", value=is_done, key=f"ex_{ai}",
                label_visibility="hidden")
            if checked and not is_done:
                ex_done_today.append(ai); st.session_state.ex_records[today] = ex_done_today; st.rerun()
            elif not checked and is_done:
                ex_done_today.remove(ai); st.session_state.ex_records[today] = ex_done_today; st.rerun()
        with col_body:
            done_cls = "done" if is_done else ""
            mark = "✅" if is_done else "⭕"
            st.markdown(
                f"<div class='kb-card {done_cls}'>"
                f"<div class='capy'>{mark}</div>"
                f"<div class='txt'><div class='t'>{act}</div></div></div>",
                unsafe_allow_html=True)

    if len(ex_done_today) == len(actions):
        st.success("今天的训练全部完成，燃脂+紧致 💪")
        # 联动：运动完成 → 首页"运动30分钟"自动勾上
        for i, t in enumerate(st.session_state.tasks):
            if "运动30分钟" in t["title"] and i not in done_today:
                done_today.append(i); st.session_state.records[today] = done_today; persist_tasks()
                break

    st.warning("⚠️ 运动时间建议 16:00-19:00；睡前2小时避免剧烈运动。运动后30分钟内补蛋白质。")

    # 本周完整计划（展示，不可打卡，便于提前了解）
    with st.expander("📅 查看本周完整计划"):
        for w, kind, level, actions in WEEK_PLAN:
            day_str = _weekday_to_date(w)
            rec = st.session_state.ex_records.get(day_str, [])
            finished = len(rec) == len(actions) and actions
            st.markdown(f"**{w} {kind}** {'✅' if finished else ''}")
            for a in actions:
                st.markdown(f"- {a}")
            st.markdown("")


def _weekday_to_date(weekday_name):
    """把「周一」…「周日」映射到本周对应的日期字符串"""
    target = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"].index(weekday_name)
    today_w = date.today().weekday()
    delta = target - today_w
    return str(date.today().fromordinal(date.today().toordinal() + delta))


# ================= 气血专项 =================
def render_qixue():
    st.markdown('<div class="kb-h">🌸 气血 & 脑疲劳专项</div>', unsafe_allow_html=True)
    tips = [
        ("叹气多=肝郁", "👣", "每天按揉太冲穴（脚背大拇趾与二趾缝间）2分钟，配合深呼吸"),
        ("补气", "🫁", "腹式呼吸：吸4秒→屏2秒→呼6秒，早晚各5分钟，激活副交感神经"),
        ("护脑", "🧠", "用脑50分钟强制休息10分钟；每用眼20分钟看6米外20秒（20-20-20）"),
        ("醒脑", "💆", "木梳从前额梳到后颈100下；促进头部血液循环"),
        ("养肝血", "🛌", "23点前入睡，23:00-3:00肝胆经当令，生长激素分泌达白天5-10倍"),
    ]
    for title, icon, desc in tips:
        st.markdown(f"<div class='kb-card'><div class='capy'>{icon}</div><div class='txt'><div class='t'>{title}</div><div class='s'>{desc}</div></div></div>", unsafe_allow_html=True)


# ================= 统计 =================
def render_stats():
    st.markdown('<div class="kb-h">📊 打卡统计</div>', unsafe_allow_html=True)
    streak = 0
    d = date.today()
    while str(d) in st.session_state.records and st.session_state.records[str(d)]:
        streak += 1
        d = d.fromordinal(d.toordinal() - 1)
    st.metric("🔥 连续打卡天数", streak)

    total = len(st.session_state.tasks)
    import pandas as pd
    rows = []
    for i in range(6, -1, -1):
        dd = str(date.fromordinal(date.today().toordinal() - i))
        rec = st.session_state.records.get(dd, [])
        # 完成率 = 通用打卡 + 运动打卡(折算)
        ex_rec = st.session_state.ex_records.get(dd, [])
        ex_total = len(WEEK_PLAN[date.fromisoformat(dd).weekday()][3]) if dd in st.session_state.ex_records else 0
        done = len(rec) + (len(ex_rec) if ex_total else 0)
        base = total + (ex_total if ex_total else 0)
        rows.append((f"{dd[5:]} {WEEKDAY_CN[date.fromisoformat(dd).weekday()]}", done / base if base else 0))
    df = pd.DataFrame(rows, columns=["日期", "完成率"])
    st.bar_chart(df.set_index("日期"))
    st.caption("柱越高代表当天完成度越高（1.0 = 全部完成）")

    if streak >= 7:
        st.success("坚持一周了，气血正在慢慢回来 🌟")
    if streak >= 28:
        st.balloons()
        st.success("28天一个皮肤代谢周期，你已经完成一个完整轮回！")


# ---------------- 底部导航 ----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 打卡", "🍱 食谱", "🏃 运动", "🌸 气血", "📊 统计"])
with tab1:
    render_home()
with tab2:
    render_meals()
with tab3:
    render_exercise()
with tab4:
    render_qixue()
with tab5:
    render_stats()
