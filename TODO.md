# 遊戲化日語學習網站 — 開發任務計劃 (TODO.md)

> 狀態圖示：⬜ 待開始 ｜ 🔄 進行中 ｜ ✅ 完成 ｜ ❌ 封鎖/待確認

---

## Phase 1：專案骨架與環境搭建

> 目標：建立可運行的本地開發環境、Git 版本控管、基礎 Streamlit App 骨架。

| # | 任務 | 狀態 | 備註 |
|---|------|------|------|
| 1.1 | 初始化 Git repo，建立 `.gitignore`（忽略 `.env`、`__pycache__`、`.venv`） | ✅ | |
| 1.2 | 建立 Python 虛擬環境（`uv`），產出 `requirements.txt` | ✅ | google-genai 2.25.0, streamlit, sqlmodel, psycopg2-binary, pytest |
| 1.3 | 建立專案目錄結構（`app/`, `tests/`, `pages/`, `.streamlit/`） | ✅ | 詳見下方目錄樹 |
| 1.4 | 建立 `.streamlit/secrets.toml.example` 與根目錄 `.env.example`（含 `DATABASE_URL`, `GEMINI_API_KEY`, OAuth keys） | ✅ | |
| 1.5 | 建立最小可運行的 `app/main.py`（Streamlit Hello World，含 page config 與 sidebar 骨架） | ✅ | 含日系主題 CSS inject |
| 1.6 | 將專案推上 GitHub，確認 remote 連線正常 | ✅ | https://github.com/thomaschang710114/goodjp |

### Phase 1 目錄樹規劃
```
myvideo/                        ← 專案根目錄
├── app/
│   ├── main.py                 ← Streamlit 入口
│   ├── auth.py                 ← Google OAuth 處理
│   ├── database.py             ← SQLModel engine & session
│   ├── models/
│   │   ├── user.py
│   │   ├── order.py
│   │   ├── learning_content.py
│   │   ├── user_progress.py
│   │   └── leaderboard.py
│   ├── services/
│   │   ├── gemini_service.py   ← Gemini API 封裝
│   │   ├── score_service.py    ← 積分計算邏輯
│   │   └── quiz_service.py     ← 測驗生成邏輯
│   └── pages/
│       ├── 01_學習中心.py
│       ├── 02_測驗.py
│       ├── 03_排行榜.py
│       └── 04_個人儀表板.py
├── tests/
│   ├── conftest.py             ← pytest fixtures (in-memory SQLite DB)
│   ├── test_models.py
│   ├── test_score_service.py
│   ├── test_quiz_service.py
│   └── test_gemini_service.py
├── .streamlit/
│   ├── config.toml             ← Theme 設定
│   └── secrets.toml.example
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── TODO.md
```

---

## Phase 2：TDD 測試框架配置與資料庫模型設計

> 目標：建立 pytest 基礎設施，用 SQLModel 定義所有 DB Entity，確保 Schema 遷移可運行。

| # | 任務 | 狀態 | 備註 |
|---|------|------|------|
| 2.1 | 建立 `tests/conftest.py`：使用 In-Memory SQLite 作為測試 DB fixture，隔離 Production DB | ⬜ | TDD 基礎設施 |
| 2.2 | **[RED]** 撰寫 `tests/test_models.py`：測試 `User` model 建立、欄位驗證、unique email 約束 | ⬜ | 先寫測試，確認 FAIL |
| 2.3 | **[GREEN]** 實作 `app/models/user.py`（`User` SQLModel Table）：姓名、Email、頭像URL、總積分、上次上課時間、訂閱狀態 | ⬜ | 讓 2.2 測試通過 |
| 2.4 | **[GREEN]** 實作 `app/models/order.py`（`Order`）：訂單編號、用戶FK、訂單狀態、訂閱期限、付款方式、付款金額 | ⬜ | |
| 2.5 | **[GREEN]** 實作 `app/models/learning_content.py`（`LearningContent`）：影片URL、標題、Gemini逐字稿JSON、測驗題庫JSON、片段時間戳記 | ⬜ | |
| 2.6 | **[GREEN]** 實作 `app/models/user_progress.py`（`UserProgress`）：用戶FK、內容FK、完成度、歷史答題JSON、本單元獲得積分 | ⬜ | |
| 2.7 | **[GREEN]** 實作 `app/models/leaderboard.py`（`LeaderboardSnapshot`）：用戶FK、排名、積分快照、快照時間 | ⬜ | |
| 2.8 | 實作 `app/database.py`：建立 Neon PostgreSQL engine（讀取 secrets），`create_db_and_tables()` 函式 | ⬜ | **暫停：需你提供 Neon `DATABASE_URL`** |
| 2.9 | **[REFACTOR]** 撰寫所有 CRUD helper function 的測試，確認 Create/Read/Update 正常運作 | ⬜ | |

---

## Phase 3：Google OAuth 登入 與 積分核心邏輯 (TDD)

> 目標：完成會員驗證流程、積分計算服務、Session State 管理，全部有 pytest 覆蓋。

