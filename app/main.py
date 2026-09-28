"""
日語學習網站 — 主入口
"""

import streamlit as st

# ── 頁面設定（必須是第一個 st 指令）──────────────────────────────────────────
st.set_page_config(
    page_title="日語冒險學院 🎌",
    page_icon="🎌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 全站自訂 CSS ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;700&family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', 'Noto Sans JP', sans-serif;
    }

    /* 漸層標題 */
    .hero-title {
        background: linear-gradient(135deg, #E63946 0%, #F4A261 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    /* 積分徽章 */
    .score-badge {
        background: linear-gradient(135deg, #0077B6, #023E8A);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(0, 119, 182, 0.4);
    }

    /* 卡片效果 */
    .card {
        background: rgba(27, 42, 59, 0.8);
        border: 1px solid rgba(230, 57, 70, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(230, 57, 70, 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Session State 初始化 ──────────────────────────────────────────────────────
def init_session_state():
    """初始化所有全域 session state 預設值"""
    defaults = {
        "user": None,           # 登入後的 User 物件
        "is_logged_in": False,
        "current_unit": None,   # 當前學習單元 ID
        "quiz_state": {},       # 答題進度 {question_id: answer}
        "session_score": 0,     # 本次 session 暫存積分
        "streak": 0,            # 連續答對數
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎌 日語冒險學院")
    st.divider()

    if st.session_state.is_logged_in and st.session_state.user:
        user = st.session_state.user
        st.markdown(f"👤 **{user.get('name', '學習者')}**")
        st.markdown(
            f'<span class="score-badge">⭐ {st.session_state.session_score} 積分</span>',
            unsafe_allow_html=True,
        )
        st.divider()
        if st.button("🚪 登出", use_container_width=True):
            st.session_state.is_logged_in = False
            st.session_state.user = None
            st.rerun()
    else:
        st.info("請登入以開始學習 🗝️")
        if st.button("🔑 Google 登入", use_container_width=True, type="primary"):
            # TODO Phase 3.5：整合 st.login
            st.session_state.is_logged_in = True
            st.session_state.user = {"name": "測試用戶", "email": "test@example.com"}
            st.rerun()

    st.divider()
    st.caption("v0.1.0 · Phase 1 骨架")


# ── 主頁面 ────────────────────────────────────────────────────────────────────
st.markdown('<h1 class="hero-title">日語冒險學院 🎌</h1>', unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:#A8B2C1; font-size:1.1rem;'>"
    "透過影片與遊戲，輕鬆學會日語 · 每天進步一點點</p>",
    unsafe_allow_html=True,
)
st.divider()

# 三欄功能入口卡片
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="card">
            <h3>📺 影片學習</h3>
            <p style="color:#A8B2C1;">貼上 YouTube 連結，AI 自動生成學習內容與測驗</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="card">
            <h3>🎮 遊戲測驗</h3>
            <p style="color:#A8B2C1;">聽力、閱讀、單字三種遊戲，答題獲得積分</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="card">
            <h3>🏆 排行榜</h3>
            <p style="color:#A8B2C1;">與其他學習者競爭，登上全球排行榜頂端</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# 快速狀態面板（登入後顯示）
if st.session_state.is_logged_in:
    st.subheader("📊 你的學習狀況")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("總積分", "0", delta=None)
    m2.metric("完成單元", "0")
    m3.metric("連續天數", "1 天")
    m4.metric("排名", "—")
else:
    st.info("👈 請先從左側登入，開始你的日語冒險！")
