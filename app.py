import html
import os

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Входящий вебхук портала, куда пишем итоговое значение поля.
# Пример: https://autozakaz.bitrix24.ru/rest/1/xxxxxxxxxxxxxxxx/
INCOMING_WEBHOOK = os.environ["INCOMING_WEBHOOK"]

# Код поля сделки, в которое пишем текст, например UF_CRM_1789999999999
FIELD_CODE = os.environ["FIELD_CODE"]


def text_to_html(text: str) -> str:
    """Обычный текст -> безопасный HTML с абзацами и переносами строк."""
    escaped = html.escape(text)
    paragraphs = escaped.split("\n\n")
    return "".join(
        "<p>{}</p>".format(p.replace("\n", "<br>"))
        for p in paragraphs
        if p.strip()
    )


@app.route("/install", methods=["GET", "POST"])
def install():
    """Страница мастера установки локального приложения (открывается один раз)."""
    return render_template("install.html")


@app.route("/field", methods=["GET", "POST"])
def field():
    """HANDLER пользовательского типа поля — отображается внутри карточки CRM."""
    return render_template("field.html")


@app.route("/set-text", methods=["POST"])
def set_text():
    """Принимает { deal_id, text } и пишет отформатированный HTML в поле сделки."""
    data = request.get_json(force=True, silent=True) or request.form
    deal_id = data.get("deal_id")
    text = data.get("text")

    if not deal_id or text is None:
        return jsonify({"error": "deal_id and text are required"}), 400

    value = text_to_html(text)

    resp = requests.post(
        INCOMING_WEBHOOK.rstrip("/") + "/crm.deal.update",
        json={"id": deal_id, "fields": {FIELD_CODE: value}},
        timeout=10,
    )
    return jsonify(resp.json())


@app.route("/health", methods=["GET", "POST"])
def health():
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
