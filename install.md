# 安裝範例

- `https://skillsmp.com/` 先到這邊找?
- `npx skills@latest add mattpocock/skills`
- `npx skills@latest add mattpocock/skills --skill=setup-matt-pocock-skills`

# 提示詞

```
# 角色與合作模式
你是一位資深的 FullStack Python 專家與 Streamlit 框架架構師。
我們即將從零開始構建一個「遊戲化日語學習網站」。你必須嚴格遵守以下**開發流程機制**：

## 開發流程與規範 (Execution Rules)
1. **規劃優先 (Plan First)**：在你撰寫任何專案程式碼之前，先根據以下需求，規劃一份詳細的 `TODO.md` 開發清單（分 Phase 與可測量的微型 Task）。**列出後暫停，等待我確認清單無誤。**
2. **單一步驟推進 (Step-by-Step)**：一次只執行 `TODO.md` 中的**一個**小任務。完成後，與我確認結果並更新 TODO 狀態，再進入下一個任務。
3. **TDD 測試驅動開發 (Test-Driven Development)**：
   - 在實作任何業務邏輯（如資料庫 CRUD、Gemini API 處理、分數計算與 Session State 狀態處理邏輯）前，**必須先撰寫對應的 `pytest` 單元測試**。
   - 確保測試會先失敗 (Red)，接著寫入最小可行性程式碼讓測試通過 (Green)，最後進行重構 (Refactor)。
4. **保持互動**：遇到需要環境變數（如 `.env` 密鑰、Database URL）、第三方 API 綁定或架構抉擇時，請執行的當下暫停並主動向我詢問。

---

# 專案需求規格 (Requirements)

## 1. 專案背景與目標
設計一個以遊戲互動方式增加學習樂趣的日語學習網站，主要目標受眾為初學者與赴日打工度假者。

## 2. 技術棧 (Tech Stack)
- **Frontend / Application Framework**: Streamlit (Python 快速 UI 框架)
- **State Management**: `st.session_state`
- **Database**: Neon PostgreSQL (搭配 SQLModel)
- **AI Service**: Google Gemini API (處理影片內容擷取與日語教材生成)
- **Testing**: `pytest` (執行 TDD，針對業務邏輯與 API 模組)
- **Deployment**: Streamlit Community Cloud

## 3. 功能需求細節

### A. 會員管理與權限
- Google OAuth 帳號登入整合（使用 Streamlit st.login），我會提供你相關的設定與金鑰)。
- 會員資料管理：姓名、Email、頭像、總積分、學習進度紀錄、上次上課時間、訂閱狀態。

### B. 核心學習體驗 (Core Game Loop)
1. **影片學習單元**：
   - 使用者貼上 YouTube 影片連結（範例影片以《你的名字》開頭）。
   - 後端調用 Gemini API 將影片內容擷取成 10–30 秒的日語學習短片段與逐字稿。
   - 提供影片播放/暫停、倍速控制功能（透過 `st.video` 或 HTML5 Video 元件）。
2. **遊戲化測驗 (3-5 個小遊戲/每單元)**：
   - **聽力練習**：播放日語音檔/短句，選擇對應文字。
   - **閱讀練習**：顯示日語文字，選擇中文翻譯。
   - **單字/文法選擇題**：根據情境選出適當日語。
   - **即時回饋**：答錯時顯示標準答案與詳細解析。
3. **獎勵與社群機制**：
   - 根據測驗表現發放積分，視覺化呈現在個人儀表板。
   - 即時積分排行榜 (Leaderboard)。

### C. 資料庫架構 (Database Entities)
- 設計時以 SQLModel 為主，並且欄位亦可使用中文
- `User` (會員基本資料、上次上課時間、訂閱狀態、總積分)
- `Order` (訂單編號、訂單狀態、訂閱期限、付款方式、付款金額)
- `LearningContent` (影片資料、Gemini 產出的句子與測驗題庫)
- `UserProgress` (使用者各單元完成度、歷史答題紀錄、獲得的積分)
- `Leaderboard/Score` (積分與排名快照)

---

# 部署與環境 (Deployment & Env)
1. 將專案上到 GitHub，以便我在地端開發也能管控版本
2. 本地開發優先：初期以本地端測試與 TDD 為主。
3. 環境變數：請在專案 `.streamlit/secrets.toml` 或根目錄 `.env` 進行配置，確保包含 `DATABASE_URL` 與 `GEMINI_API_KEY`。
4. 自動化部署：協助配置 Streamlit Community Cloud 部署設定。

---

# 現在的第一步行動
請**不要**直接撰寫程式碼。請先回答我，並產出這份專案的 **`TODO.md` 完整任務拆解計劃**，劃分成 4~5 個 Phase（從環境搭建、TDD 測試配置、資料庫設計，到 UI 與 AI 串接），等待我確認。
```