import os


def get_env(key, default=None, allow_default=True):
    if key not in os.environ:
        if not allow_default:
            raise NotImplementedError("Environment variable is unset: '%s'" % key)
        print("using default value for %s=%s" % (key, default))
    return os.environ.get(key, default)
