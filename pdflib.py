#!/usr/local/bin/python
#! -*- coding: utf-8 -*-

"""
pbrian

library functions from lib.py but to do with pdf - just cleaning them
up

"""

def create_pdf(source, ltx_source, errors):
    """given source file create pdfs  

    2 steps - take rst and make latex, then take latex and make pdf
    """

    pdflatex_cmds = ['pdflatex', '--quiet', '--output-directory=%s' % latex_dir, '--interaction=nonstopmode']
    to_latex_cmds   = ['rst2latex.py']


    try: 
        to_latex_cmds.extend([source, ltx_source]) #src, dest  
        subprocess.check_call(to_latex_cmds)

        pdflatex_cmds.append(ltx_source)
        subprocess.check_call(pdflatex_cmds)

    except Exception, e:
        errors.append(e)

    abs_latex_dir = os.path.abspath(latex_dir)
    kill_pdf_odds(abs_latex_dir)


def kill_pdf_odds(abs_latex_dir):
    """given a file killoff any temp latex pdf files

    log, out, ltx """
    files = os.listdir(abs_latex_dir)

    for f in files:
        j, ext = os.path.splitext(f)
        if ext in (".log", ".aux", ".out"): 
            os.remove(os.path.join(abs_latex_dir, f))
