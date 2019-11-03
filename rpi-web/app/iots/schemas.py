from flask_io import fields, Schema, post_dump
from .models import IoTs


class IoTSchema(Schema):
    id = fields.Integer(dump_only=True)
    hmt = fields.String(allow_none=True)
    tmp = fields.String(allow_none=True)
    ppm = fields.String(allow_none=True)
    lx = fields.String(allow_none=True)
    ld = fields.String(allow_none=True)
    time = fields.String(required=True)
    date = fields.String(required=True)
    timestamp = fields.String(required=True)
    device  = fields.String(required=False)

    @post_dump
    def make_object(self, data):
        return IoTs(**data)