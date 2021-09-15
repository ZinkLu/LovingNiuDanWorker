from pathlib import Path
from string import Template
from uuid import uuid4

import docx
from utils.logger import logger

T_FILE = Path("templates") / "template.docx"
OUT_PUT = Path("output")

OUT_PUT.mkdir(exist_ok=True)


def render_docx(context=None) -> Path:
    """由于存在参数跨run的情况，如果遇到这种情况将其合并成同一个run"""
    file = OUT_PUT / f'{uuid4()}.docx'
    with file.open('wb') as f, T_FILE.open("rb") as t:
        f.write(t.read())

    context = context or dict()
    doc = docx.Document(file)

    for para in doc.paragraphs:
        start_run = None
        start_run_text = ""

        for run in para.runs:
            temp_text = run.text

            if start_run and "$" not in temp_text:
                if "}" in temp_text:
                    start_run_text += temp_text
                    line = Template(start_run_text).safe_substitute(**context)
                    start_run.text = line
                    start_run = None
                    start_run_text = ""
                else:
                    start_run_text += temp_text

                run.text = ''
                continue

            if "$" in temp_text and "}" not in temp_text:
                start_run = run
                start_run_text = run.text
                continue
            else:
                if start_run is not None:
                    logger.warning("start run is not closed, please check you template file")
                start_run = None
                start_run_text = ""
                line = Template(temp_text).safe_substitute(**context)
                run.text = line

    doc.save(file)

    return file


if __name__ == "__main__":
    render_docx({'name': "小明", 'gender': "男", 'con': "天蝎座"})
