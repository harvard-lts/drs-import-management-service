from typing import Tuple

from flask import jsonify, Response

from app.common.application.response_status import ResponseStatus


def render_bad_request_problem(error) -> Tuple[Response, int]:
    response = {
        "status": ResponseStatus.failure.value,
        "status_code": None,
        "message": error.detail
    }

    return jsonify(response), error.status
