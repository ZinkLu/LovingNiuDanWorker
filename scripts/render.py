import hashlib
import urllib3
import base64
from pathlib import Path
from string import Template
from uuid import uuid4

import docx
from utils.logger import logger

T_FILE = Path("templates") / "template.docx"
OUT_PUT = Path("output").absolute()

OUT_PUT.mkdir(exist_ok=True)

PIC_MD5 = "529f754246ba9fe09f39e968f37d54bf"


def render_docx(context=None) -> Path:
    """由于存在参数跨run的情况，如果遇到这种情况将其合并成同一个run"""
    file = OUT_PUT / f'{uuid4()}.docx'
    with file.open('wb') as f, T_FILE.open("rb") as t:
        f.write(t.read())

    context = context or dict()
    doc = docx.Document(file)

    # 处理图片
    pic = context.get("picture_bytes")
    if pic:
        try:
            pic = base64.b64decode(pic)
        except:
            logger.error("图片文件解析失败")

    pic_url = context.get("picture_url")
    if not pic and pic_url:
        http = urllib3.PoolManager()

        try:
            logger.info("正在下载图片数据 :%s", pic_url)
            resp = http.request("GET", pic_url, timeout=10)
            logger.info("下载图片数据完成")
        except:
            logger.error("图片下载失败, url %s", pic_url)
        else:
            if resp.status == 200:
                pic = resp.data
            else:
                logger.error("图片下载失败, url %s", pic_url)

    if pic:
        # 使用 md5 作为模板
        for inline_shape in doc.inline_shapes:
            blip = inline_shape._inline.graphic.graphicData.pic.blipFill.blip
            rId = blip.embed
            document_part = doc.part
            image_part = document_part.related_parts[rId]
            if image_part._blob and hashlib.md5(image_part._blob).hexdigest() == PIC_MD5:
                image_part._blob = pic

    for para in doc.paragraphs:
        start_run = None
        start_run_text = ""

        for run in para.runs:
            temp_text = run.text

            if not temp_text:
                continue

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
