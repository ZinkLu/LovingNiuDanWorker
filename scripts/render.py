from pathlib import Path
from string import Template
from uuid import uuid4

import docx

T_FILE = Path("templates") / "template.docx"
OUT_PUT = Path("output")

OUT_PUT.mkdir(exist_ok=True)


def render_docx(context=None) -> Path:
    file = OUT_PUT / f'{uuid4()}.docx'
    with file.open('wb') as f, T_FILE.open("rb") as t:
        f.write(t.read())

    context = context or dict()
    doc = docx.Document(file)
    for para in doc.paragraphs:
        for run in para.runs:
            temp_text = run.text
            line = Template(temp_text).safe_substitute(**context)
            run.text = line
    doc.save(file)

    return file


if __name__ == "__main__":
    render_docx({'name': "小明", 'gender': "男", 'con': "天蝎座"})
