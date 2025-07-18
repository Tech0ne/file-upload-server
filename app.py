import hashlib
import os
import sys

from flask import Flask, render_template, request

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
    if request.method == "POST":
        file = request.files["file"]
        if not os.path.isdir("uploads"):
            os.mkdir("uploads")
        fname = hashlib.md5(os.urandom(16)).hexdigest()
        with open(os.path.join("uploads", f"{fname}.meta"), "w+") as f:
            f.write(
                f"""################################
## Metadata for received file ##
################################

original_filename: {file.filename.encode()}
file_size: {get_file_size(file)}
"""
            )
        with open(os.path.join("uploads", f"{fname}.data"), "wb+") as f:
            f.write(file.read())
        print(
            f"Saved file {file.filename.encode()} \
as uploads/{fname}.data",
            file=sys.stderr,
        )
        return render_template("success.html", name=file.filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)
