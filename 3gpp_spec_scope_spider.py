import json
import urllib.request
import re
import os
import zipfile
import io
import xml.etree.ElementTree as ET
import argparse
import sys
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# Global Config
print_lock = Lock()
MAX_THREAD_SAFE = 32 

def log_status(spec, stage, current, total, status="info"):
    """Thread-safe progress and status logger."""
    if total <= 0: return 
    with print_lock:
        c_safe = max(0, min(current, total))
        percent = (c_safe / total) * 100
        bar = '█' * int(20 * c_safe // total) + '-' * (20 - int(20 * c_safe // total))
        progress_line = f"\rProgress: |{bar}| {percent:.1f}% ({current}/{total})"
        try:
            sys.stdout.write('\x1b[2K') 
        except:
            sys.stdout.write('\r')
        print(f"\r[{spec[:12]:<12}] {stage:<12} | {status}")
        sys.stdout.write(progress_line)
        sys.stdout.flush()

def get_release_data(target_rel=None):
    """Find the latest or specific Rel folder that contains 38-series zip files."""
    base_url = "https://www.3gpp.org/ftp/Specs/latest/"
    
    # If target_rel is specified, try only that one
    if target_rel:
        if not str(target_rel).startswith("Rel-"):
            target_rel = f"Rel-{target_rel}"
        rel_path = f"{base_url}{target_rel}/38_series/"
        print(f"[*] Checking Specified Release: {target_rel}...")
        try:
            req_rel = urllib.request.Request(rel_path, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_rel, timeout=15) as resp:
                rel_html = resp.read().decode('utf-8', errors='ignore')
            zips = re.findall(r'href="([^"]*\.zip)"', rel_html)
            if len(zips) > 0:
                print(f"[*] Target Release Locked: {target_rel} ({len(zips)} files found)")
                links = [l if l.startswith("http") else rel_path + l.split("/")[-1] for l in zips]
                return target_rel, list(set(links))
            else:
                print(f"[!] Warning: No zip files found in {target_rel}/38_series/")
                return None, []
        except Exception as e:
            print(f"[!] Error accessing {target_rel}: {e}")
            return None, []

    # Fallback to automatic detection of latest populated release
    print(f"[*] Connecting to 3GPP FTP Index...")
    try:
        req = urllib.request.Request(base_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=20) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"[!] Network Error: {e}")
        return None, []
    
    rels = re.findall(r'href="[^"]*(Rel-(\d+))/?"', html)
    sorted_rels = sorted(rels, key=lambda x: int(x[1]), reverse=True)
    
    for rel_name, _ in sorted_rels:
        rel_path = f"{base_url}{rel_name}/38_series/"
        try:
            req_rel = urllib.request.Request(rel_path, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_rel, timeout=15) as resp:
                rel_html = resp.read().decode('utf-8', errors='ignore')
            zips = re.findall(r'href="([^"]*\.zip)"', rel_html)
            if len(zips) > 0:
                print(f"[*] Target Release Locked: {rel_name} ({len(zips)} files found)")
                links = [l if l.startswith("http") else rel_path + l.split("/")[-1] for l in zips]
                return rel_name, list(set(links))
        except: continue
    return None, []

