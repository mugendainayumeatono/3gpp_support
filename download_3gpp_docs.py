import urllib.request
import re
import os
import argparse
import sys
import tempfile
import zipfile
import io
import json
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed

def extract_docx_to_json(docx_path, output_json_path):
    """
    Parses a .docx file and converts it to a structured JSON format by chapter.
    Uses basic numbering patterns to identify headings.
    """
    namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    try:
        with zipfile.ZipFile(docx_path) as z:
            xml_content = z.read('word/document.xml')
        
        tree = ET.XML(xml_content)
        chapters = []
        current_chapter = {"title": "Pre-amble", "content": []}
        
        # Regex to match chapter numbers like "1 ", "1.1 ", "5.2.2.1 "
        header_pattern = re.compile(r'^(\d+(\.\d+)*)\s+(.*)')
        
        for p in tree.findall('.//w:p', namespaces):
            # Extract text from paragraph
            texts = [node.text for node in p.findall('.//w:t', namespaces) if node.text]
            if not texts:
                continue
            
            p_text = ''.join(texts).strip()
            if not p_text:
                continue
                
            match = header_pattern.match(p_text)
            # Simple heuristic: if it matches the pattern and is relatively short, treat as header
            # Or if it has a Heading style (often w:pStyle val="HeadingX" or "1", "11" etc)
            is_header = False
            p_style = p.find('.//w:pPr/w:pStyle', namespaces)
            if p_style is not None:
                style_val = p_style.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
                # 3GPP often uses styles named '1', '2', '3' or 'Heading 1' etc.
                if style_val and (style_val.isdigit() or 'Heading' in style_val):
                    is_header = True
            
            if match and len(p_text) < 200: # Heuristic length check
                is_header = True

            if is_header:
                if current_chapter["content"]:
                    chapters.append(current_chapter)
                current_chapter = {"title": p_text, "content": []}
            else:
                current_chapter["content"].append(p_text)
        
        if current_chapter["content"] or current_chapter["title"] != "Pre-amble":
            chapters.append(current_chapter)
            
        # Post-process content to join lines
        for ch in chapters:
            ch["content"] = "\n".join(ch["content"])
            
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(chapters, f, indent=2, ensure_ascii=False)
            
        return True
    except Exception as e:
        print(f"[!] Error converting {docx_path} to JSON: {e}")
        return False

def get_spec_links(rel, series, specs=None):
    """Finds download links for the given release and series from the 3GPP FTP."""
    if not str(rel).startswith("Rel-"):
        rel = f"Rel-{rel}"
    
    # Ensure series is formatted correctly (e.g., 38 -> 38_series)
    series_str = str(series)
    series_folder = f"{series_str}_series" if "_series" not in series_str else series_str
    base_url = f"https://www.3gpp.org/ftp/Specs/latest/{rel}/{series_folder}/"
    
    print(f"[*] Fetching links from: {base_url}")
    try:
        req = urllib.request.Request(base_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=20) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"[!] Error accessing 3GPP FTP: {e}")
        return []

    # Find all zip links
    zips = re.findall(r'href="([^"]*\.zip)"', html)
    links = []
    for z in zips:
        filename = z.split("/")[-1]
        # If specific specs are requested, filter them
        if specs:
            match_found = False
            for s in specs:
                # Match 38.331 or 38331 style in filename (e.g., 38331-i90.zip)
                s_clean = s.replace(".", "")
                if s_clean in filename:
                    match_found = True
                    break
            if not match_found:
                continue
        
        full_url = z if z.startswith("http") else base_url + filename
        links.append(full_url)
    
    return list(set(links))

def download_and_unzip(url, target_dir, convert_to_json=False):
    filename = url.split("/")[-1]
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=60) as resp:
            zip_data = resp.read()
        
        # Unzip in memory and save to target_dir
        extracted_files = []
        with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
            z.extractall(target_dir)
            extracted_files = z.namelist()
            
        status_msg = f"Extracted: {', '.join(extracted_files)}"
        
        if convert_to_json:
            for f in extracted_files:
                if f.lower().endswith('.docx'):
                    docx_path = os.path.join(target_dir, f)
                    json_path = docx_path.rsplit('.', 1)[0] + '.json'
                    if extract_docx_to_json(docx_path, json_path):
                        status_msg += f" | Converted to JSON: {os.path.basename(json_path)}"
                        # Remove docx after successful conversion
                        try:
                            os.remove(docx_path)
                            status_msg += " (Docx removed)"
                        except Exception as e:
                            status_msg += f" (Cleanup failed: {e})"
            
        return filename, status_msg
    except Exception as e:
        return filename, str(e)

def main():
    parser = argparse.ArgumentParser(description="Download and unzip specific 3GPP specifications.")
    parser.add_argument("-r", "--rel", required=True, help="Release number (e.g., 17, 18)")
    parser.add_argument("-s", "--series", required=True, help="Series number (e.g., 23, 38)")
    parser.add_argument("--specs", nargs="+", help="Specific spec IDs to download (e.g., 38.331 38.211)")
    parser.add_argument("-t", "--threads", type=int, default=8, help="Number of download threads")
    parser.add_argument("-o", "--output", help="Output directory (defaults to system temp dir)")
    parser.add_argument("--json", action="store_true", help="Convert .docx files to JSON format")
    
    args = parser.parse_args()
    
    links = get_spec_links(args.rel, args.series, args.specs)
    
    if not links:
        print("[!] No matching specifications found.")
        if args.specs:
            print(f"[*] Searched for: {', '.join(args.specs)}")
        sys.exit(1)
        
    target_dir = args.output if args.output else os.path.join(tempfile.gettempdir(), f"3gpp_rel{args.rel}_s{args.series}_extracted")
    os.makedirs(target_dir, exist_ok=True)
    
    print(f"[*] Found {len(links)} matching files. Downloading and unzipping to: {target_dir}")
    
    results = []
    with ThreadPoolExecutor(max_workers=args.threads) as pool:
        futures = [pool.submit(download_and_unzip, url, target_dir, args.json) for url in links]
        for f in as_completed(futures):
            results.append(f.result())
            
    success_count = 0
    for name, status in results:
        if "Extracted:" in status:
            success_count += 1
            print(f"  [OK] {name} -> {status}")
        else:
            print(f"  [FAIL] {name}: {status}")

    print(f"\n[*] Task complete. {success_count}/{len(links)} files processed successfully.")
    print(f"[*] Files are located in: {target_dir}")

if __name__ == "__main__":
    main()
