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
    """Мастер установки: только завершает установку (BX24.installFinish)."""
    return render_template("install.html")


@app.route("/app", methods=["GET", "POST"])
def app_page():
    """Основная страница приложения: регистрирует тип поля и само поле."""
    return render_template("app.html")


@app.route("/field", methods=["GET", "POST"])
def field():
    """HANDLER пользовательского типа поля — отображается внутри карточки CRM."""
    return render_template("field.html")


# Имя поля для метода crm.item.update — в camelCase, без префикса UF_CRM.
# UF_CRM_RICH_DESCRIPTION -> ufCrm_RICH_DESCRIPTION
ITEM_FIELD_CODE = "ufCrm_RICH_DESCRIPTION"


@app.route("/set-text", methods=["GET", "POST"])
def set_text():
    """Принимает deal_id и text (из GET-параметров или JSON) и пишет HTML в поле сделки.

    Использует crm.item.update (не deal.update) — он легче и не упирается
    в OPERATION_TIME_LIMIT, т.к. не тянет тяжёлый каскад обновления сделки.
    """
    if request.method == "GET":
        deal_id = request.args.get("deal_id")
        text = request.args.get("text")
    else:
        data = request.get_json(force=True, silent=True) or request.form
        deal_id = data.get("deal_id")
        text = data.get("text")

    if not deal_id or text is None:
        return jsonify({"error": "deal_id and text are required"}), 400

    value = text_to_html(text)

    resp = requests.post(
        INCOMING_WEBHOOK.rstrip("/") + "/crm.item.update",
        json={
            "entityTypeId": 2,  # 2 = сделка
            "id": deal_id,
            "fields": {ITEM_FIELD_CODE: value},
        },
        timeout=15,
    )
    return jsonify(resp.json())


@app.route("/health", methods=["GET", "POST"])
def health():
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