| # | 任務 | 狀態 | 備註 |
|---|------|------|------|
| 3.1 | **[RED]** 撰寫 `tests/test_score_service.py`：測試答對/答錯積分計算、連續答對 Bonus、單元完成積分 | ⬜ | 先寫測試 |
| 3.2 | **[GREEN]** 實作 `app/services/score_service.py`：積分計算函式（答對 +10, 答錯 0, 連續答對 Bonus +5, 單元完成 +50） | ⬜ | |
| 3.3 | **[RED]** 撰寫 `tests/test_quiz_service.py`：測試測驗題目格式驗證、選項洗牌、答案核對邏輯 | ⬜ | |
| 3.4 | **[GREEN]** 實作 `app/services/quiz_service.py`：題目格式 dataclass、選項隨機洗牌、答案核對 | ⬜ | |
| 3.5 | 實作 `app/auth.py`：整合 `st.login` Google OAuth，首次登入自動建立 `User` 資料庫紀錄 | ⬜ | **暫停：需你提供 OAuth Client ID/Secret** |
| 3.6 | 在 `app/main.py` 整合 `st.session_state` 管理：用戶登入狀態、當前學習單元、答題進度、積分暫存 | ⬜ | |
| 3.7 | **[REFACTOR]** 整合測試：模擬完整的「登入 → 開始學習 → 答題 → 獲得積分 → 寫入 DB」流程 | ⬜ | |

---

## Phase 4：Gemini AI 串接 與 核心學習 UI

> 目標：完成 Gemini 影片分析功能、四種測驗遊戲 UI、個人儀表板與排行榜。

| # | 任務 | 狀態 | 備註 |
|---|------|------|------|
| 4.1 | **[RED]** 撰寫 `tests/test_gemini_service.py`：Mock Gemini API 回應，測試逐字稿解析、題庫 JSON Schema 驗證 | ⬜ | 使用 `unittest.mock` |
| 4.2 | **[GREEN]** 實作 `app/services/gemini_service.py`：呼叫 Gemini API 傳入 YouTube URL，解析逐字稿與題庫結構 | ⬜ | **暫停：需你確認 GEMINI_API_KEY** |
| 4.3 | 實作 `pages/01_學習中心.py`：YouTube URL 輸入、Gemini 處理動畫、影片片段顯示（HTML5 Video + 倍速控制）、逐字稿顯示 | ⬜ | |
| 4.4 | 實作 `pages/02_測驗.py` — 聽力練習：播放音檔、四選一選擇題、即時回饋動畫 | ⬜ | |
| 4.5 | 實作 `pages/02_測驗.py` — 閱讀練習：顯示日語文字、選擇中文翻譯、即時回饋 | ⬜ | |
| 4.6 | 實作 `pages/02_測驗.py` — 單字/文法選擇題：情境題、正確答案解析展示 | ⬜ | |
| 4.7 | 實作 `pages/03_排行榜.py`：即時從 DB 讀取積分排名，表格 + 動態圖表（`st.bar_chart` 或 Plotly） | ⬜ | |
| 4.8 | 實作 `pages/04_個人儀表板.py`：用戶頭像、總積分、學習歷程時間軸、已完成單元列表、積分趨勢圖 | ⬜ | |
| 4.9 | **[REFACTOR]** UI 全站視覺一致性：套用自訂 `.streamlit/config.toml` 主題色（日系風格：深藍+紅+白）、自訂 CSS inject | ⬜ | |

---

## Phase 5：部署、CI 與收尾

> 目標：完成 GitHub Actions CI 自動測試、Streamlit Community Cloud 部署、README 文件。

| # | 任務 | 狀態 | 備註 |
|---|------|------|------|
| 5.1 | 建立 `.github/workflows/ci.yml`：Push/PR 時自動執行 `pytest`，確保所有測試通過才允許 merge | ⬜ | |
| 5.2 | 建立 `README.md`：專案介紹、Local 啟動步驟、環境變數說明、架構圖 | ⬜ | |
| 5.3 | 在 Streamlit Community Cloud 連結 GitHub repo，設定 Secrets（`DATABASE_URL`, `GEMINI_API_KEY`, OAuth keys） | ⬜ | **暫停：需你登入 Streamlit Cloud 授權** |
| 5.4 | 配置 Neon PostgreSQL Production DB，執行 `create_db_and_tables()` 初始化 Schema | ⬜ | |
| 5.5 | End-to-End 驗收測試：走完完整流程（登入 → 貼影片 → 測驗 → 獲得積分 → 查排行榜） | ⬜ | |
| 5.6 | 效能優化：為 `UserProgress` 與 `Leaderboard` 查詢加上 DB Index，`st.cache_data` 快取 Gemini 結果 | ⬜ | |

---

## 關鍵依賴與需要你提供的資訊清單

> 在正式開始各 Phase 前，以下資訊需要你確認提供：

| 需要的資訊 | 在哪個 Task 需要 | 狀態 |
|-----------|----------------|------|
| Neon PostgreSQL `DATABASE_URL` | Phase 2.8 | ⬜ 待提供 |
| Google `GEMINI_API_KEY` | Phase 4.2 | ⬜ 待提供 |
| Google OAuth `CLIENT_ID` & `CLIENT_SECRET` | Phase 3.5 | ⬜ 待提供 |
| GitHub Repo URL（或授權我建立） | Phase 1.6 | ⬜ 待提供 |
| Streamlit Community Cloud 帳號授權 | Phase 5.3 | ⬜ 待提供 |

---

## 開發節奏協議

- ✅ 每完成一個 Task，我會更新此 TODO.md 的狀態圖示
- 🔄 每次只推進一個 Task，完成後等你確認再繼續
- ❓ 遇到架構抉擇或金鑰需求，立即暫停並向你詢問
- 🧪 所有業務邏輯 Task 必須先有 RED 測試，才能寫實作程式碼
