from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model

from rest_framework.serializers import ValidationError


class BaseService:
    # @staticmethod
    # def get_object(model, **kwargs):
    #     """
    #     Helper method for querying the database and returning a model object
    #     based on provided query parameters.

    #     Args:
    #         model: The model class to use for the query.
    #         **kwargs: The query parameters to use for the query.

    #     Returns:
    #         A model object from the database if one exists with the specified query parameters, None otherwise.
    #     """
    #     try:
    #         return model.objects.get(**kwargs)
    #     except model.DoesNotExist:
    #         return None

    # @staticmethod
    # def get_object_by_id(model, **kwargs):
    #     is_deleted = kwargs.get('is_deleted', False)
    #     pk = kwargs.get('pk', None)
    #     kwargs["is_deleted"] = is_deleted
    #     if 'pk' in kwargs:
    #         kwargs["pk"] = pk
    #     if is_deleted or is_deleted is None:
    #         kwargs.pop('is_deleted')
    #     return BaseService.get_object(model, **kwargs)

    @staticmethod
    def get_object(model, **kwargs):
        """
        Get an object from the database based on the provided model and filter criteria.

        Args:
            model (django.db.models.Model): The Django model to query.
            **kwargs: Keyword arguments representing filter criteria.

        Returns:
            model instance or None: The retrieved object or None if not found.
        """
        try:
            return model.objects.get(**kwargs)
        except model.DoesNotExist:
            return None

    @staticmethod
    def get_object_by_id(model, pk=None, is_deleted=False, **kwargs):
        """
        Get an object by its primary key with an optional filter for 'is_deleted'.

        Args:
            model (django.db.models.Model): The Django model to query.
            pk (int): The primary key of the object.
            is_deleted (bool): Flag to filter deleted objects.
            **kwargs: Additional filter criteria.

        Returns:
            model instance or None: The retrieved object or None if not found.
        """
        if is_deleted is not None:
            kwargs["is_deleted"] = is_deleted
        if pk is not None:
            kwargs["pk"] = pk

        return BaseService.get_object(model, **kwargs)

    @staticmethod
    def get_all(model: Model, ordering=None, **kwargs):
        """
        Get all objects of a given model from the database.

        Args:
            model: The model class to use for the query.
            ordering: The field to use for sorting the results.
            **kwargs: The query parameters to use for the query.

        Returns:
            A QuerySet of model objects from the database that match the specified query parameters.
        """
        is_deleted = kwargs.get('is_deleted', False)
        kwargs["is_deleted"] = is_deleted
        if is_deleted or is_deleted is None:
            kwargs.pop('is_deleted')
        queryset = model.objects.filter(**kwargs)
        if ordering is not None:
            queryset = queryset.order_by(ordering)
        return queryset

    @staticmethod
    def list_all(model_class, serializer_class, ordering=None, **kwargs):
        """
        List all objects of a given model from the database, serialized as JSON.

        Args:
            model_class: The model class to use for the query.
            serializer_class: The serializer class to use for converting model objects to JSON.
            ordering: The field to use for sorting the results.
            **kwargs: The query parameters to use for the query.

        Returns:
            A list of serialized JSON objects representing model objects from the database that match the specified
            query parameters.
        """
        queryset = BaseService.get_all(
            model_class, ordering=ordering, **kwargs)
        serializer = serializer_class(queryset, many=True)
        return serializer.data

    @staticmethod
    def create(serializer_class, model_class, data):
        """
        Create a new object of a given model in the database, using data provided in JSON format.

        Args:
            serializer_class: The serializer class to use for converting JSON data to a model object.
            model_class: The model class to use for creating the new object in the database.
            data: The JSON data to use for creating the new object.

        Returns:
            A dictionary representing the newly created object in serialized JSON format.
        """
        serializer = serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            raise ValidationError(serializer.errors)

    @staticmethod
    def list_details(object, serializer_class, **kwargs):
        """
        Serialize a single object of a given model to JSON.

        Args:
            object: The object to serialize.
            serializer_class: The serializer class to use for converting the object to JSON.
            **kwargs: Additional arguments to pass to the serializer.

        Returns:
            A dictionary representing the object in serialized JSON format.
        """
        serializer = serializer_class(object)
        return serializer.data

    @staticmethod
    def update(object, serializer_class, data, partial=False):
        """
        Helper method for updating an existing database object with new data.

        Args:
            object: The object to update.
            serializer_class: The serializer class to use to serialize the updated object.
            data: The new data to use to update the object.
            partial: Whether to allow partial updates or not.

        Returns:
            The serialized data of the updated object.
        Raises:
            serializers.ValidationError: If the serializer is invalid.
        """
        serializer = serializer_class(object, data=data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            raise ValidationError(serializer.errors)

    @staticmethod
    def delete(object):
        """
        Helper method for soft-deleting a database object.

        Args:
            object: The object to delete.

        Returns:
            True if the object was deleted successfully.
        """
        object.is_deleted = True
        object.save()
        return True

    @staticmethod
    def deactivate_object(obj):
        """
        Deactivates a database object by setting its 'is_active' attribute to False.

        Args:
            obj: The object to deactivate.

        Returns:
            True if the object was deactivated successfully.
        """
        obj.is_active = False
        obj.save()
        return True

    @staticmethod
    def delete_permanently(object):
        """
        Helper method for soft-deleting a database object.

        Args:
            object: The object to delete.

        Returns:
            True if the object was deleted successfully.
        """
        object.delete()
        return True

    @staticmethod
    def validate_data(serializer_class, data, partial=False):
        """
        Validate the provided data using the specified serializer class.

        Args:
            serializer_class (Serializer): The serializer class to use for data validation.
            data (dict): The data to validate.

        Raises:
            ValidationError: If the data is not valid.

        Returns:
            bool: True if the data is valid.
        """
        serializer = serializer_class(data=data, partial=partial)
        if serializer.is_valid():
            return serializer.validated_data
        else:
            raise ValidationError(serializer.errors)


class AbstractBaseService:

    @staticmethod
    def create(serializer_class, model_class, data):
        """
        Create a new object of a given model in the database, using data provided in JSON format.

        Args:
            serializer_class: The serializer class to use for converting JSON data to a model object.
            model_class: The model class to use for creating the new object in the database.
            data: The JSON data to use for creating the new object.

        Returns:
            A dictionary representing the newly created object in serialized JSON format.
        """
        serializer = serializer_class(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            return instance
        else:
            raise ValidationError(serializer.errors)

    @staticmethod
    def update(object, serializer_class, data, partial=False):
        """
        Helper method for updating an existing database object with new data.

        Args:
            object: The object to update.
            serializer_class: The serializer class to use to serialize the updated object.
            data: The new data to use to update the object.
            partial: Whether to allow partial updates or not.

        Returns:
            The serialized data of the updated object.
        Raises:
            serializers.ValidationError: If the serializer is invalid.
        """
        serializer = serializer_class(object, data=data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            raise ValidationError(serializer.errors)

    @staticmethod
    def delete(object):
        """
        Helper method for soft-deleting a database object.

        Args:
            object: The object to delete.

        Returns:
            True if the object was deleted successfully.
        """
        object.is_deleted = True
        object.save()
        return True
