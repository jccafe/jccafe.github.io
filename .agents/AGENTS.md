# github_html 專案專屬 AI Agent 開發規則

本文件定義了未來 Agent 在開發、維護或重構 `github_html` 專案時必須遵守的規範與限制。

---

## 1. 專案背景與技術棧
* **專案定位**：`jccafe.github.io` 網站目錄自動化生成、監控與部署工具。
* **技術棧**：Python 3.10+、Git CLI、GitHub Actions。
* **環境與套件管理**：必須使用 `uv` 進行虛擬環境管理與套件安裝。執行本機 Python 程式一律使用 `uv run <script.py>`。

---

## 2. 開發限制與規範

### 2.1 自動部署與 Git 流程
* **執行命令序列**：自動部署必須嚴格依序執行：
  1. `git pull origin <當前分支>`
  2. `uv run generate_index.py` (確保重新生成最新目錄)
  3. `git add .`
  4. `git commit -m "Auto-update index"` (若無檔案變更，須能優雅退出，避免 commit 失敗中斷)
  5. `git push origin <當前分支>`
* **合併衝突與預檢防禦**：
  * 執行 Git 指令前，必須先執行預檢，確保當前目錄為 Git 儲存庫 (`git rev-parse --is-inside-work-tree`)，若非，應給予友善提示並中斷。
  * 執行 `git pull` 時若回傳 Exit Code 非 0 或是提示衝突，**必須立即暫停所有後續動作**。
  * 嚴禁嘗試自動合併衝突。必須輸出明確的紅色警告字樣，提示使用者：「[Warning] 偵測到 Git 合併衝突，請手動解決衝突後再繼續執行部署。」

### 2.2 目錄掃描與排版規範
* **資料夾掃描排除**：當修改或重構 `generate_index.py` 時，掃描邏輯必須明確排除以下資料夾，以防將非公開網頁或系統檔案寫入目錄：
  * `.git/`、`.venv/`、`docs/`、`.agents/`、`__pycache__/`、`node_modules/` 等。
* **兩欄式導覽佈局 (Premium UI)**：
  * 產出的 `index.html` 必須維持**兩欄式導覽**：左欄為固定的磨砂玻璃資料夾導覽側邊欄 (Sidebar)，右欄為對應卡片區。
  * **RWD 響應式**：當螢幕寬度小於 `900px` 時，左側導覽必須自適應轉換為頂部橫向水平滑動的導覽 Tab 欄。
  * **JS 智慧聯動**：必須保留「平滑滾動定位」、「Scrollspy 滾動選單追蹤高亮（行動端 Active 項目自動滾動對齊至螢幕中心）」以及「兩欄同步搜尋過濾與隱藏」功能。

### 2.3 雲端自動更新 (GitHub Actions)
* 工作流配置於 `.github/workflows/update-index.yml`。
* 任何對 `generate_index.py` 的修改，皆不可破壞雲端 Actions 的執行相容性（避免導入 Actions 不支援的外部 OS 特性）。
* Actions 機器人在自動 commit & push 時，必須加上 `[skip ci]` 標記，且觸發路徑中必須排除 `index.html` 本身，嚴防無窮迴圈觸發。

---

## 3. 控制台輸出與回覆規範
* **解決 Windows 控制台 CP950 編碼問題**：
  * **重要禁忌**：嚴禁直接在終端機 print CP950 不支援的 Unicode 特殊表情圖示（如 `✅`、`🚀`、`🎉` 等），以免在預設為 CP950 的 Windows 終端機下拋出 `UnicodeEncodeError` 崩潰。
  * **替代方案**：使用標準文字標記（如 `[OK]`, `[Deploy]`, `[Success]`, `[Warning]`）做為提示。
  * **編碼重設**：所有 Python 腳本開頭必須配置自適應編碼重組，確保中文輸出正常：
    ```python
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        try: sys.stdout.reconfigure(encoding='utf-8')
        except Exception: pass
    ```
* **語言要求**：所有的日誌、回報訊息與錯誤提示，均應使用**繁體中文 (zh-TW)**。
