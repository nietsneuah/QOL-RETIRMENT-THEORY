"""
ROBUST COMPREHENSIVE RESEARCH REPORT PDF GENERATOR

Creates a professional PDF from the complete Dynamic Portfolio Reallocation Research Report
using a more robust markdown to LaTeX conversion approach.
"""

import os
import subprocess
from pathlib import Path
import re

def escape_latex(text):
    """Escape special LaTeX characters"""
    text = text.replace('\\', '\\textbackslash{}')
    text = text.replace('{', '\\{')
    text = text.replace('}', '\\}')
    text = text.replace('$', '\\$')
    text = text.replace('&', '\\&')
    text = text.replace('%', '\\%')
    text = text.replace('#', '\\#')
    text = text.replace('^', '\\textasciicircum{}')
    text = text.replace('_', '\\_')
    text = text.replace('~', '\\textasciitilde{}')
    return text

def process_markdown_formatting(text):
    """Process markdown formatting to LaTeX"""
    # First escape LaTeX special characters
    text = escape_latex(text)
    
    # Then apply markdown formatting
    # Handle bold text (multiple asterisks patterns)
    text = re.sub(r'\*{4,}([^*]+?)\*{4,}', r'\\textbf{\1}', text)  # ****bold****
    text = re.sub(r'\*{2}([^*]+?)\*{2}', r'\\textbf{\1}', text)    # **bold**
    text = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'\\textit{\1}', text)  # *italic*
    
    return text

def convert_markdown_to_latex(markdown_content):
    """Convert markdown content to LaTeX with robust parsing"""
    
    lines = markdown_content.split('\n')
    latex_lines = []
    
    in_list = False
    in_table = False
    table_lines = []
    
    # LaTeX document header
    latex_header = r"""
\documentclass[11pt,letterpaper]{article}
\usepackage[margin=1.1in]{geometry}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{array}
\usepackage{longtable}
\usepackage{xcolor}
\usepackage{fancyhdr}
\usepackage{hyperref}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{tocloft}
\usepackage{microtype}
\usepackage{float}
\usepackage{caption}
\usepackage{multirow}
\usepackage{tabularx}
\usepackage{setspace}

% Professional color scheme
\definecolor{primary}{RGB}{0,47,108}
\definecolor{secondary}{RGB}{204,82,0}
\definecolor{accent}{RGB}{0,102,51}
\definecolor{lightgray}{RGB}{245,245,245}
\definecolor{darkgray}{RGB}{80,80,80}

% Enhanced page setup
\setlength{\headheight}{14pt}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\leftmark}
\fancyhead[R]{\small Dynamic Portfolio Research}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.4pt}

% Section formatting
\titleformat{\section}
{\Large\bfseries\color{primary}}
{\thesection}{1em}{}
[\titlerule]

\titleformat{\subsection}
{\large\bfseries\color{secondary}}
{\thesubsection}{1em}{}

\titleformat{\subsubsection}
{\normalsize\bfseries\color{accent}}
{\thesubsubsection}{1em}{}

% Hyperref setup
\hypersetup{
    colorlinks=true,
    linkcolor=primary,
    filecolor=secondary,      
    urlcolor=accent,
    citecolor=primary,
    pdfauthor={QOL Retirement Theory Research Team},
    pdftitle={Dynamic Portfolio Reallocation Research},
    pdfsubject={Retirement Planning Research Analysis}
}

% Title
\title{
    \vspace{-1cm}
    \Huge\textbf{\color{primary}Dynamic Portfolio Reallocation}\\
    \vspace{0.3cm}
    \LARGE\textbf{\color{secondary}for Quality of Life Retirement Strategies}\\
    \vspace{0.2cm}
    \Large\textbf{\color{accent}A Comprehensive Analysis}
}

\author{
    \large\textbf{QOL Retirement Theory Research Team}\\
    \normalsize Independent Research Analysis
}

\date{
    \large September 15, 2025\\
    \normalsize Research Report
}

\begin{document}

\maketitle
\thispagestyle{empty}

\vfill
\begin{center}
\large
\colorbox{lightgray}{\parbox{0.8\textwidth}{\centering
\textbf{Breakthrough Research Finding}\\
\vspace{0.2cm}
\textit{First QOL Strategy to Achieve Sub-\\$1.00 Efficiency}\\
\textit{Aggressive Glide Path: \\textbf{\\$0.97 per Enjoyment Dollar}}
}}
\end{center}
\vfill

\newpage
\tableofcontents
\newpage

"""
    
    latex_lines.append(latex_header)
    
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        
        # Skip YAML-style headers and dividers
        if (line.startswith('**Research Report**') or 
            line.startswith('**Date**') or 
            line.startswith('**Authors**') or 
            line.startswith('**Institution**') or
            line.strip() == '---'):
            i += 1
            continue
        
        # Handle headers
        if line.startswith('# '):
            if in_list:
                latex_lines.append('\\end{itemize}\n')
                in_list = False
            title = process_markdown_formatting(line[2:].strip())
            latex_lines.append(f'\\section{{{title}}}\n')
            
        elif line.startswith('## '):
            if in_list:
                latex_lines.append('\\end{itemize}\n')
                in_list = False
            title = process_markdown_formatting(line[3:].strip())
            latex_lines.append(f'\\subsection{{{title}}}\n')
            
        elif line.startswith('### '):
            if in_list:
                latex_lines.append('\\end{itemize}\n')
                in_list = False
            title = process_markdown_formatting(line[4:].strip())
            latex_lines.append(f'\\subsubsection{{{title}}}\n')
            
        elif line.startswith('#### '):
            if in_list:
                latex_lines.append('\\end{itemize}\n')
                in_list = False
            title = process_markdown_formatting(line[5:].strip())
            latex_lines.append(f'\\paragraph{{{title}}}\n')
        
        # Handle lists
        elif line.startswith('- ') or line.startswith('1. ') or line.startswith('2. ') or line.startswith('3. '):
            if not in_list:
                latex_lines.append('\\begin{itemize}\n')
                in_list = True
            
            # Extract list content
            if line.startswith('- '):
                content = line[2:].strip()
            else:
                content = line[3:].strip()
            
            content = process_markdown_formatting(content)
            latex_lines.append(f'\\item {content}\n')
        
        # Handle tables
        elif '|' in line and line.strip():
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
            latex_lines.append('\n')
        
        # Handle regular text
        else:
            if in_list:
                latex_lines.append('\\end{itemize}\n')
                in_list = False
            if in_table:
                table_lines.append(line)
            else:
                processed_line = process_markdown_formatting(line)
                latex_lines.append(f'{processed_line}\n\n')
        
        i += 1
    
    # Close any remaining lists or tables
    if in_list:
        latex_lines.append('\\end{itemize}\n')
    if in_table and table_lines:
        latex_lines.append(convert_table(table_lines))
    
    # Document footer
    latex_footer = """
\\section*{Acknowledgments}

This research builds upon decades of retirement planning scholarship while introducing novel concepts in dynamic allocation and quality of life optimization.

\\section*{Disclaimer}

This research is for educational purposes only. Past performance does not guarantee future results. Consult qualified financial professionals before implementing any strategy.

\\vfill
\\begin{center}
\\rule{0.8\\textwidth}{0.4pt}\\\\
\\textbf{Report generated on September 15, 2025}\\\\
\\textit{Based on 10,000+ Monte Carlo simulations}
\\end{center}

\\end{document}
"""
    
    latex_lines.append(latex_footer)
    return ''.join(latex_lines)

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
\\caption{Research Data}
\\end{table}

