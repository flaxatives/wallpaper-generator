from bottle import get, post, request, run, static_file, Bottle, redirect
import subprocess
import os

app = Bottle()
root = "."

@app.get("/")
def wallpaper():
    return static_file("wallpaper_form.html", root=root)

@app.post("/")
def do_wallpaper():
    text = request.forms.get("text")
    if len(text) > 100:
        return "<h1>Message must be less than 100</h1>"
    else:
        # generate magic
        filename = subprocess.check_output([root + "/generatewallpaper.sh", text])
        filename = filename.decode("utf-8").strip()
        if os.path.isfile("/tmp/"+filename):
            redirect("i/" + filename)
        else:
            return "Image generation failed."

@app.get("/i/<filename>")
def get_image(filename):
    if os.path.isfile("/tmp/"+filename):
        return static_file(filename, root="/tmp")



if __name__ == "__main__":
    app.run(host="localhost",
            port=9090,
            debug=True)
