''' Schemas for Hub.
Raw: The format of the resposne from the API endpoint
Parsed: The format used internally, a subset of the original fields
'''
from marshmallow import Schema, fields

class HubRawSchema(Schema):
    connection = fields.Str()
    id = fields.Integer()
    online = fields.Boolean()
    timezone = fields.Str(allow_none=True)
    unit_id = fields.Integer()
    wifi_supported = fields.Boolean()
    wifi_v2_supported = fields.Boolean()


class HubParsedSchema(Schema):
    id = fields.Integer()