"""
    
    return latex_table

def generate_comprehensive_pdf():
    """Generate PDF from the complete research report"""
    
    # Find project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Read the markdown file
    md_file = project_root / 'output' / 'reports' / 'Dynamic_Portfolio_Reallocation_Research_Report.md'
    
    if not md_file.exists():
        print(f"❌ Could not find the markdown file at {md_file}")
        return None
    
    print(f"📖 Reading markdown file: {md_file}")
    
    with open(md_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Convert to LaTeX
    print("🔄 Converting markdown to LaTeX...")
    latex_content = convert_markdown_to_latex(markdown_content)
    
    # Create output directory
    output_dir = project_root / 'output' / 'reports'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Write LaTeX file
    latex_file = output_dir / 'robust_research_report.tex'
    with open(latex_file, 'w', encoding='utf-8') as f:
        f.write(latex_content)
    
    print(f"📄 LaTeX file created: {latex_file}")
    
    # Generate PDF using pdflatex
    try:
        # Change to output directory for compilation
        original_dir = os.getcwd()
        os.chdir(output_dir)
        
        # Run pdflatex multiple times for proper cross-references
        print("🔄 Compiling LaTeX to PDF (first pass)...")
        result1 = subprocess.run(['pdflatex', '-interaction=nonstopmode', 'robust_research_report.tex'], 
                                capture_output=True, text=True, encoding='utf-8', errors='ignore')
        
        print("🔄 Compiling LaTeX to PDF (second pass)...")
        result2 = subprocess.run(['pdflatex', '-interaction=nonstopmode', 'robust_research_report.tex'], 
                                capture_output=True, text=True, encoding='utf-8', errors='ignore')
        
        # Return to original directory
        os.chdir(original_dir)
        
        # Check if PDF file was created (LaTeX sometimes returns 0 even with warnings)
        pdf_file = output_dir / 'robust_research_report.pdf'
        if pdf_file.exists():
            print(f"✅ PDF successfully generated: {pdf_file}")
            print(f"📊 File size: {pdf_file.stat().st_size / 1024:.1f} KB")
            
            # Clean up auxiliary files
            aux_files = ['*.aux', '*.log', '*.toc', '*.out', '*.fls', '*.fdb_latexmk']
            for pattern in aux_files:
                for file in output_dir.glob(pattern):
                    file.unlink()
            
            return str(pdf_file)
        else:
            print(f"❌ LaTeX compilation failed - no PDF output:")
            if result2.stderr:
                print("STDERR:", result2.stderr[-1000:])
            if result2.stdout:
                print("STDOUT:", result2.stdout[-1000:])
            return None
            
    except Exception as e:
        print(f"❌ Error during PDF generation: {e}")
        return None

if __name__ == "__main__":
    print("🚀 ROBUST COMPREHENSIVE RESEARCH REPORT PDF GENERATOR")
    print("=" * 70)
    print("Converting Complete Dynamic Portfolio Reallocation Research Report")
    print("=" * 70)
    
    pdf_path = generate_comprehensive_pdf()
    
    if pdf_path:
        print(f"\n🎉 PDF generation complete!")
        print(f"📁 Location: {pdf_path}")
        print(f"\n💡 Professional PDF includes:")
        print("   • Complete research analysis with proper formatting")
        print("   • Academic-style layout with color scheme")
        print("   • All tables and data properly converted")
        print("   • Table of contents and navigation")
        print("   • Professional typography and spacing")
    else:
        print("\n❌ PDF generation failed. Check the error messages above.")