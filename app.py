from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Downloader</title>
    <style>
        body { background-color: #121212; color: #ffffff; font-family: Arial, sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }
        .container { background: #1e1e1e; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,255,100,0.2); width: 85%; max-width: 400px; text-align: center; }
        input[type="text"] { width: 90%; padding: 12px; margin-bottom: 15px; border: 1px solid #333; background: #2a2a2a; color: #fff; border-radius: 6px; }
        button { background-color: #00ff66; color: #000; border: none; padding: 12px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; width: 100%; }
        button:hover { background-color: #00cc52; }
        .success { margin-top: 15px; color: #00ff66; }
        .error { margin-top: 15px; color: #ff4d4d; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Video Downloader</h2>
        <form method="POST">
            <input type="text" name="url" placeholder="Paste link here..." required>
            <button type="submit">Download Video</button>
        </form>
        {% if success %}
            <div class="success">
                <p>Ready!</p>
                <a href="/download/{{ filename }}" style="color: #00ff66; font-weight: bold;">Click here to save file</a>
            </div>
        {% endif %}
        {% if error %}
            <div class="error"><p>{{ error }}</p></div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            return render_template_string(HTML_TEMPLATE, error="Please enter a valid URL.")
        try:
            ydl_opts = {
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
                'format': 'best',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            return render_template_string(HTML_TEMPLATE, success=True, filename=os.path.basename(filename))
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, error=str(e))
    return render_template_string(HTML_TEMPLATE)

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
  
