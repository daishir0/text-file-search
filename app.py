from flask import Flask, render_template, request, jsonify
import os
import codecs

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    keyword = request.form.get("keyword")
    results = {}
    for subdir, dirs, files in os.walk('.'):
        for file in files:
            if file == 'scripts_improved.txt':
                filepath = os.path.join(subdir, file)
                with codecs.open(filepath, "r", encoding='utf-8') as f:
                    lines = f.readlines()
                    for idx, line in enumerate(lines):
                        if keyword in line:
                            context = []
                            start_line_number = max(0, idx - 5)
                            end_line_number = min(idx + 5, len(lines) - 1)
                            for i in range(start_line_number, end_line_number + 1):
                                context.append(lines[i].strip())
                            if subdir not in results:
                                results[subdir] = []
                            results[subdir].append({"filename": file, "line_number": idx, "context": "\n".join(context)})
    return jsonify(results)

if __name__ == "__main__":
     app.run(host="0.0.0.0", debug=False, port=15613)

