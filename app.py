from pprint import pprint
from textwrap import wrap
from flask import Flask, jsonify, request,render_template

app = Flask(__name__)
methods = ["GET", "POST", "PATCH", "DELETE"]
app.config["DEBUG"] = True

@app.route("/", methods=methods, defaults={"path": ""})
@app.route("/<path:path>", methods=methods)
def hello_world(path):
    j = request.get_json()

    print(f"*** Received data at: {path}")

    if path == 'index.html':
        return render_template("index.html")


    print("\n** data:")
    print("\n".join(wrap(request.data.decode())))

    print("\n** form:")
    pprint(request.form)

    print("\n** json:")
    pprint(j)

    return jsonify(
        {
            "endpoint": path,
            "data": request.data.decode("utf-8"),
            "form": request.form,
            "json": request.get_json(),
        }
    )



if __name__ == "__main__":
    app.run()