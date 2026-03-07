from bottle import route, run, static_file, get, post, request, template
import json


@route("/")
def index():
    return static_file("index.html", root="./")


@get("/<fp:path>")
def f(fp):
    return static_file(fp, root="./")


@get("/counter")
def gc():
    with open("msg.json") as mfr:
        count = len(json.load(mfr))
    return str(count)


@post("/messages")
def pm():

    m = request.json["msg"]  # pyright: ignore
    with open("msg.json") as mfr:
        mfjso = json.load(mfr)
    mfjso.append(
        {
            "id": max(mfjso, key=lambda i: i["id"])["id"] + 1 if len(mfjso) > 0 else 1,
            "content": m,
        }
    )
    with open("msg.json", "w") as mfw:
        json.dump(mfjso, mfw)
    return gm()


@get("/messages")
def gm():
    html = ""
    with open("msg.json") as mfr:
        msgs = json.load(mfr)
    counter = 0
    msgs.sort(key=lambda x: x["id"], reverse=True)

    for i in msgs:
        if i["content"] == "":
            counter += 1
        else:
            if counter > 0:
                html += f"""
                <div>
                    {counter} bumps
                </div>
                """
                counter = 0
            html += template(
                """
                <div>
                    <b><em>\"{{msg}}\"</em></b>
                </div>
                """,
                msg=i["content"],
            )
    if counter > 0:
        html += f"""
            <div>
                {counter} bumps
            </div>
            """
        counter = 0

    return html


if __name__ == "__main__":
    try:
        with open("msg.json", "r") as mf:
            json.load(mf)
    except:
        with open("msg.json", "w") as mf:
            json.dump([], mf)
    run(host="localhost", port=8080, debug=True)
