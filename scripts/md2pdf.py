#!/usr/bin/env python3
"""
MD2PDF - Universal Markdown to PDF Converter

A robust command-line tool for converting markdown files to professional PDFs
using LaTeX with advanced formatting and typography.

Usage:
    python md2pdf.py -i input.md output.pdf
    python md2pdf.py --input report.md --output report.pdf
    python md2pdf.py -i README.md README.pdf --style academic
    python md2pdf.py -i notes.md notes.pdf --no-toc
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
import re
import tempfile
import shutil

def escape_latex(text):
    """Escape special LaTeX characters"""
    # Define character replacements
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

def process_markdown_formatting(text):
    """Convert markdown formatting to LaTeX"""
    # First escape LaTeX special characters
    text = escape_latex(text)
    
    # Then apply markdown formatting
    # Handle code blocks first (to protect from other formatting)
    text = re.sub(r'`([^`]+)`', r'\\texttt{\1}', text)  # inline code
    
    # Handle bold and italic (multiple patterns)
    text = re.sub(r'\*{4,}([^*]+?)\*{4,}', r'\\textbf{\1}', text)  # ****bold****
    text = re.sub(r'\*{2}([^*]+?)\*{2}', r'\\textbf{\1}', text)    # **bold**
    text = re.sub(r'(?<!\*)\*([^*\n]+?)\*(?!\*)', r'\\textit{\1}', text)  # *italic*
    
    # Handle links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\\href{\2}{\1}', text)  # [text](url)
    
    return text

def get_latex_template(style="modern", include_toc=True, title=None, author=None):
    """Generate LaTeX document template based on style"""
    
    if style == "academic":
        color_primary = "RGB{0,47,108}"
        color_secondary = "RGB{204,82,0}"
        color_accent = "RGB{0,102,51}"
    elif style == "minimal":
        color_primary = "RGB{64,64,64}"
        color_secondary = "RGB{128,128,128}"
        color_accent = "RGB{0,0,0}"
    else:  # modern (default)
        color_primary = "RGB{33,150,243}"
        color_secondary = "RGB{255,87,34}"
        color_accent = "RGB{76,175,80}"
    
    template = f"""\\documentclass[11pt,letterpaper]{{article}}
\\usepackage[margin=1in]{{geometry}}
\\usepackage{{amsmath}}
\\usepackage{{amsfonts}}
\\usepackage{{amssymb}}
\\usepackage{{graphicx}}
\\usepackage{{booktabs}}
\\usepackage{{array}}
\\usepackage{{longtable}}
\\usepackage{{xcolor}}
\\usepackage{{fancyhdr}}
\\usepackage{{hyperref}}
\\usepackage{{enumitem}}
\\usepackage{{titlesec}}
\\usepackage{{tocloft}}
\\usepackage{{microtype}}
\\usepackage{{float}}
\\usepackage{{caption}}
\\usepackage{{listings}}
\\usepackage{{setspace}}

% Color scheme
\\definecolor{{primary}}{{{color_primary}}}
\\definecolor{{secondary}}{{{color_secondary}}}
\\definecolor{{accent}}{{{color_accent}}}
\\definecolor{{lightgray}}{{RGB}}{{245,245,245}}
\\definecolor{{darkgray}}{{RGB}}{{80,80,80}}

% Page setup
\\setlength{{\\headheight}}{{14pt}}
\\pagestyle{{fancy}}
\\fancyhf{{}}
\\fancyhead[L]{{\\small\\leftmark}}
\\fancyhead[R]{{\\small Generated from Markdown}}
\\fancyfoot[C]{{\\thepage}}
\\renewcommand{{\\headrulewidth}}{{0.4pt}}
\\renewcommand{{\\footrulewidth}}{{0.4pt}}

% Section formatting
\\titleformat{{\\section}}
{{\\Large\\bfseries\\color{{primary}}}}
{{\\thesection}}{{1em}}{{}}
[\\titlerule]

\\titleformat{{\\subsection}}
{{\\large\\bfseries\\color{{secondary}}}}
{{\\thesubsection}}{{1em}}{{}}

\\titleformat{{\\subsubsection}}
{{\\normalsize\\bfseries\\color{{accent}}}}
{{\\thesubsubsection}}{{1em}}{{}}

% Table formatting
\\renewcommand{{\\arraystretch}}{{1.2}}

% Code formatting
\\lstset{{
    basicstyle=\\ttfamily\\small,
    backgroundcolor=\\color{{lightgray}},
    frame=single,
    rulecolor=\\color{{darkgray}},
    breaklines=true,
    breakatwhitespace=true,
    showstringspaces=false
}}

