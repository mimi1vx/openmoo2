import copy

def parse_cli_args(argv, default_options = {}):
    argc = len(argv)
    options = copy.copy(default_options)
    params = []
    i = 1
    while i < argc:
        if argv[i][:1] == "-":
            options[argv[i]] = argv[i+1]
            i += 1
        else:
            params.append(argv[i])
        i += 1
    return (options, params)
