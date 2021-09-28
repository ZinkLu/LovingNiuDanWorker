import PyInstaller.__main__

PyInstaller.__main__.run([
    '--windowed',
    '--noconsole',
    '--add-data=configs/config.json;configs',
    '--add-data=templates/template.docx;templates',
    '--add-data=templates/example.png;templates',
    'main.py',
])
