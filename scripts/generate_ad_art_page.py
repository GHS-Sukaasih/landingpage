#!/usr/bin/env python3
"""
generate_ad_art_page.py
Membuat halaman ad-art.html berbasis berkas "AD ART GHS.md" dengan layout
portal warga Griya Hasanah Sukaasih (sidebar navigasi cepat, search filter, print view).
"""
import re
import os
import markdown

SOURCE_MD = "/mnt/c/Users/aseps/Downloads/AD ART GHS.md"
OUTPUT_HTML = "/home/aseps/MCP/workspace/landingpage/ad-art.html"

def clean_markdown(md_text: str) -> str:
    # Hapus escape backslash yang muncul dari export Google Docs / Word
    cleaned = re.sub(r'\\([-.()_~`*+])', r'\1', md_text)
    return cleaned

def parse_and_enhance_ad_art(raw_md: str):
    cleaned = clean_markdown(raw_md)
    lines = cleaned.splitlines()

    # Pre-process headings:
    # Convert bold lines like **BAB I**, **Pasal 1**, etc. into semantic markdown headings
    processed_lines = []
    
    in_mukadimah = False
    in_bagian_1 = False
    in_bagian_2 = False

    for line in lines:
        stripped = line.strip()
        
        # Deteksi Header Khusus
        if stripped == "**MUKADIMAH**":
            processed_lines.append("\n## MUKADIMAH\n")
            continue

        if "**BAGIAN – 1**" in stripped or "**BAGIAN - 1**" in stripped:
            processed_lines.append("\n# BAGIAN 1: ANGGARAN DASAR (AD)\n")
            in_bagian_1 = True
            in_bagian_2 = False
            continue

        if "**BAGIAN – 2**" in stripped or "**BAGIAN - 2**" in stripped:
            processed_lines.append("\n# BAGIAN 2: ANGGARAN RUMAH TANGGA (ART)\n")
            in_bagian_2 = True
            in_bagian_1 = False
            continue

        if "**LAMPIRAN**" in stripped:
            processed_lines.append("\n# LAMPIRAN AD/ART\n")
            continue

        # Deteksi BAB
        bab_match = re.match(r'^\*\*(BAB\s+[IVXLCDM]+)\*\*\s*$', stripped)
        if bab_match:
            bab_num = bab_match.group(1)
            processed_lines.append(f"\n## {bab_num}\n")
            continue

        # Deteksi Pasal
        pasal_match = re.match(r'^\*\*(Pasal\s+\d+)\*\*\s*$', stripped)
        if pasal_match:
            pasal_num = pasal_match.group(1)
            prefix = "ART - " if in_bagian_2 else "AD - "
            processed_lines.append(f"\n### {prefix}{pasal_num}\n")
            continue

        # Judul di bawah BAB atau Pasal (jika seluruh baris bold)
        if stripped.startswith("**") and stripped.endswith("**") and len(stripped) > 4:
            clean_title = stripped[2:-2].strip()
            # Hindari judul dokumen utama di paling atas
            if "PAGUYUBAN" not in clean_title and "TATA KELOLA" not in clean_title and "DESA SUKAASIH" not in clean_title and "KABUPATEN BEKASI" not in clean_title and "PROVINSI" not in clean_title and "ANGGARAN DASAR" not in clean_title:
                processed_lines.append(f"\n#### {clean_title}\n")
                continue

        processed_lines.append(line)

    enhanced_md = "\n".join(processed_lines)
    
    # Gunakan markdown dengan extensions
    html_body = markdown.markdown(
        enhanced_md,
        extensions=['tables', 'fenced_code', 'nl2br', 'sane_lists']
    )
    
    return html_body

