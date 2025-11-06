import hashlib
import os
import sys

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


def get_file_size(f):
    f.seek(0, 2)
    size = f.tell()
    f.seek(0)
    return size


@app.route("/")
def upload():
    return render_template("file_upload_form.html")


@app.route("/upload", methods=["POST"])
def success():
    file = request.files["file"]
    if not file:
        return jsonify({"status": "error", "message": "No file uploaded"}), 400

    if not os.path.isdir("uploads"):
        os.mkdir("uploads")

    fname = hashlib.md5(os.urandom(16)).hexdigest()

    with open(os.path.join("uploads", f"{fname}.meta"), "w+") as f:
        f.write(
            f"""################################
## Metadata for received file ##
################################

original_filename: {file.filename}
file_size: {get_file_size(file)}
"""
        )

    with open(os.path.join("uploads", f"{fname}.data"), "wb+") as f:
        f.write(file.read())

    print(f"Saved file {
          file.filename} as uploads/{fname}.data", file=sys.stderr)

    return jsonify({"status": "success", "filename": file.filename})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)
