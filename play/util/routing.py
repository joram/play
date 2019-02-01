from django.http import HttpResponseNotAllowed


def method_dispatch(**table):
    def invalid_method(request, *args, **kwargs):
        return HttpResponseNotAllowed(table.keys())

    def route(request, *args, **kwargs):
        method = request.method
        if request.POST and "_method" in request.POST:
            method = request.POST["_method"]
        method = method.upper()
        handler = table.get(method, invalid_method)
        return handler(request, *args, **kwargs)

    return route
