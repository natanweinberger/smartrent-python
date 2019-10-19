# Schemas

We use schemas to represent each model that the Smartrent API returns in its responses. Each model is represented by two schemas - one raw, one parsed.

- raw: An exact representation of the API response, as it is sent by Smartrent
- parsed: A transformed version of the raw response, for use within the wrapper

For example, a sample response from the `/hubs` endpoint looks like this:
```json
[
    {"id": 123,
     "online": true}
]
```

So, our raw schema looks like:
```python
from marshmallow import Schema, fields

class HubRawSchema(Schema):
    id = fields.Integer()
    online = fields.Boolean()
```

Within the wrapper, we never care about the field `online`. It would be easier to just drop it from the dictionary. So, we create another schema with the transformations we want to apply, which include dropping fields entirely:

```python
from marshmallow import Schema, fields

class HubParsedSchema(Schema):
    id = fields.Integer()
```

Executing the transformation is simple:
```python
response_text = client.api.get('hubs')

raw_dicts = HubRawSchema().load(response_text, many=True)
parsed_dicts = HubParsedSchema().dump(raw_dicts, many=True)

print(parsed_dicts)

# [{"id": 123}]
