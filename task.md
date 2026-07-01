# github_html 開發任務清單 (TODO)

## Phase 1: 基礎架構與文件配置 (已完成)
- [x] 閱讀與分析 `ProjectBrief .md` 需求
- [x] 建立專案企劃書 (`docs/spec/企劃書.md`)
- [x] 建立專案規格書 (`docs/spec/規格書.md`)
- [x] 建立系統設計文件 SDD (`docs/sdd/系統設計文件.md`)
- [x] 建立 AI Agent 規則配置 (`.agents/AGENTS.md`)
- [x] 初始化專案任務清單 (`task.md`)

## Phase 2: 自動化部署與目錄生成實作 (已完成)
- [x] 檢查與設定 Python 虛擬環境 (`.venv`)
  - [x] 執行 `uv venv` 初始化虛擬環境
- [x] 檢查與實作 `generate_index.py` 腳本
  - [x] 撰寫輕量、具備 Glassmorphism 樣式與搜尋功能的目錄生成腳本
- [x] 實作 Git 自動化腳本/流程
  - [x] 撰寫自動化部署腳本 `deploy.py`
  - [x] 實作 Git 合併衝突與無 Git 儲存庫的預檢防錯機制
- [x] 本地整合測試
  - [x] 模擬正常流程執行，成功生成並更新 `index.html` 目錄
  - [x] 模擬無 Git 儲存庫異常，確認腳本能友善警告並終止流程

## Phase 3: 儀表板整合與專案完成 (已完成)
- [x] 執行 `Build-LogsDashboard.ps1` 將專案規格匯入「知識庫總覽」
- [x] 撰寫 Walkthrough 結案報告
- [x] 正式交付專案並上線