def process_spec_zip(zip_url, total, tracker):
    """Downloads and parses a single spec to extract Clause 1 (Scope)."""
    match = re.search(r'(38\.\d+|38\d{3})', zip_url)
    spec_id = match.group(1) if match else "Spec"
    
    try:
        # 1. Download
        log_status(spec_id, "Downloading", tracker['completed'], total)
        req = urllib.request.Request(zip_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=60) as resp:
            zip_data = resp.read()
        
        # 2. Extract in-memory (Critical Fix: Using BytesIO for nested ZIP)
        log_status(spec_id, "Extracting", tracker['completed'], total)
        with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
            docx_name = next((n for n in z.namelist() if n.endswith(".docx")), None)
            if not docx_name: raise ValueError("No DOCX found")
            
            # 先读取出 DOCX 的原始字节，再交给 ZipFile 解析
            docx_bytes = z.read(docx_name)
            with zipfile.ZipFile(io.BytesIO(docx_bytes)) as dxz:
                xml_content = dxz.read("word/document.xml")
        
        # 3. Parse XML using robust text iteration
        log_status(spec_id, "Parsing XML", tracker['completed'], total)
        root = ET.fromstring(xml_content)
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        
        # 改进：利用 itertext() 提取段落内所有层级的文本，更健壮
        paras = []
        for p in root.findall(".//w:p", ns):
            text = "".join(p.itertext()).strip()
            if text: paras.append(text)
        
        scope_lines, in_scope = [], False
        for p in paras:
            p_clean = p.lower().strip()
            # Regex 增强：支持 "1 Scope", "1. Scope" 且支持结尾有空格
            if re.match(r'^1\.?\s*scope(\s|$)', p_clean):
                in_scope, scope_lines = True, []
            elif re.match(r'^2\.?\s*references(\s|$)', p_clean):
                in_scope = False
            elif in_scope and p and "PAGEREF" not in p:
                scope_lines.append(p)
        
        final_scope = "\n".join(scope_lines).strip()
        with tracker['lock']: tracker['completed'] += 1
        log_status(spec_id, "Success", tracker['completed'], total, "OK")
        
        return {"spec": spec_id, "scope": final_scope if final_scope else "Scope section not found.", "status": "success"}

    except Exception as e:
        with tracker['lock']: tracker['completed'] += 1
        log_status(spec_id, "Failed", tracker['completed'], total, f"Error: {str(e)[:15]}")
        return {"spec": spec_id, "error": str(e), "status": "error"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--threads", type=int, default=1)
    parser.add_argument("-r", "--release", type=str, help="Target Release (e.g., 19 or Rel-19)")
    parser.add_argument("-o", "--output", type=str, help="Output directory or file path for the JSON report")
    args = parser.parse_args()

    num_threads = max(1, min(args.threads, MAX_THREAD_SAFE))
    rel_id, spec_urls = get_release_data(args.release)
    if not rel_id:
        print("[!] Error: No specifications found.")
        sys.exit(1)
        
    out_path = "resources/summary/38_series_full_report.json"
    if args.output:
        if args.output.endswith(".json"):
            out_path = args.output
        else:
            out_path = os.path.join(args.output, "38_series_full_report.json")
            
    # Load existing results to skip already processed specs
    all_results = []
    processed_specs = set()
    if os.path.exists(out_path):
        try:
            with open(out_path, "r", encoding="utf-8") as f:
                all_results = json.load(f)
                processed_specs = {item['spec'] for item in all_results if item.get('status') == 'success'}
                print(f"[*] Found existing report with {len(processed_specs)} entries. Skipping them.")
        except Exception as e:
            print(f"[!] Warning: Could not read existing report: {e}")

    # Filter spec_urls
    filtered_urls = []
    for url in spec_urls:
        match = re.search(r'(38\.\d+|38\d{3})', url)
        spec_id = match.group(1) if match else None
        if spec_id and spec_id in processed_specs:
            continue
        filtered_urls.append(url)

    if not filtered_urls:
        print("[*] All specifications are already processed in the existing report.")
        sys.exit(0)

    print(f"[*] Task: Extracting {len(filtered_urls)} abstracts from {rel_id} (Threads: {num_threads})")
    task_tracker = {'completed': 0, 'lock': Lock()}
    
    try:
        with ThreadPoolExecutor(max_workers=num_threads) as pool:
            futures = [pool.submit(process_spec_zip, url, len(filtered_urls), task_tracker) for url in filtered_urls]
            for f in as_completed(futures):
                all_results.append(f.result())
    except KeyboardInterrupt:
        print("\n[!] User aborted.")
            
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=4, ensure_ascii=False)
    print(f"\n\n[*] Completed. Report: {out_path}")

    out_path = "resources/summary/38_series_full_report.json"
    if args.output:
        if args.output.endswith(".json"):
            out_path = args.output
        else:
            out_path = os.path.join(args.output, "38_series_full_report.json")
            
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=4, ensure_ascii=False)
    print(f"\n\n[*] Completed. Report: {out_path}")