def build_full_page(html_body: str) -> str:
    template = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AD/ART Paguyuban Perumahan Griya Hasanah Sukaasih</title>
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .adart-header {{
            background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%);
            color: #ffffff;
            padding: 7rem 1rem 3.5rem;
            text-align: center;
        }}
        .adart-header h1 {{
            font-size: 2.2rem;
            margin-bottom: 0.75rem;
            color: #ffffff;
        }}
        .adart-header p {{
            font-size: 1.1rem;
            color: #e8f5e9;
            max-width: 800px;
            margin: 0 auto 1.5rem;
        }}
        .adart-actions {{
            display: flex;
            justify-content: center;
            gap: 1rem;
            flex-wrap: wrap;
            margin-top: 1.5rem;
        }}
        .adart-btn {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.65rem 1.4rem;
            border-radius: 8px;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.2s ease;
            cursor: pointer;
            border: none;
            font-size: 0.95rem;
        }}
        .adart-btn-light {{
            background: #ffffff;
            color: #1b5e20;
        }}
        .adart-btn-light:hover {{
            background: #f1f8e9;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        .adart-btn-outline {{
            background: rgba(255,255,255,0.15);
            color: #ffffff;
            border: 1px solid rgba(255,255,255,0.4);
        }}
        .adart-btn-outline:hover {{
            background: rgba(255,255,255,0.25);
            transform: translateY(-2px);
        }}
        
        /* Container Layout */
        .adart-layout {{
            max-width: 1240px;
            margin: 2.5rem auto 4rem;
            padding: 0 1.5rem;
            display: grid;
            grid-template-columns: 290px 1fr;
            gap: 2.5rem;
            align-items: start;
        }}
        
        /* Sidebar Sticky */
        .adart-sidebar {{
            position: sticky;
            top: 90px;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 1.25rem;
            box-shadow: 0 2px 12px rgba(0,0,0,0.05);
            max-height: calc(100vh - 120px);
            overflow-y: auto;
        }}
        .sidebar-title {{
            font-size: 1.1rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .search-box {{
            width: 100%;
            padding: 0.6rem 0.85rem;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            font-size: 0.9rem;
            margin-bottom: 1rem;
            outline: none;
            transition: border-color 0.2s;
        }}
        .search-box:focus {{
            border-color: #2e7d32;
            box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.15);
        }}
        .toc-list {{
            list-style: none;
            padding: 0;
            margin: 0;
            font-size: 0.88rem;
        }}
        .toc-list li {{
            margin-bottom: 0.4rem;
        }}
        .toc-list a {{
            color: #475569;
            text-decoration: none;
            display: block;
            padding: 0.35rem 0.5rem;
            border-radius: 6px;
            transition: all 0.15s ease;
            line-height: 1.4;
        }}
        .toc-list a:hover {{
            background: #f1f8e9;
            color: #1b5e20;
            padding-left: 0.75rem;
        }}
        .toc-group-title {{
            font-weight: 700;
            color: #1b5e20;
            margin-top: 1rem;
            margin-bottom: 0.4rem;
            padding-bottom: 0.2rem;
            border-bottom: 1px solid #e2e8f0;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        /* Content Document */
        .adart-content {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 2.5rem 3rem;
            box-shadow: 0 2px 15px rgba(0,0,0,0.04);
            line-height: 1.75;
            color: #334155;
        }}
        .adart-content h1 {{
            font-size: 1.75rem;
            color: #1b5e20;
            border-bottom: 3px solid #2e7d32;
            padding-bottom: 0.6rem;
            margin-top: 2.5rem;
            margin-bottom: 1.5rem;
        }}
        .adart-content h1:first-of-type {{
            margin-top: 0;
        }}
        .adart-content h2 {{
            font-size: 1.35rem;
            color: #2e7d32;
            margin-top: 2rem;
            margin-bottom: 1rem;
            padding-left: 0.6rem;
            border-left: 4px solid #4caf50;
        }}
        .adart-content h3 {{
            font-size: 1.15rem;
            color: #1e293b;
            margin-top: 1.6rem;
            margin-bottom: 0.5rem;
            font-weight: 700;
        }}
        .adart-content h4 {{
            font-size: 1rem;
            color: #475569;
            margin-top: 0.25rem;
            margin-bottom: 0.75rem;
            font-style: italic;
        }}
        .adart-content p {{
            margin-bottom: 1rem;
            text-align: justify;
        }}
        .adart-content ol, .adart-content ul {{
            margin-bottom: 1.25rem;
            padding-left: 1.5rem;
        }}
        .adart-content li {{
            margin-bottom: 0.5rem;
        }}
        .adart-content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            font-size: 0.95rem;
        }}
        .adart-content th, .adart-content td {{
            border: 1px solid #cbd5e1;
            padding: 0.75rem 1rem;
            text-align: left;
        }}
        .adart-content th {{
            background: #f1f8e9;
            color: #1b5e20;
            font-weight: 600;
        }}
        .highlight {{
            background-color: #ffeb3b;
            padding: 0.1rem 0.2rem;
            border-radius: 3px;
        }}

        /* Responsive */
        @media (max-width: 992px) {{
            .adart-layout {{
                grid-template-columns: 1fr;
            }}
            .adart-sidebar {{
                position: static;
                max-height: none;
            }}
            .adart-content {{
                padding: 1.5rem 1.25rem;
            }}
        }}

        @media print {{
            .header, .footer, .adart-sidebar, .adart-actions, .fab {{
                display: none !important;
            }}
            .adart-header {{
                background: none !important;
                color: #000 !important;
                padding: 1rem 0 !important;
            }}
            .adart-header h1 {{
                color: #000 !important;
            }}
            .adart-layout {{
                display: block !important;
                margin: 0 !important;
                padding: 0 !important;
            }}
            .adart-content {{
                border: none !important;
                box-shadow: none !important;
                padding: 0 !important;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <nav class="nav">
            <div class="logo-container">
                <div class="logo-circle">GHS</div>
                <div class="logo-text">
                    <div class="logo-main">Griya Hasanah</div>
                    <div class="logo-sub">Sukaasih</div>
                </div>
            </div>
            <div class="nav-menu">
                <a href="index.html#home">Beranda</a>
                <a href="index.html#vision-mission">Visi & Misi</a>
                <a href="index.html#announcements">Pengumuman</a>
                <a href="index.html#management">Pengurus</a>
                <a href="index.html#facilities">Fasilitas</a>
                <a href="index.html#payment">Iuran</a>
                <a href="index.html#financial-info">Keuangan</a>
                <a href="ad-art.html" style="color: #2d7d32; font-weight: 700;">AD/ART</a>
                <a href="index.html#gallery">Galeri</a>
                <a href="index.html#contact">Kontak</a>
            </div>
            <a href="index.html#contact" class="cta-btn">Hubungi Pengurus</a>
        </nav>
    </header>

    <div class="adart-header">
        <h1>Anggaran Dasar & Anggaran Rumah Tangga (AD/ART)</h1>
        <p>Paguyuban Perumahan Griya Hasanah Sukaasih — Desa Sukaasih, Kecamatan Sukatani, Kabupaten Bekasi, Provinsi Jawa Barat</p>
        <div class="adart-actions">
            <a href="index.html" class="adart-btn adart-btn-outline"><i class="fas fa-arrow-left"></i> Kembali ke Beranda</a>
            <button onclick="window.print()" class="adart-btn adart-btn-light"><i class="fas fa-print"></i> Cetak / Simpan PDF</button>
            <a href="#bagian-1" class="adart-btn adart-btn-outline"><i class="fas fa-book-open"></i> Mulai Baca</a>
        </div>
    </div>

    <div class="adart-layout">
        <aside class="adart-sidebar">
            <div class="sidebar-title">
                <span><i class="fas fa-list-ul"></i> Daftar Isi</span>
            </div>
            <input type="text" id="clause-search" class="search-box" placeholder="Cari pasal, aturan, iuran...">
            <div id="toc-container">
                <!-- TOC links will be dynamically populated/linked -->
                <div class="toc-group-title">Pendahuluan</div>
                <ul class="toc-list">
                    <li><a href="#mukadimah">Mukadimah</a></li>
                </ul>

                <div class="toc-group-title">Bagian 1: Anggaran Dasar</div>
                <ul class="toc-list">
                    <li><a href="#bab-i">BAB I: Nama, Waktu & Kedudukan</a></li>
                    <li><a href="#bab-ii">BAB II: Visi, Misi, Asas & Usaha</a></li>
                    <li><a href="#bab-organisasi">BAB Organisasi Kepengurusan</a></li>
                    <li><a href="#bab-iii">BAB III: Pemilihan Ketua</a></li>
                    <li><a href="#bab-iv">BAB IV: Keuangan Paguyuban</a></li>
                    <li><a href="#bab-v">BAB V: Kerja Bakti / Gotong Royong</a></li>
                    <li><a href="#bab-vi">BAB VI: Keamanan & Siskamling</a></li>
                    <li><a href="#bab-vii">BAB VII: Pelaksanaan Hari Besar</a></li>
                    <li><a href="#bab-viii">BAB VIII: Permasalahan & Sanksi</a></li>
                    <li><a href="#bab-ix">BAB IX: Perubahan Anggaran Dasar</a></li>
                    <li><a href="#bab-x">BAB X: Penutup</a></li>
                </ul>

                <div class="toc-group-title">Bagian 2: Anggaran Rumah Tangga</div>
                <ul class="toc-list">
                    <li><a href="#art-pasal-1">Pasal 1: Pengertian</a></li>
                    <li><a href="#art-pasal-2">Pasal 2: Struktur Organisasi</a></li>
                    <li><a href="#art-pasal-3">Pasal 3: Tugas & Tanggung Jawab</a></li>
                    <li><a href="#art-pasal-4">Pasal 4: Hak & Kewajiban Warga</a></li>
                    <li><a href="#art-pasal-5">Pasal 5: Pengelolaan Kas RT</a></li>
                    <li><a href="#art-pasal-6">Pasal 6: Kriteria Bantuan Warga</a></li>
                    <li><a href="#art-pasal-7">Pasal 7: Renovasi Rumah</a></li>
                    <li><a href="#art-pasal-8">Pasal 8: Tata Tertib Berkendara</a></li>
                    <li><a href="#art-pasal-9">Pasal 9: Perubahan ART</a></li>
                </ul>

                <div class="toc-group-title">Lampiran Dokumen</div>
                <ul class="toc-list">
                    <li><a href="#lampiran-ipl">1. Kebijakan IPL</a></li>
                    <li><a href="#lampiran-psu">2. Formulir Inventarisasi PSU</a></li>
                </ul>
            </div>
        </aside>

        <main class="adart-content" id="document-content">
            {html_body}
        </main>
    </div>

    <footer class="footer">
        <div class="footer-content">
            <div class="logo-container" style="justify-content: center; margin-bottom: 1rem;">
                <div class="logo-circle">GHS</div>
                <div class="logo-text">
                    <div class="logo-main">Griya Hasanah</div>
                    <div class="logo-sub">Sukaasih</div>
                </div>
            </div>
            <div class="footer-links">
                <a href="index.html#home">Beranda</a>
                <a href="index.html#vision-mission">Visi & Misi</a>
                <a href="index.html#announcements">Pengumuman</a>
                <a href="index.html#management">Pengurus</a>
                <a href="index.html#facilities">Fasilitas</a>
                <a href="index.html#payment">Iuran</a>
                <a href="index.html#financial-info">Keuangan</a>
                <a href="ad-art.html">AD/ART</a>
                <a href="index.html#gallery">Galeri</a>
                <a href="index.html#contact">Kontak</a>
            </div>
            <p style="color: #94a3b8; font-size: 0.9rem;">&copy; 2026 Paguyuban Griya Hasanah Sukaasih. All Rights Reserved.</p>
        </div>
    </footer>

    <script>
        // Fitur Pencarian Real-Time dalam Naskah AD/ART
        document.getElementById('clause-search').addEventListener('input', function(e) {{
            const query = e.target.value.toLowerCase().trim();
            const content = document.getElementById('document-content');
            
            // Hapus highlight sebelumnya
            const highlighted = content.querySelectorAll('.highlight');
            highlighted.forEach(el => {{
                el.outerHTML = el.innerText;
            }});

            if (!query || query.length < 3) return;

            // Highlight matches
            const walker = document.createTreeWalker(content, NodeFilter.SHOW_TEXT, null, false);
            const nodesToReplace = [];
            while (walker.nextNode()) {{
                const node = walker.currentNode;
                if (node.nodeValue.toLowerCase().includes(query) && node.parentElement.tagName !== 'SCRIPT') {{
                    nodesToReplace.push(node);
                }}
            }}

            nodesToReplace.forEach(node => {{
                const regex = new RegExp(`(${{query.replace(/[-\\/\\\\^$*+?.()|[\\]{{}}]/g, '\\\\$&')}})`, 'gi');
                const span = document.createElement('span');
                span.innerHTML = node.nodeValue.replace(regex, '<span class="highlight">$1</span>');
                node.parentNode.replaceChild(span, node);
            }});
        }});
    </script>
</body>
</html>
"""
    return template

def main():
    if not os.path.exists(SOURCE_MD):
        print(f"Error: Sumber {SOURCE_MD} tidak ditemukan.")
        return

    with open(SOURCE_MD, "r", encoding="utf-8") as f:
        raw_md = f.read()

    html_body = parse_and_enhance_ad_art(raw_md)
    
    # Berikan ID anchor ke elemen-elemen penting
    # Mukadimah
    html_body = html_body.replace('<h2>MUKADIMAH</h2>', '<h2 id="mukadimah">MUKADIMAH</h2>')
    
    # Bagian 1 & 2
    html_body = html_body.replace('<h1>BAGIAN 1: ANGGARAN DASAR (AD)</h1>', '<h1 id="bagian-1">BAGIAN 1: ANGGARAN DASAR (AD)</h1>')
    html_body = html_body.replace('<h1>BAGIAN 2: ANGGARAN RUMAH TANGGA (ART)</h1>', '<h1 id="bagian-2">BAGIAN 2: ANGGARAN RUMAH TANGGA (ART)</h1>')
    html_body = html_body.replace('<h1>LAMPIRAN AD/ART</h1>', '<h1 id="lampiran">LAMPIRAN AD/ART</h1>')
    
    # BAB anchors
    html_body = html_body.replace('<h2>BAB I</h2>', '<h2 id="bab-i">BAB I</h2>')
    html_body = html_body.replace('<h2>BAB II</h2>', '<h2 id="bab-ii">BAB II</h2>', 1)
    # BAB organisasi
    html_body = html_body.replace('<h2>BAB II</h2>', '<h2 id="bab-organisasi">BAB II: ORGANISASI KEPENGURUSAN</h2>', 1)
    html_body = html_body.replace('<h2>BAB III</h2>', '<h2 id="bab-iii">BAB III</h2>')
    html_body = html_body.replace('<h2>BAB IV</h2>', '<h2 id="bab-iv">BAB IV</h2>')
    html_body = html_body.replace('<h2>BAB V</h2>', '<h2 id="bab-v">BAB V</h2>')
    html_body = html_body.replace('<h2>BAB VI</h2>', '<h2 id="bab-vi">BAB VI</h2>')
    html_body = html_body.replace('<h2>BAB VII</h2>', '<h2 id="bab-vii">BAB VII</h2>')
    html_body = html_body.replace('<h2>BAB VIII</h2>', '<h2 id="bab-viii">BAB VIII</h2>')
    html_body = html_body.replace('<h2>BAB IX</h2>', '<h2 id="bab-ix">BAB IX</h2>')
    html_body = html_body.replace('<h2>BAB X</h2>', '<h2 id="bab-x">BAB X</h2>')
    
    # ART Pasal anchors
    for i in range(1, 10):
        target = f'<h3>ART - Pasal {i}</h3>'
        replacement = f'<h3 id="art-pasal-{i}">ART - Pasal {i}</h3>'
        html_body = html_body.replace(target, replacement)

    # Lampiran anchors
    html_body = html_body.replace('1. Kebijakan Iuran Pengelolaan Lingkungan (IPL)', '<span id="lampiran-ipl">1. Kebijakan Iuran Pengelolaan Lingkungan (IPL)</span>')
    html_body = html_body.replace('2. Formulir Inventarisasi PSU', '<span id="lampiran-psu">2. Formulir Inventarisasi PSU</span>')

    full_html = build_full_page(html_body)

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"Berhasil menghasilkan halaman {OUTPUT_HTML} (Ukuran: {len(full_html)} bytes)")

if __name__ == "__main__":
    main()

