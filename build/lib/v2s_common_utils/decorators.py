from functools import wraps

def replace_placeholder_with_id(model, attribute, placeholder_key):
    """
    A decorator to replace a placeholder value in request.data with the corresponding model's ID.

    Args:
        model (class): The Django model class to query.
        attribute (str): The attribute name in the model to match.
        placeholder_key (str): The key in request.data where the placeholder value is located.

    Returns:
        function: A decorator function.

    Example:
        @replace_placeholder_with_id(Endpoint, 'name', 'endpoint_name')
        def your_view(request):
            # Your view logic here
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            if request.data.get(placeholder_key) is not None:
                # Get the placeholder value from request.data
                placeholder_value = request.data[placeholder_key]
                print(placeholder_value)
                print(attribute)
                obj = model.objects.filter(**{attribute: placeholder_value}).first()
                print(obj)
                if obj:
                    # Replace the placeholder value with the object's ID
                    request.data[placeholder_key] = obj.id
            return view_func(self, request, *args, **kwargs)
        return _wrapped_view
    return decorator
