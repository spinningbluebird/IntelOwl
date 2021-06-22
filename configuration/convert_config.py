import json

EXTRA_KEYS = [
    "run_hash",
    "run_hash_type",
    "supported_filetypes",
    "not_supported_filetypes",
    "observable_supported",
]


def main():
    file_path = "analyzer_config.json"
    with open(file_path, "r") as f:
        analyzer_configs = json.load(f)

    new_config = {}
    for name, config in analyzer_configs.items():
        # Storing general info
        tmp_config = {
            "type": config["type"],
            "python_module": config["python_module"],
            "description": config.get("description", ""),
            "disabled": config.get("disabled", False),
            "requires_configuration": config.get("requires_configuration", False),
            "external_service": config.get("external_service", False),
            "leaks_info": config.get("leaks_info", False),
        }

        # Storing type-specific info
        for key in EXTRA_KEYS:
            if key in config:
                tmp_config[key] = config[key]

        # Storing general config info
        tmp_config["config"] = {
            "soft_time_limit": config.get("soft_time_limit", 300),
            "queue": config.get("queue", "default"),
        }

        # Storing analyzer-specific config info
        tmp_config["secrets"] = {}
        if "additional_config_params" in config.keys():
            for s_name, s_value in config["additional_config_params"].items():
                tmp_config["secrets"][s_name] = {
                    "value": s_value,
                    "type": "",
                    "required": True,
                    "default": None,
                    "description": "",
                }

        new_config[name] = tmp_config

    with open("new_analyzer_config.json", "w") as f:
        json.dump(new_config, f, indent=4)


if __name__ == "__main__":
    main()