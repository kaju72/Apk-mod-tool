from flask import Flask, request, send_file, render_template_string
import zipfile, os, shutil

app = Flask(__name__)

HTML_FORM = """
<!DOCTYPE html>
<html>
<head><title>APK Mod Generator</title></head>
<body>
<h2>Customize Dialog</h2>
<form action='/generate' method='post'>
Title: <input name='title'><br><br>
Message: <input name='message'><br><br>
Button 1: <input name='btn1'><br><br>
Button 2: <input name='btn2'><br><br>
Link: <input name='link'><br><br>
Color: <input name='color'><br><br>
<button type='submit'>Generate ZIP</button>
</form>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_FORM)

@app.route('/generate', methods=['POST'])
def generate():
    title = request.form['title']
    message = request.form['message']
    btn1 = request.form['btn1']
    btn2 = request.form['btn2']
    link = request.form['link']
    color = request.form['color']

    base_zip = 'Dialog_with_switch.zip'
    extract_to = 'temp_extract'
    output_zip = 'Generated_Dialog.zip'

    if os.path.exists(extract_to):
        shutil.rmtree(extract_to)
    os.makedirs(extract_to, exist_ok=True)

    with zipfile.ZipFile(base_zip, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    hook_file = os.path.join(extract_to, 'Hook.txt')
    if os.path.exists(hook_file):
        with open(hook_file, 'r', encoding='utf-8') as f:
            data = f.read()
        data = data.replace('{TITLE}', title).replace('{MESSAGE}', message)
        data = data.replace('{BTN1}', btn1).replace('{BTN2}', btn2)
        data = data.replace('{LINK}', link).replace('{COLOR}', color)
        with open(hook_file, 'w', encoding='utf-8') as f:
            f.write(data)

    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for root, _, files in os.walk(extract_to):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), extract_to))

    return send_file(output_zip, as_attachment=True)

if __name__ == '__main__':
    app.run()
