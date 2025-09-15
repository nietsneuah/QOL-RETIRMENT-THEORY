"""
FINAL REPORT SUMMARY PDF GENERATOR

Converts the Final Report Summary from Markdown to professional LaTeX/PDF format
"""

import os
import subprocess
from pathlib import Path
from datetime import datetime

def create_latex_document():
    """Generate LaTeX document for Final Report Summary"""
    
    latex_content = r"""
\documentclass[11pt,letterpaper]{article}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{array}
\usepackage{longtable}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{fancyhdr}
\usepackage{hyperref}

% Page setup
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{QOL Framework Analysis}
\fancyhead[R]{Final Report Summary}
\fancyfoot[C]{\thepage}

% Colors
\definecolor{codegreen}{rgb}{0,0.6,0}
\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\definecolor{codepurple}{rgb}{0.58,0,0.82}
\definecolor{backcolour}{rgb}{0.95,0.95,0.92}

% Code style
\lstdefinestyle{mystyle}{
    backgroundcolor=\color{backcolour},   
    commentstyle=\color{codegreen},
    keywordstyle=\color{magenta},
    numberstyle=\tiny\color{codegray},
    stringstyle=\color{codepurple},
    basicstyle=\ttfamily\footnotesize,
    breakatwhitespace=false,         
    breaklines=true,                 
    captionpos=b,                    
    keepspaces=true,                 
    numbers=left,                    
    numbersep=5pt,                  
    showspaces=false,                
    showstringspaces=false,
    showtabs=false,                  
    tabsize=2
}
\lstset{style=mystyle}

\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    filecolor=magenta,      
    urlcolor=cyan,
}

\title{\textbf{QOL Framework Analysis\\Final Report Summary}}
\author{Quality of Life Retirement Theory Research}
\date{September 15, 2025}

\begin{document}

\maketitle

\begin{abstract}
This report presents the final summary of the Quality of Life (QOL) Framework Analysis for retirement planning strategies. The analysis provides corrected implementations of both the Trinity Study baseline and QOL enhancement strategies, with comprehensive validation and comparative performance metrics. Key findings demonstrate that QOL strategies offer higher total income but with significantly increased portfolio depletion risk, representing a fundamental risk-preference trade-off rather than optimization.
\end{abstract}

\tableofcontents
\newpage

\section{Major Corrections Applied}

\subsection{Trinity Study Inflation Fix}
\textbf{Problem:} Inflation was applied in Year 1, making first withdrawal \$41,200 instead of \$40,000.

\textbf{Solution:} Apply inflation factor AFTER withdrawal calculation.

\textbf{Result:} Trinity Study now correctly provides exactly \$40,000 real purchasing power in Year 1.

\subsection{QOL Framework Fundamental Rebase}
\textbf{Problem:} QOL was implemented as percentage-of-current-balance (completely different approach).

\textbf{Solution:} Changed to Trinity Study base × QOL multipliers (true comparative framework).

\textbf{Result:} QOL strategies now meaningfully comparable to Trinity Study.

\section{Corrected Results Summary}

\subsection{Performance Comparison}
Table~\ref{tab:performance} shows the performance comparison in real Year 1 dollars.

\begin{table}[h!]
\centering
\begin{tabular}{@{}lcccc@{}}
\toprule
\textbf{Strategy} & \textbf{Total Real Income} & \textbf{Final Portfolio} & \textbf{Depletion Rate} & \textbf{Success Rate} \\
\midrule
Trinity Study & \$829,120 & \$68,472 & 84.6\% & 11.6\% \\
QOL Standard & \$885,562 & \$41,028 & 90.0\% & 7.2\% \\
QOL Enhanced & \$943,895 & \$14,630 & 96.9\% & 2.7\% \\
\bottomrule
\end{tabular}
\caption{Performance Comparison (Real Year 1 Dollars)}
\label{tab:performance}
\end{table}

\subsection{Key Insights from Corrected Analysis}
\begin{enumerate}
    \item \textbf{QOL strategies provide higher total income} (+6.8\% to +13.8\%)
    \item \textbf{But with significantly higher depletion risk} (+5.4\% to +12.3\% higher depletion rates)
    \item \textbf{Trinity Study is more conservative} in portfolio preservation
    \item \textbf{QOL represents risk preference trade-off}, not superior performance
\end{enumerate}

\section{Implementation Details}

\subsection{QOL Multiplier System (Corrected)}
\begin{lstlisting}[language=Python, caption=QOL Multiplier Implementation]
# QOL Multiplier System
Year 1-10 (Phase 1): Trinity Base × 1.35 (Peak enjoyment years)
Year 11-20 (Phase 2): Trinity Base × 1.125 (Comfortable years)  
Year 21-29 (Phase 3): Trinity Base × 0.875 (Care years)
\end{lstlisting}

\subsection{Trinity Study Foundation}
\begin{lstlisting}[language=Python, caption=Trinity Study Implementation]
Base Withdrawal = $40,000 × Cumulative Inflation Factor
QOL Withdrawal = Base Withdrawal × QOL Multiplier
\end{lstlisting}

\section{Generated Output Files}

\subsection{Charts (output/charts/)}
\begin{itemize}
    \item \texttt{comprehensive\_qol\_analysis.png} - 9-panel comprehensive analysis
    \item \texttt{real\_dollar\_comparison.png} - Real purchasing power comparison
    \item \texttt{strategy\_comparison.png} - Strategy performance comparison
\end{itemize}

\subsection{Data (output/data/)}
\begin{itemize}
    \item \texttt{comprehensive\_qol\_analysis.csv} - Detailed year-by-year analysis
    \item \texttt{strategy\_comparison\_table.csv} - Strategy implementation details
    \item \texttt{risk\_analysis\_table.csv} - Risk-adjusted performance metrics
    \item \texttt{real\_dollar\_comparison.csv} - Real purchasing power data
    \item \texttt{trinity\_verification.csv} - Trinity Study validation data
\end{itemize}

\subsection{Reports (output/reports/)}
\begin{itemize}
    \item \texttt{qol\_framework\_summary\_report.md} - Executive summary (Markdown)
    \item \texttt{qol\_framework\_comprehensive\_report.tex} - Professional report (LaTeX)
    \item \texttt{strategy\_comparison\_summary.txt} - Quick comparison summary
\end{itemize}

\section{Academic Implications}

\subsection{Methodological Contributions}
\begin{enumerate}
    \item \textbf{Proper Trinity Study implementation} with correct inflation timing
    \item \textbf{QOL framework as risk preference model} rather than optimization
    \item \textbf{Real purchasing power normalization} for meaningful comparisons
    \item \textbf{Monte Carlo validation} with realistic market assumptions
\end{enumerate}

\subsection{Research Applications}
\begin{itemize}
    \item Retirement planning strategy comparison
    \item Risk tolerance modeling in withdrawal strategies
    \item Quality of life considerations in financial planning
    \item Front-loading vs. preservation trade-off analysis
\end{itemize}

\section{Validation Completed}
\begin{itemize}
    \item [\checkmark] Trinity Study produces exactly \$40,000 real withdrawals annually
    \item [\checkmark] QOL strategies use Trinity foundation with correct multipliers
    \item [\checkmark] Inflation adjustments applied consistently across strategies
    \item [\checkmark] Real purchasing power calculations verified
    \item [\checkmark] Monte Carlo simulation results validated
\end{itemize}

\section{Decision Framework}

\subsection{Choose Trinity Study If:}
\begin{itemize}
    \item Portfolio preservation is primary concern
    \item Steady, predictable withdrawals preferred
    \item Lower risk tolerance for depletion
    \item Legacy/inheritance planning important
\end{itemize}

\subsection{Choose QOL Framework If:}
\begin{itemize}
    \item Early retirement enjoyment prioritized
    \item Comfortable with higher depletion risk
    \item Prefer front-loaded consumption
    \item Less concerned about late-life preservation
\end{itemize}

\section{Important Notes}
\begin{itemize}
    \item Analysis uses conservative 1.5\% real return assumption
    \item 15\% volatility reflects realistic market conditions
    \item 3\% inflation with variability included
    \item Professional financial advice recommended for personal decisions
    \item Healthcare and long-term care costs not explicitly modeled
\end{itemize}

\section{Conclusion}

\textbf{Status:} Framework mathematically validated and ready for academic presentation/publication.

\textbf{Next Steps:} Framework can be used for sensitivity analysis, parameter optimization, or extended research applications.

The QOL Framework Analysis demonstrates a rigorous approach to comparing retirement withdrawal strategies with proper mathematical foundations. The corrected implementation provides a solid basis for both academic research and practical retirement planning applications.

\end{document}
"""
    
    return latex_content

