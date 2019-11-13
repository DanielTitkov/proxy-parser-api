from typing import Dict, Tuple


def validate_args(args_spec: Dict, parsed_args: Dict) -> Tuple[bool, str]:
    for arg_name, arg_value in parsed_args.items():
        if arg_name not in args_spec.keys():  # this is impossible in the app but seems logical to have
            return False, "Unknown agrument: '{}'. Avaliable arguments are: {}".format(
                arg_name, ", ".join(args_spec.keys())
            )
        elif any([
            all([
                args_spec[arg_name]["type"] == "nominal",
                arg_value not in args_spec[arg_name]["values"]
            ]),
            all([
                args_spec[arg_name]["type"] == "interval",
                any([
                    arg_value < args_spec[arg_name]["values"][0],
                    arg_value > args_spec[arg_name]["values"][1],
                ])
            ])
        ]):
            return False, "Wrong value '{}' for argument '{}'. Suppported values are: {}".format(
                arg_value, arg_name, args_spec[arg_name]["values"]
            )
    return True, ""


def parse_args(args_spec: Dict, args: Dict) -> Dict:
    parsed_args = {}
    for k, v in args_spec.items():
        arg = args.get(k, v["default"])
        parsed_args[k] = int(arg) if v["type"] == "interval" else arg
    return parsed_args
