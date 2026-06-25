import os
import io
import base64
import traceback
from flask import Flask, request, send_file, jsonify

from card_generator_html import (
    generate_profile_card,
    generate_leaderboard_card,
    generate_duo_leaderboard_card,
    generate_match_result_card,
)

app = Flask(__name__)


def _decode_avatar_b64(b64: str) -> bytes | None:
    """Декодирует base64-строку в bytes."""
    if not b64:
        return None
    try:
        return base64.b64decode(b64)
    except Exception:
        return None


def _decode_avatars(avatars) -> dict:
    """Декодирует {uid_str: base64} → {int_uid: bytes}."""
    if not avatars:
        return {}
    result = {}
    for uid_str, b64 in avatars.items():
        decoded = _decode_avatar_b64(b64)
        if decoded:
            try:
                result[int(uid_str)] = decoded
            except (ValueError, TypeError):
                pass
    return result


def _error(msg: str, code: int = 400):
    return jsonify({"error": msg}), code


@app.route("/health")
def health():
    return "ok"


@app.route("/profile", methods=["POST"])
def profile():
    try:
        data = dict(request.get_json(force=True) or {})
        avatar_b64 = data.pop("avatar_bytes", None)
        data["avatar_bytes"] = _decode_avatar_b64(avatar_b64)
        buf = generate_profile_card(**data)
        buf.seek(0)
        return send_file(buf, mimetype="image/png")
    except TypeError as e:
        return _error(f"Bad params: {e}")
    except Exception as e:
        traceback.print_exc()
        return _error(f"Internal error: {e}", 500)


@app.route("/leaderboard", methods=["POST"])
def leaderboard():
    try:
        data = request.get_json(force=True) or {}
        players = data.get("players", [])
        title   = data.get("title", "ЛУЧШИЕ ИГРОКИ")
        avatars = _decode_avatars(data.get("avatars"))
        buf = generate_leaderboard_card(players=players, title=title, avatars=avatars or None)
        buf.seek(0)
        return send_file(buf, mimetype="image/png")
    except Exception as e:
        traceback.print_exc()
        return _error(f"Internal error: {e}", 500)


@app.route("/duo_leaderboard", methods=["POST"])
def duo_leaderboard():
    try:
        data = request.get_json(force=True) or {}
        players = data.get("players", [])
        title   = data.get("title", "2v2 ТОП")
        avatars = _decode_avatars(data.get("avatars"))
        buf = generate_duo_leaderboard_card(players=players, title=title, avatars=avatars or None)
        buf.seek(0)
        return send_file(buf, mimetype="image/png")
    except Exception as e:
        traceback.print_exc()
        return _error(f"Internal error: {e}", 500)


@app.route("/match_result", methods=["POST"])
def match_result():
    try:
        data = dict(request.get_json(force=True) or {})
        avatars = _decode_avatars(data.pop("avatars", None))
        buf = generate_match_result_card(**data, avatars=avatars or None)
        buf.seek(0)
        return send_file(buf, mimetype="image/png")
    except TypeError as e:
        return _error(f"Bad params: {e}")
    except Exception as e:
        traceback.print_exc()
        return _error(f"Internal error: {e}", 500)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, threaded=False)
