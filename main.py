#!/usr/bin/python3

from subprocess import call
import sys

target = sys.argv[1]  # Get file to read from command line arguments

# Read contents of input file
with open(target, "r", encoding="utf-8") as f:
    content = f.read()


# Split input into parts
s1 = content.split("\n\n\n")

headers = s1[0].split("\n")  # Separate header info

paragraphs = s1[1].split("\n\n")  # Separate paragraphs

citations = s1[2].split("\n\n")  # Separate citations

del s1  # Remove unused var


# Identify header information
last = headers[0]
title = headers[1]
full = headers[2]
teacher = headers[3]
class_ = headers[4]
date = headers[5]

del headers  # Remove unused var


# TODO: Add italics (\textit) to applicable parts of citations


paragraphs = '\n\n'.join(paragraphs)  # Combine paragraphs into continuous string
citations = '\\bibent\n' + '\n\n\\bibent\n'.join(citations)  # Combine citations into continuous string


base = [r"""\documentclass[12pt, letterpaper]{article}

%UTF-8
%\usepackage{utf8}

%Margin - 1 inch on all sides
\usepackage[letterpaper]{geometry}
\usepackage{times}
\geometry{top=1.0in, bottom=1.0in, left=1.0in, right=1.0in}

%Doublespacing
\usepackage{setspace}
\doublespacing

%Rotating tables (e.g. sideways when too long)
\usepackage{rotating}

%Fancy-header package to modify header/page numbering (insert last name)
\usepackage{fancyhdr}
\pagestyle{fancy}
\lhead{}
\chead{}
\rhead{""", last, r""" \thepage}
\lfoot{}
\cfoot{}
\rfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
%To make sure we actually have header 0.5in away from top edge
%12pt is one-sixth of an inch. Subtract this from 0.5in to get headsep value
\setlength\headsep{0.333in}

%Works cited environment
%(to start, use \begin{workscited...}, each entry preceded by \bibent)
\newcommand{\bibent}{\noindent \hangindent 40pt}
\newenvironment{workscited}{\newpage \begin{center} Works Cited \end{center}}{\newpage }


\begin{document}
\begin{flushleft}

""", full, r"""\\
""", teacher, r"""\\
""", class_, r"""\\
""", date, r"""\\

%Title
\begin{center}
""", title, r"""
\end{center}

%Changes paragraph indentation to 0.5in
\setlength{\parindent}{0.5in}

%Begin body of paper here

""", paragraphs, r"""

\newpage

%%Works cited
\begin{workscited}

""", citations, r"""
\end{workscited}

\end{flushleft}
\end{document}"""]

towrite = "{}.tex".format(target)

with open(towrite, "w+") as f:
    f.write(''.join(base))

call(["pdflatex", towrite])

print('Done.')