% Hyperref setup
\\hypersetup{{
    colorlinks=true,
    linkcolor=primary,
    filecolor=secondary,      
    urlcolor=accent,
    citecolor=primary,
    pdfauthor={{{author or "MD2PDF"}}},
    pdftitle={{{title or "Converted from Markdown"}}},
    pdfsubject={{Document converted from Markdown}}
}}

"""

    if title:
        template += f"""
\\title{{\\Huge\\textbf{{\\color{{primary}}{title}}}}}
"""
        if author:
            template += f"\\author{{\\large{author}}}\n"
        template += "\\date{\\today}\n"

    template += """
\\begin{document}

"""

    if title:
        template += """\\maketitle
\\thispagestyle{empty}
\\newpage

"""

    if include_toc:
        template += """\\tableofcontents
\\newpage

"""

    return template

def convert_table(table_lines):
    """Convert markdown table to LaTeX"""
    if len(table_lines) < 2:
        return ""
    
    # Remove empty lines and separators
    clean_lines = [line for line in table_lines if line.strip() and '---' not in line]
    
    if len(clean_lines) < 2:
        return ""
    
    # Parse header
    header_cells = [cell.strip() for cell in clean_lines[0].split('|') if cell.strip()]
    if not header_cells:
        return ""
    
    num_cols = len(header_cells)
    
    # Parse data rows
    data_rows = []
    for line in clean_lines[1:]:
        row_cells = [cell.strip() for cell in line.split('|') if cell.strip()]
        if len(row_cells) == num_cols:
            data_rows.append(row_cells)
    
    if not data_rows:
        return ""
    
    # Create LaTeX table
    col_spec = 'l' * num_cols
    latex_table = f"""
\\begin{{table}}[H]
\\centering
\\begin{{tabular}}{{@{{}}{col_spec}@{{}}}}
\\toprule
"""
    
    # Add header
    processed_header = [process_markdown_formatting(cell) for cell in header_cells]
    latex_table += " & ".join([f"\\textbf{{{cell}}}" for cell in processed_header]) + " \\\\\n\\midrule\n"
    
    # Add data rows
    for row in data_rows:
        processed_row = [process_markdown_formatting(cell) for cell in row]
        latex_table += " & ".join(processed_row) + " \\\\\n"
    
    latex_table += """\\bottomrule
\\end{tabular}
\\end{table}

