''' Schemas for Device.
Raw: The format of the resposne from the API endpoint
Parsed: The format used internally, a subset of the original fields
'''
from marshmallow import Schema, fields


#############
# Attribute #
#############

class AttributeRawSchema(Schema):
    last_read_at = fields.DateTime()
    name = fields.Str()
    state = fields.Str()


##########
# Device #
##########

class DeviceRawSchema(Schema):
    attributes = fields.List(fields.Nested(AttributeRawSchema()))
    battery_level = fields.Integer(allow_none=True)
    battery_powered = fields.Boolean()
    icon = fields.Field(allow_none=True)
    id = fields.Integer()
    inserted_at = fields.DateTime()
    name = fields.Str()
    online = fields.Boolean()
    pending_update = fields.Boolean()
    primary_lock = fields.Boolean()
    room = fields.Dict()
    show_on_dashboard = fields.Boolean()
    type = fields.Str()
    updated_at = fields.DateTime()
    valid_config = fields.Boolean()
    warning = fields.Boolean()


class DeviceParsedSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
