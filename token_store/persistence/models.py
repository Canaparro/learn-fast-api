from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model


class TokenModel(Model):
    id = fields.UUIDField(pk=True)
    client_id = fields.CharField(max_length=255)
    instance_id = fields.CharField(max_length=255)
    account_id = fields.CharField(max_length=255)
    token = fields.TextField()
    expire_at = fields.IntField()
    permissions: fields.ManyToManyRelation["PermissionModel"]


class PermissionModel(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=255)
    tokens: fields.ManyToManyRelation[TokenModel] = fields.ManyToManyField("models.TokenModel", related_name="permissions", through="token_permission")
