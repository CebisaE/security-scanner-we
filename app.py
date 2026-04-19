from flask import Flask, render_template, request, make_response
import requests
import socket

scan_history = []

common_ports = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP"
}

app = Flask(__name__)


def scan_website(url):
    result = ""

    # HTTPS CHECK
    if url.startswith("https"):
        result += "<div class='card green'>🔐 HTTPS: Enabled</div>"
    else:
        result += "<div class='card red'>🔐 HTTPS: Not Enabled</div>"

    # BASIC REQUEST TEST
    try:
        response = requests.get(url)
        result += f"<div class='card blue'>📡 Status Code: {response.status_code}</div>"

        headers = response.headers
        result += "<div class='card'>🔍 Security Headers</div>"

        for h in ["Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options"]:
            if h in headers:
                result += f"<div class='card green'>✔ {h}</div>"
            else:
                result += f"<div class='card red'>✖ {h} Missing</div>"

    except:
        result += "<div class='card red'>Website unreachable</div>"

    # PORT SCANNING
    host = url.replace("https://", "").replace("http://", "").split("/")[0]
    result += scan_ports(host)

    return result

def scan_ports(host):
    result = ""

    for port in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        status = sock.connect_ex((host, port))

        if status == 0:
            result += f"<div class='card red'>🚪 Port {port} OPEN ({common_ports[port]})</div>"
        else:
            result += f"<div class='card'>🔒 Port {port} closed</div>"

        sock.close()

    return result


@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":
        url = request.form["url"]
        result = scan_website(url)

    response = make_response(render_template("index.html", result=result))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response

@app.route("/scan", methods=["POST"])
def scan():
    url = request.form["url"]
    result = scan_website(url)
    scan_history.append(url)
    return result

@app.route("/history")
def history():
    return {"history": scan_history}


if __name__ == "__main__":
    app.run(debug=True)