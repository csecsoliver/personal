from bottle import route, run, static_file, get, post, request, template
import json

clicks = 0
unsaved = 0


@route("/")
def index():
    return static_file("index.html", root="./static/")


@get("/clicker")
def gclp():
    return static_file("clicker.html", root="./static/")


@post("/click")
def pcl():
    global clicks
    global unsaved
    clicks += 1
    unsaved += 1
    if unsaved > 1000:
        with open("cl.json", "w") as clf:
            json.dump({"clicks": clicks}, clf)
        unsaved = 0
    return str(clicks)


@route("/saveclicks")
def saveclicks():
    with open("cl.json", "w") as clf:
        json.dump({"clicks": clicks}, clf)


@post("/clicks")
def gcls():
    print("all in memory:", clicks)
    print("unsaved:", unsaved)
    return str(clicks)


@get("/<fp:path>")
def f(fp):
    return static_file(fp, root="./static/")


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
    try:
        with open("cl.json", "r") as clf:
            cldata = json.load(clf)
            clicks = int(cldata["clicks"])
    except:
        with open("cl.json", "w") as clf:
            json.dump({"clicks": 0}, clf)
            clicks = 0

    run(host="0.0.0.0", port=8080, debug=True)
