from app.common.application.controllers.error_responses.error_response import ErrorResponse


class UnsupportedDepositingApplicationErrorResponse(ErrorResponse):
    http_code = 400
    message = "Unsupported depositing application {depositing_application}"

    def __init__(self, depositing_application: str):
        self.message = self.message.format(depositing_application=depositing_application)
