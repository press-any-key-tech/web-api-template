# Pynamodb

Pynamodb do not allow to change dynamically the region assigned to the model, that is, it is on the definition of the model.

If you need to implement models that work on differente regions you need to specify th region on the model itself.

e.g.

You have this base model:

'''python
class BaseModel(Model):
    """
    A DynamoDB Base Model
    """

    class Meta:
        table_name = None
        region = settings.DYNAMODB_REGION
        if settings.DYNAMODB_ENDPOINT is not None:
            host = settings.DYNAMODB_ENDPOINT
'''

If you need to specify a concrete region for the model, this should be done in the meta:

'''python
class MyModel(BaseModel):

    class Meta(BaseModel.Meta):
        table_name = "mytable"
        region = "us-east-1"

    id = UnicodeAttribute(hash_key=True, default=lambda: str(Ksuid()), null=False)

    name = UnicodeAttribute()

'''

Of course, you can read the region from a settings file, but it's your responsibility to define that file.