def generate_pdf():
    """Generate PDF from LaTeX source"""
    
    # Find project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Create output directory
    output_dir = project_root / 'output' / 'reports'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate LaTeX content
    latex_content = create_latex_document()
    
    # Write LaTeX file
    latex_file = output_dir / 'final_report_summary.tex'
    with open(latex_file, 'w') as f:
        f.write(latex_content)
    
    print(f"📄 LaTeX file created: {latex_file}")
    
    # Generate PDF using pdflatex
    try:
        # Change to output directory for compilation
        original_dir = os.getcwd()
        os.chdir(output_dir)
        
        # Run pdflatex twice for proper cross-references and TOC
        print("🔄 Compiling LaTeX to PDF (first pass)...")
        result1 = subprocess.run(['pdflatex', '-interaction=nonstopmode', 'final_report_summary.tex'], 
                                capture_output=True, text=True, encoding='utf-8', errors='ignore')
        
        print("🔄 Compiling LaTeX to PDF (second pass)...")
        result2 = subprocess.run(['pdflatex', '-interaction=nonstopmode', 'final_report_summary.tex'], 
                                capture_output=True, text=True, encoding='utf-8', errors='ignore')
        
        # Return to original directory
        os.chdir(original_dir)
        
        if result2.returncode == 0:
            pdf_file = output_dir / 'final_report_summary.pdf'
            print(f"✅ PDF successfully generated: {pdf_file}")
            print(f"📊 File size: {pdf_file.stat().st_size / 1024:.1f} KB")
            
            # Clean up auxiliary files
            aux_files = ['*.aux', '*.log', '*.toc', '*.out']
            for pattern in aux_files:
                for file in output_dir.glob(pattern):
                    file.unlink()
            
            return str(pdf_file)
        else:
            print(f"❌ LaTeX compilation failed:")
            print(result2.stderr)
            return None
            
    except Exception as e:
        print(f"❌ Error during PDF generation: {e}")
        return None

if __name__ == "__main__":
    print("🚀 FINAL REPORT SUMMARY PDF GENERATOR")
    print("=" * 50)
    
    pdf_path = generate_pdf()
    
    if pdf_path:
        print(f"\n🎉 PDF generation complete!")
        print(f"📁 Location: {pdf_path}")
        print(f"\n💡 The PDF includes:")
        print("   • Professional LaTeX formatting")
        print("   • Table of contents")
        print("   • Properly formatted tables")
        print("   • Code syntax highlighting")
        print("   • Academic-quality typography")
    else:
        print("\n❌ PDF generation failed. Check the error messages above.")