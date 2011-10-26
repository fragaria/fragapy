from .format import format_version
from .utils import get_version

def version(request):
    return {'VERSION': format_version(get_version())}
