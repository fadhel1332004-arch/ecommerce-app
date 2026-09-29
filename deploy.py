"""
Auto-Deploy Script for Al-Aaqil Market
سير التحديث التلقائي الشامل لمتجر العاقل ماركت على PythonAnywhere

طريقة الاستخدام:
    python deploy.py "رسالة التعديل"
أو ببساطة:
    python deploy.py
"""
import sys
import os
import subprocess
import urllib.request
import json

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

DEPLOY_URL = "https://fadhelalzilh.pythonanywhere.com/api/auto-deploy?token=fadhel_market_auto_deploy_2026"

def run_cmd(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if result.stdout and result.stdout.strip():
        print("  " + result.stdout.strip())
    if result.stderr and result.stderr.strip():
        print("  " + result.stderr.strip())
    if result.returncode != 0:
        return False
    return True

def main():
    commit_msg = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].strip() else "Auto deploy update"

    print("=" * 60)
    print(">> بدء النشر والتحديث التلقائي الشامل (Local -> GitHub -> PythonAnywhere)")
    print("=" * 60)

    # 1. Add modified files
    print("\n[1/4] تجهيز الملفات المعدلة (git add .)...")
    if not run_cmd(["git", "add", "."]):
        print("[-] فشل في تجهيز الملفات.")
        return

    # 2. Check if commit is needed
    print("\n[2/4] حفظ التعديل (git commit)...")
    status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if status.stdout.strip():
        run_cmd(["git", "commit", "-m", commit_msg])
    else:
        print("  لا توجد تغييرات جديدة للحفظ (Commit). سيتم محاولة تحديث السيرفر مباشرة.")

    # 3. Push to GitHub
    print("\n[3/4] رفع التعديلات إلى GitHub (git push origin main)...")
    if not run_cmd(["git", "push", "origin", "main"]):
        print("[-] فشل الرفع إلى GitHub. تأكد من اتصال الإنترنت.")
        return

    # 4. Trigger auto-deploy on PythonAnywhere
    print("\n[4/4] إرسال أمر التحديث التلقائي إلى سيرفر PythonAnywhere...")
    try:
        req = urllib.request.Request(
            DEPLOY_URL,
            headers={'User-Agent': 'DeployScript/1.0'}
        )
        with urllib.request.urlopen(req, timeout=40) as response:
            res_body = response.read().decode('utf-8')
            res_data = json.loads(res_body)
            if res_data.get('status') == 'success':
                print("\n[+] تم التحديث وإعادة تشغيل السيرفر بنجاح تام!")
                print("تفاصيل العملية في السيرفر:")
                for line in res_data.get('log', []):
                    if line.strip():
                        print(f"  * {line}")
            else:
                print("\n[!] استجابة السيرفر:", res_data)
    except urllib.error.HTTPError as e:
        print(f"\n[!] استجاب السيرفر برمز ({e.code}): {e.reason}")
        print("ملاحظة مهمة: في المرة الأولى فقط، قم بسحب التحديث يدوياً على السيرفر لتثبيت مسار التحديث التلقائي.")
    except Exception as e:
        print(f"\n[-] تعذر الوصول لطلب التحديث: {e}")

    print("\n" + "=" * 60)
    print("رابط موقعك المباشر: https://fadhelalzilh.pythonanywhere.com")
    print("=" * 60)

if __name__ == '__main__':
    main()
