from app.common.application.controllers.error_responses.error_response import ErrorResponse


class UnsupportedDepositingApplicationErrorResponse(ErrorResponse):
    http_code = 400
    status_code = "UNSUPPORTED_DEPOSITING_APPLICATION"
    message = "Unsupported depositing application {depositing_application}"

    def __init__(self, package_id: str, depositing_application: str) -> None:
        self.package_id = package_id
        self.message = self.message.format(depositing_application=depositing_application)
