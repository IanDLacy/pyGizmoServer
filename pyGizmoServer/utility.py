import copy, json


class Utility:
    @classmethod
    def parse_path_against_schema_and_model(
        cls,
        model: dict,
        schema: dict,
        path: str,
        read_write: str = "r",
        toLeaves: bool = False,
    ) -> dict:
        """
        navigate the schema following the request's path. The destination
        should be the name of a function and associated parameters that this 
        method will call
        """
        err = None
        if path is None:
            return None
        result = {}
        index = None
        # print('model ' + str(model))

        schema_location = copy.deepcopy(schema)
        model_location = copy.deepcopy(model)
        paths = (
            path.replace("[", ".")
            .replace("/", ".")
            .replace("]", "")
            .strip("\n\r\t")
            .split(".")
        )
        n_non_indexed_locations = len(paths)
        # print(model_location)
        while "" in paths:
            paths.remove("")
        for i, p in enumerate(paths):
            """ 
            check if the request utilizes array indexing 
            and if so, store the index to pass to the controller
            """
            try:
                if p.isnumeric():
                    n_non_indexed_locations = i
                    p = int(p)
                    index = p
                else:
                    schema_location = schema_location[p]
                model_location = model_location[p]
            except Exception as e:
                epath = "/" + "/".join(paths[:i])
                if not "FAVICON" in epath:
                    err = f"PATH ERROR: {epath}/{p}"
                    break
                else:
                    continue
        result["error"] = err
        if err is not None:
            result["path_array"] = None
            result["path_string"] = None
            result["path_up_to_array_index"] = None
            result["routine"] = None
            result["model_data"] = None
            result["args"] = None
        else:
            result["path_array"] = paths if err is None else None
            result["path_string"] = "/" + "/".join(paths) if err is None else None
            result["path_up_to_array_index"] = (
                "/" + "/".join(paths[:n_non_indexed_locations]) if err is None else None
            )
            result["routine"] = schema_location.get(read_write) if err is None else None
            result["model_data"] = model_location if err is None else None
            args = schema_location.get("args")
            if index is not None and args is not None:
                args.append(index)
            result["args"] = args if err is None else None
        return result

    @classmethod
    def initialize_model_from_schema(cls, d):
        if "$count" in d:
            return [
                {
                    k: cls.initialize_model_from_schema(v)
                    for k, v in d.items()
                    if k != "$count"
                }
                for i in range(d["$count"])
            ]
        if "$type" in d:
            return None
        return {k: cls.initialize_model_from_schema(v) for k, v in d.items()}
