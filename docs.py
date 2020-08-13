import twl
from docx import Document
from docx.enum.section import WD_SECTION
from docx.shared import Inches


def _set_columns(section, cols):
    """
    sets number of columns through xpath.
    This is a workaround found on https://github.com/python-openxml/python-docx/issues/167
    calls to _set_columns(section, ...) should be replaced by section.set_... after the issue is
    fixed and set_columns or similar is added added to docx
    """
    section._sectPr.xpath("./w:cols")[0].set(_set_columns.WNS_COLS_NUM, str(cols))
    # section.right_margin = Inches(0)


_set_columns.WNS_COLS_NUM = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}num"


def fix_filename(fname):
    if fname.lower().endswith('.docx'):
        return fname

    return fname + '.docx'


def prep_words(words, end='\n'):
    return ''.join([w+end for w in words])


def doc_by_letter(wolf, cols, fname):
    doc = Document()
    _set_columns(doc.sections[-1], cols)

    for c in twl.letters:
        pup = wolf.starts(c)
        if len(pup) == 0:
            continue
        doc.add_paragraph(prep_words(pup.words))
        doc.add_section(WD_SECTION.CONTINUOUS)

    doc.save(fix_filename(fname))


wolf = twl.Wolf()

if __name__ == "__main__":
    doc_by_letter(wolf.len(3), 9, "3ltr")
