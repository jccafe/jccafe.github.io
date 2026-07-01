import subprocess
import sys
import os

# 解決 Windows 控制台 CP950 編碼問題
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run_cmd(args, capture_output=True):
    try:
        res = subprocess.run(args, capture_output=capture_output, text=True, check=False)
        return res
    except Exception as e:
        print(f"\033[91m執行指令時發生例外: {' '.join(args)} - {e}\033[0m")
        sys.exit(1)

def get_current_branch():
    res = run_cmd(['git', 'branch', '--show-current'])
    branch = res.stdout.strip() if res.returncode == 0 else 'main'
    return branch if branch else 'main'

def main():
    # 支援 Windows 終端機 ANSI 顏色輸出
    if os.name == 'nt':
        os.system('color')

    print("==========================================")
    print("[Deploy] 開始執行自動化部署與網站目錄更新流程...")
    print("==========================================")

    # 0. 預檢：是否為 Git 儲存庫
    git_check = run_cmd(['git', 'rev-parse', '--is-inside-work-tree'])
    if git_check.returncode != 0:
        print("\033[91m[Error] 當前目錄並非 Git 儲存庫！\033[0m")
        print("請確保此目錄已初始化 Git (執行 git init) 且配置了遠端儲存庫 (git remote add origin ...)。")
        sys.exit(1)

    # 1. 取得當前分支
    branch = get_current_branch()
    print(f"[Info] 當前分支: {branch}")

    # 2. 執行 git pull origin <branch>
    print(f"\n[Deploy] 步驟 1: 同步遠端儲存庫 (git pull origin {branch})...")
    pull_res = run_cmd(['git', 'pull', 'origin', branch])
    
    if pull_res.returncode != 0:
        print("\033[91m[Error] 同步遠端儲存庫失敗！\033[0m")
        print("標準輸出:\n", pull_res.stdout)
        print("錯誤輸出:\n", pull_res.stderr)
        
        output_lower = (pull_res.stdout + pull_res.stderr).lower()
        if "conflict" in output_lower or "merge" in output_lower:
            print("\033[91;1m[Warning] 偵測到 Git 合併衝突，請手動解決衝突後再繼續執行部署。\033[0m")
        else:
            print("\033[91m[Error] 執行 git pull 出錯，請確認網路連線或儲存庫設定。\033[0m")
        sys.exit(1)
        
    print("[OK] 遠端同步成功。")

    # 3. 執行 generate_index.py 重新生成目錄
    print("\n[Deploy] 步驟 2: 重新生成網頁目錄 (generate_index.py)...")
    # 由於我們已在虛擬環境中，直接用當前執行器 python 執行 generate_index.py
    gen_res = run_cmd([sys.executable, 'generate_index.py'], capture_output=False)
    
    if gen_res.returncode != 0:
        print("\033[91m[Error] 網頁目錄生成失敗！\033[0m")
        sys.exit(1)
        
    print("[OK] 網頁目錄生成成功。")

    # 4. 檢查是否有變更
    print("\n[Deploy] 步驟 3: 檢查網頁變更狀態...")
    status_res = run_cmd(['git', 'status', '--porcelain'])
    
    if status_res.returncode != 0:
        print("\033[91m[Error] 無法取得 Git 狀態！\033[0m")
        sys.exit(1)
        
    changes = status_res.stdout.strip()
    if not changes:
        print("[OK] 沒有偵測到任何目錄更新變更，略過 Git 提交與推送。")
        print("\n[Success] 部署流程順利結束，本地與遠端均為最新狀態！")
        sys.exit(0)
        
    print("[List] 偵測到變更項目:")
    print(changes)

    # 5. 暫存變更 (git add .)
    print("\n[Deploy] 步驟 4: 暫存與提交變更 (git add . & commit)...")
    add_res = run_cmd(['git', 'add', '.'])
    if add_res.returncode != 0:
        print("\033[91m[Error] git add 失敗！\033[0m")
        sys.exit(1)
    print("[OK] 檔案已暫存。")

    # 6. 提交變更 (git commit)
    commit_res = run_cmd(['git', 'commit', '-m', 'Auto-update index'])
    if commit_res.returncode != 0:
        if "nothing to commit" in commit_res.stdout or "nothing to commit" in commit_res.stderr:
            print("[OK] 無檔案需要提交。")
        else:
            print("\033[91m[Error] git commit 失敗！\033[0m")
            print(commit_res.stdout)
            print(commit_res.stderr)
            sys.exit(1)
    else:
        print("[OK] 成功提交變更。")

    # 7. 推送變更 (git push origin <branch>)
    print(f"\n[Deploy] 步驟 5: 推送至遠端儲存庫 (git push origin {branch})...")
    push_res = run_cmd(['git', 'push', 'origin', branch])
    
    if push_res.returncode != 0:
        print("\033[91m[Error] 推送至 GitHub 失敗！\033[0m")
        print("標準輸出:\n", push_res.stdout)
        print("錯誤輸出:\n", push_res.stderr)
        sys.exit(1)
        
    print("\n==========================================")
    print("[Success] 部署成功！網站目錄已更新並推送到遠端儲存庫。")
    print("==========================================")

if __name__ == "__main__":
    main()
