from common import error_messages, generate_params_error_message, write_log
from util import print_error

class ErrorUtils():
    @staticmethod
    def api_error(error_code, inner_message, **parameters):
        write_log(inner_message)

        error_mesage = error_messages.get(error_code, False)
        print error_code
        print error_mesage
        if not error_mesage:
            return inner_message
        else:
            error_mesage = str(error_mesage).format(**parameters)

        return error_mesage

    @staticmethod
    def validation_error(error_code, inner_message, parameter):
        write_log(inner_message)

        message = "Parameter {!r} ".format(parameter)
        reason = error_messages.get(
            error_code, error_messages['ValidationError'])

        message += reason.format(parameter)

        return message

    @staticmethod
    def mandatory_params_missing(parameters, inner_message):
        write_log(inner_message)

        error_message = generate_params_error_message(parameters, error_messages['MandatoryParamsMissing'])
        return error_message

    @staticmethod
    def internal_error(inner_message):
        write_log(inner_message)

        error_message = "{0}, {1}".format(error_messages['InternalError'], inner_message)
        return error_message

    @staticmethod
    def bundle_error(inner_message):
        write_log(inner_message)

        return error_messages['BundleError']

    @staticmethod
    def check_mandatory_params_is_empty(parameters, data_dict):
        keys = []
        for v in parameters:
            if len(str(data_dict.get(v, "")).strip()) == 0:
                keys.append(v)

        if bool(keys):
            error_message = generate_params_error_message(keys, error_messages['MandatoryParamsEmpty'])

            return {"error": True, "message": error_message}
        
        return {"error": False}