"""
    
    return latex_table

def markdown_to_latex(markdown_content, style="modern", include_toc=True, title=None, author=None):
    """Convert markdown content to LaTeX"""
    
    lines = markdown_content.split('\n')
    latex_lines = []
    
    # Extract title from first header if not provided
    if not title:
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                break
    
    # Add template header
    latex_lines.append(get_latex_template(style, include_toc, title, author))
    
    in_list = False
    in_code_block = False
    in_table = False
    table_lines = []
    code_block_content = []
    
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        
        # Handle code blocks
        if line.startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_block_content = []
                language = line[3:].strip()
                if language:
                    latex_lines.append(f"\\begin{{lstlisting}}[language={language}]\n")
                else:
                    latex_lines.append("\\begin{lstlisting}\n")
            else:
                latex_lines.append("\\end{lstlisting}\n\n")
                in_code_block = False
                code_block_content = []
        elif in_code_block:
            # Don't process content inside code blocks
            latex_lines.append(line + '\n')
        
        # Handle headers (only if not in code block)
        elif line.startswith('# ') and not in_code_block:
            if in_list:
                latex_lines.append('\\end{itemize}\n')
                in_list = False
            header_text = process_markdown_formatting(line[2:].strip())
            latex_lines.append(f'\\section{{{header_text}}}\n')
            
        elif line.startswith('## ') and not in_code_block:
            if in_list:
                latex_lines.append('\\end{itemize}\n')
                in_list = False
            header_text = process_markdown_formatting(line[3:].strip())
            latex_lines.append(f'\\subsection{{{header_text}}}\n')
            
        elif line.startswith('### ') and not in_code_block:
            if in_list:
                latex_lines.append('\\end{itemize}\n')
                in_list = False
            header_text = process_markdown_formatting(line[4:].strip())
            latex_lines.append(f'\\subsubsection{{{header_text}}}\n')
            
        elif line.startswith('#### ') and not in_code_block:
            if in_list:
                latex_lines.append('\\end{itemize}\n')
                in_list = False
            header_text = process_markdown_formatting(line[5:].strip())
            latex_lines.append(f'\\paragraph{{{header_text}}}\n')
        
        # Handle lists (only if not in code block)
        elif (line.startswith('- ') or line.startswith('* ') or 
              re.match(r'^\d+\. ', line)) and not in_code_block:
            if not in_list:
                latex_lines.append('\\begin{itemize}\n')
                in_list = True
            
            # Extract list content
            if line.startswith(('- ', '* ')):
                content = line[2:].strip()
            else:
                content = re.sub(r'^\d+\. ', '', line).strip()
            
            content = process_markdown_formatting(content)
            latex_lines.append(f'\\item {content}\n')
        
        # Handle tables (only if not in code block)
        elif '|' in line and line.strip() and not in_code_block:
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(line)
            
        # Handle empty lines
        elif line.strip() == '':
            if in_list:
                latex_lines.append('\\end{itemize}\n')
                in_list = False
            if in_table and table_lines:
                latex_lines.append(convert_table(table_lines))
                in_table = False
                table_lines = []
            if not in_code_block:
                latex_lines.append('\n')
        
        # Handle regular text (only if not in code block)
        elif not in_code_block:
            if in_list:
                latex_lines.append('\\end{itemize}\n')
                in_list = False
            if in_table:
                table_lines.append(line)
            else:
                processed_line = process_markdown_formatting(line)
                latex_lines.append(f'{processed_line}\n\n')
        
        i += 1
    
    # Close any remaining environments
    if in_list:
        latex_lines.append('\\end{itemize}\n')
    if in_table and table_lines:
        latex_lines.append(convert_table(table_lines))
    if in_code_block:
        latex_lines.append('\\end{lstlisting}\n')
    
    # Add document footer
    latex_lines.append('\\end{document}\n')
    
    return ''.join(latex_lines)

def compile_latex_to_pdf(latex_content, output_path):
    """Compile LaTeX content to PDF"""
    
    # Convert to absolute path to avoid issues with directory changes
    output_path = Path(output_path).absolute()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        
        # Write LaTeX file
        tex_file = temp_dir_path / 'document.tex'
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        # Change to temp directory for compilation
        original_dir = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            # Run pdflatex (twice for cross-references)
            for i in range(2):
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', 'document.tex'],
                    capture_output=True, text=True, encoding='utf-8', errors='ignore'
                )
            
            # Check if PDF was created
            pdf_file = temp_dir_path / 'document.pdf'
            if pdf_file.exists():
                # Copy PDF to output location
                try:
                    shutil.copy2(pdf_file, output_path)
                    return True
                except Exception as e:
                    print(f"❌ Error copying PDF: {e}")
                    return False
            else:
                print("❌ PDF file was not created by LaTeX")
                print(f"Return code: {result.returncode}")
                if result.stderr:
                    print(f"Error: {result.stderr[-800:]}")
                if result.stdout:
                    print(f"Output: {result.stdout[-800:]}")
                return False
                
        except Exception as e:
            print(f"❌ Exception during compilation: {e}")
            return False
        finally:
            os.chdir(original_dir)

def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown files to professional PDFs using LaTeX',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -i README.md README.pdf
  %(prog)s --input report.md --output report.pdf
  %(prog)s -i notes.md notes.pdf --style academic --title "My Notes"
  %(prog)s -i doc.md doc.pdf --no-toc --author "John Doe"
        """
    )
    
    parser.add_argument('-i', '--input', required=True,
                       help='Input markdown file')
    parser.add_argument('output', 
                       help='Output PDF file')
    parser.add_argument('--style', choices=['modern', 'academic', 'minimal'], 
                       default='modern',
                       help='Document style (default: modern)')
    parser.add_argument('--no-toc', action='store_true',
                       help='Disable table of contents')
    parser.add_argument('--title',
                       help='Document title (extracted from first header if not specified)')
    parser.add_argument('--author',
                       help='Document author')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # Validate input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ Error: Input file '{args.input}' not found")
        sys.exit(1)
    
    # Validate output path
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if args.verbose:
        print(f"📖 Reading markdown file: {input_path}")
    
    # Read markdown content
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
    except Exception as e:
        print(f"❌ Error reading input file: {e}")
        sys.exit(1)
    
    if args.verbose:
        print(f"🔄 Converting to LaTeX (style: {args.style})...")
    
    # Convert to LaTeX
    latex_content = markdown_to_latex(
        markdown_content,
        style=args.style,
        include_toc=not args.no_toc,
        title=args.title,
        author=args.author
    )
    
    if args.verbose:
        print("🔄 Compiling PDF...")
    
    # Compile to PDF
    success = compile_latex_to_pdf(latex_content, output_path)
    
    if success and output_path.exists():
        file_size = output_path.stat().st_size / 1024
        print(f"✅ PDF successfully generated: {output_path}")
        print(f"📊 File size: {file_size:.1f} KB")
    else:
        print("❌ PDF generation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()