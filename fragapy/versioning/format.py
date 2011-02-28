def format_version(version_tuple):
    version = '%s.%s' % (version_tuple[0], version_tuple[1])
    if len(version_tuple) > 2:
        version = '%s.%s' % (version, version_tuple[2])
    return version
