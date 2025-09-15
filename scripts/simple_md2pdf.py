#!/usr/bin/env python3
"""
Simple MD2PDF - Minimal Markdown to PDF Converter

A simplified version for debugging LaTeX compilation issues.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
import re
import tempfile
import shutil

def simple_escape_latex(text):
    """Simple LaTeX character escaping"""
    replacements = {
        '\\': '\\textbackslash{}',
        '{': '\\{',
        '}': '\\}',
        '$': '\\$',
        '&': '\\&',
        '%': '\\%',
        '#': '\\#',
        '^': '\\textasciicircum{}',
        '_': '\\_',
        '~': '\\textasciitilde{}'
    }
    
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    
    return text

def simple_markdown_to_latex(markdown_content, title="Document"):
    """Simple markdown to LaTeX conversion"""
    
    template = f"""\\documentclass[11pt,letterpaper]{{article}}
\\usepackage[margin=1in]{{geometry}}
\\usepackage{{amsmath}}
\\usepackage{{amsfonts}}
\\usepackage{{graphicx}}
\\usepackage{{booktabs}}
\\usepackage{{xcolor}}
\\usepackage{{hyperref}}
\\usepackage{{listings}}

\\definecolor{{primary}}{{RGB}}{{33,150,243}}

\\title{{{title}}}
\\author{{MD2PDF}}
\\date{{\\today}}

\\begin{{document}}

\\maketitle

"""
    
    lines = markdown_content.split('\n')
    
    for line in lines:
        line = line.rstrip()
        
        if line.startswith('# '):
            title = simple_escape_latex(line[2:].strip())
            template += f"\\section{{{title}}}\n\n"
        elif line.startswith('## '):
            title = simple_escape_latex(line[3:].strip())
            template += f"\\subsection{{{title}}}\n\n"
        elif line.startswith('### '):
            title = simple_escape_latex(line[4:].strip())
            template += f"\\subsubsection{{{title}}}\n\n"
        elif line.startswith('- '):
            content = simple_escape_latex(line[2:].strip())
            content = re.sub(r'\\textasteriskmark\\textasteriskmark(.*?)\\textasteriskmark\\textasteriskmark', r'\\textbf{\1}', content)
            template += f"\\begin{{itemize}}\\item {content}\\end{{itemize}}\n\n"
        elif line.strip() == '':
            template += "\n"
        else:
            # Regular text
            content = simple_escape_latex(line)
            # Simple bold formatting
            content = re.sub(r'\\textasteriskmark\\textasteriskmark(.*?)\\textasteriskmark\\textasteriskmark', r'\\textbf{\1}', content)
            template += f"{content}\n\n"
    
    template += "\\end{document}\n"
    return template

def compile_simple_pdf(latex_content, output_path):
    """Simple PDF compilation with debugging"""
    
    # Convert to absolute path to avoid issues with directory changes
    output_path = Path(output_path).absolute()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save LaTeX file for debugging
    debug_tex = output_path.parent / f"{output_path.stem}_debug.tex"
    with open(debug_tex, 'w', encoding='utf-8') as f:
        f.write(latex_content)
    
    print(f"Debug: LaTeX file saved to {debug_tex}")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        
        # Write LaTeX file
        tex_file = temp_dir_path / 'document.tex'
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        # Change to temp directory
        original_dir = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            # Run pdflatex
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', 'document.tex'],
                capture_output=True, text=True
            )
            
            print(f"LaTeX return code: {result.returncode}")
            
            if result.stdout:
                print("LaTeX stdout:")
                print(result.stdout[-1000:])
            
            if result.stderr:
                print("LaTeX stderr:")
                print(result.stderr[-1000:])
            
            # Check for PDF
            pdf_file = temp_dir_path / 'document.pdf'
            print(f"Looking for PDF at: {pdf_file}")
            print(f"Temp dir contents: {list(temp_dir_path.iterdir())}")
            
            if pdf_file.exists():
                print(f"PDF found, size: {pdf_file.stat().st_size} bytes")
                print(f"Copying to: {output_path}")
                try:
                    shutil.copy2(pdf_file, output_path)
                    print(f"Copy completed")
                    # Verify copy worked
                    if output_path.exists():
                        print(f"Verification: Output file exists, size: {output_path.stat().st_size} bytes")
                        return True
                    else:
                        print(f"Verification failed: Output file doesn't exist at {output_path}")
                        return False
                except Exception as e:
                    print(f"Copy failed: {e}")
                    return False
            else:
                print("No PDF file was created")
                return False
                
        finally:
            os.chdir(original_dir)

def main():
    parser = argparse.ArgumentParser(description='Simple Markdown to PDF converter')
    parser.add_argument('-i', '--input', required=True, help='Input markdown file')
    parser.add_argument('output', help='Output PDF file')
    parser.add_argument('--title', help='Document title')
    
    args = parser.parse_args()
    
    # Read input
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: {args.input} not found")
        sys.exit(1)
    
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title
    title = args.title or "Document"
    for line in content.split('\n'):
        if line.startswith('# '):
            title = line[2:].strip()
            break
    
    print(f"Converting {args.input} to PDF...")
    
    # Convert
    latex_content = simple_markdown_to_latex(content, title)
    
    # Compile
    success = compile_simple_pdf(latex_content, args.output)
    
    if success:
        output_path = Path(args.output)
        if output_path.exists():
            size = output_path.stat().st_size / 1024
            print(f"✅ Success: {args.output} ({size:.1f} KB)")
        else:
            print(f"❌ PDF creation reported success but file not found at {output_path.absolute()}")
            sys.exit(1)
    else:
        print("❌ Failed to generate PDF")
        sys.exit(1)

if __name__ == "__main__":
    main()