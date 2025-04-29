import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def autosave_form_pdf(
    output_dir: str,
    filename: str,
    fields: dict,
    template_path: str = None
) -> str:
    """
    If template_path is provided:
      • if it’s a form‑enabled PDF, fills via PyPDF2 (fill_pdf_form)
      • if it’s a flat PDF, overlays via pdfrw+reportlab (fill_pdf_overlay)
      • if it’s a .docx, renders via docxtpl+docx2pdf (fill_docx_and_export_pdf)
    Otherwise falls back to plain ReportLab text.
    """
    os.makedirs(output_dir, exist_ok=True)
    basename, _ = os.path.splitext(filename)
    out_pdf = os.path.join(output_dir, basename + ".pdf")

    if template_path:
        ext = os.path.splitext(template_path)[1].lower()
        if ext == ".pdf":
            try:
                from pdf_helper import fill_pdf_form
                return fill_pdf_form(template_path, out_pdf, fields)
            except Exception:
                from pdf_helper import fill_pdf_overlay
                return fill_pdf_overlay(template_path, out_pdf, fields)
        elif ext == ".docx":
            from pdf_helper import fill_docx_and_export_pdf
            return fill_docx_and_export_pdf(template_path, output_dir, basename, fields)

    # fallback: simple ReportLab text dump
    c = canvas.Canvas(out_pdf, pagesize=letter)
    y = 750
    for label, value in fields.items():
        c.drawString(50, y, f"{label}: {value}")
        y -= 20
        if y < 50:
            c.showPage()
            y = 750
    c.save()
    return out_pdf
