from datetime import datetime, timezone

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.json.ensure_ascii = False

tasks: list[dict[str, object]] = []
next_task_id = 1


def api_response(status: str, message: str, data: object, http_status: int = 200):
    response = jsonify(
        {
            "status": status,
            "message": message,
            "data": data,
        }
    )
    response.status_code = http_status
    return response


@app.errorhandler(HTTPException)
def handle_http_exception(error: HTTPException):
    return api_response("error", error.description, None, error.code or 500)


@app.get("/api/health")
def health_check():
    return api_response(
        "success",
        "服務運作正常",
        {
            "status": "running",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


@app.get("/api/tasks")
def get_tasks():
    return api_response("success", "取得任務清單成功", tasks)


@app.post("/api/tasks")
def create_task():
    global next_task_id

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return api_response("error", "請提供合法的 JSON 物件", None, 400)

    title = payload.get("title")
    if not isinstance(title, str) or not title.strip():
        return api_response("error", "必填欄位 title 不可缺少或空白", None, 400)

    description = payload.get("description", "")
    if not isinstance(description, str):
        return api_response("error", "欄位 description 必須是字串", None, 400)

    task = {
        "id": next_task_id,
        "title": title.strip(),
        "description": description,
    }
    tasks.append(task)
    next_task_id += 1

    return api_response("success", "任務新增成功", task, 201)


@app.get("/api/tasks/<int:task_id>")
def get_task(task_id: int):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        return api_response("error", "找不到指定任務", None, 404)

    return api_response("success", "取得任務成功", task)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)