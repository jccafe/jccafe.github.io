# github_html 專案專屬 AI Agent 規則

本文件定義了未來 Agent 在開發或維護 `github_html` 專案時必須遵守的規範與限制。

## 1. 專案背景與技術棧
* **專案定位**：`jccafe.github.io` 網站目錄自動化生成與 Git 部署工具。
* **技術棧**：Python 3.10+、Git CLI。
* **依賴管理**：必須使用 `uv` 進行虛擬環境管理與套件安裝。執行 Python 程式一律使用 `uv run <script_y>`。

## 2. 開發限制與規範
* **自動部署流程**：
  * 當使用者要求「更新目錄」或「執行部署」時，必須嚴格依序執行：
    1. `git pull origin <當前分支>`
    2. `uv run generate_index.py` (或 `python generate_index.py` 確保在虛擬環境中)
    3. `git add .` (或特定變更檔案)
    4. `git commit -m "Auto-update index"`
    5. `git push origin <當前分支>`
* **合併衝突 (Merge Conflict) 處理**：
  * 執行 `git pull` 時若回傳 Exit Code 非 0 或提示衝突，**必須立即暫停所有後續動作**。
  * 嚴禁嘗試自動合併衝突或使用 `git checkout --ours/theirs` 強行解決。
  * 必須輸出明確的紅色警告字樣，提示使用者：「偵測到 Git 合併衝突，請手動解決衝突後再繼續執行部署。」
* **目錄掃描規範**：
  * 當更新或重構 `generate_index.py` 時，掃描邏輯必須明確排除以下資料夾，以防將非公開網頁或系統檔案寫入目錄：
    * `.git/`、`.venv/`、`docs/`、`.agents/`、`__pycache__/` 等。

## 3. 回覆與輸出規範
* 所有的日誌、回報訊息與錯誤提示，均應使用**繁體中文 (zh-TW)**。
* 在終端機執行指令成功後，應印出美觀的成功摘要（例如使用 Unicode 符號如 `✅`、`🚀` 裝飾）。
