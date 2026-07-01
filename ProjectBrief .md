# 專案啟動需求單 (Project Brief)

這是一份由 Antigravity Bootstrapper 產生的自動化需求表單。

## 1. 基礎資訊
- **專案名稱**：github_html
- **建立時間**：2026-07-01

## 2. 目標概述 (Goal)
更新 jccafe.github.io 的網站目錄

## 3. 預期功能 (Features)
[角色任務]：你現在是我的自動化部署助理。
[背景資訊]：我要更新 jccafe.github.io 的網站目錄。
[具體指令]：請依序在終端機執行以下操作：1. 執行 git pull 確保本地端為最新版本。2. 執行 python generate_index.py 重新生成網頁目錄。3. 將變更透過 git add .、git commit -m "Auto-update index" 與 git push 推送回 GitHub。
[約束條件]：請直接執行上述終端機指令，並在完成後回報執行結果。若遇到合併衝突（Merge Conflict），請暫停動作並提醒我手動處理。

## 4. 參考資源 (References)
請 AI (Agent) 在開始撰寫企畫與架構前，務必透過工具讀取並理解以下資源：

*(無外部參考連結)*

## 5. Agent 執行指令 (Next Steps)
收到此文件後，請 Agent 依序執行以下步驟：
1. 詳細閱讀並理解上述目標與參考資源。
2. 在 `docs/spec/` 下建立 `企劃書.md` 與 `規格書.md`。
3. 在 `docs/sdd/` 下建立 `系統設計文件.md` (SDD)。
4. 建立 `task.md` 列出第一階段的開發步驟清單。
5. 在 `.agents/` 建立 `AGENTS.md` 寫入適合此專案的 AI 開發提示詞 (Prompts)。
