from marshmallow import Schema, fields, validate


class ProductSchema(Schema):
    """Esquema para productos"""
    id = fields.Int(dump_only=True, description="ID único del producto")
    name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=100),
        description="Nombre del producto"
    )
    description = fields.Str(
        validate=validate.Length(max=200),
        description="Descripción del producto"
    )
    created_at = fields.DateTime(dump_only=True, description="Fecha de creación")
    updated_at = fields.DateTime(dump_only=True, description="Fecha de última actualización")

class InventoryEntrySchema(Schema):
    """Esquema para entradas y salidas de inventario"""
    id = fields.Int(dump_only=True, description="ID único de la entrada")
    product_id = fields.Int(
        required=True,
        description="ID del producto relacionado"
    )
    quantity = fields.Int(
        required=True,
        validate=validate.Range(min=1),
        description="Cantidad (positiva para entradas, negativa para salidas)"
    )
    expiration_date = fields.DateTime(
        required=True,
        description="Fecha de vencimiento del producto"
    )
    entry_type = fields.Str(
        validate=validate.OneOf(['in', 'out']),
        description="Tipo de movimiento (in=entrada, out=salida)"
    )
    status = fields.Str(
        dump_only=True,
        description="Estado del producto (vigente, por_vencer, vencido)"
    )
    created_at = fields.DateTime(
        dump_only=True,
        description="Fecha de registro del movimiento"
    )
    product = fields.Nested(
        ProductSchema,
        dump_only=True,
        description="Información del producto relacionado"
    )