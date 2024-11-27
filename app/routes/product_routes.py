from datetime import datetime

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app import db
from app.models.product import InventoryEntry, Product
from app.schemas.product_schema import InventoryEntrySchema, ProductSchema

blp = Blueprint(
    'products', 
    __name__, 
    description='Operaciones sobre productos e inventario'
)

@blp.route('/products')
class ProductResource(MethodView):
    @blp.response(200, ProductSchema(many=True))
    def get(self):
        """Listar todos los productos"""
        return Product.query.all()

    @blp.arguments(ProductSchema)
    @blp.response(201, ProductSchema)
    def post(self, product_data):
        """Crear un nuevo producto"""
        try:
            product = Product(
                name=product_data['name'],
                description=product_data.get('description', '')
            )
            db.session.add(product)
            db.session.commit()
            return product
        except Exception as e:
            db.session.rollback()
            abort(400, message=str(e))

@blp.route('/inventory/entry')
class InventoryEntryResource(MethodView):
    @blp.arguments(InventoryEntrySchema)
    @blp.response(201, InventoryEntrySchema)
    def post(self, entry_data):
        """Registrar una entrada de inventario"""
        try:
            entry = InventoryEntry(
                product_id=entry_data['product_id'],
                quantity=entry_data['quantity'],
                expiration_date=entry_data['expiration_date'],
                entry_type='in'
            )
            
            if entry.quantity <= 0:
                abort(400, message='La cantidad debe ser positiva')
                
            db.session.add(entry)
            db.session.commit()
            return entry
        except Exception as e:
            db.session.rollback()
            abort(400, message=str(e))

@blp.route('/inventory/exit')
class InventoryExitResource(MethodView):
    @blp.arguments(InventoryEntrySchema)
    @blp.response(201, InventoryEntrySchema)
    def post(self, exit_data):
        """Registrar una salida de inventario"""
        try:
            available_stock = db.session.query(
                db.func.sum(InventoryEntry.quantity)
            ).filter(
                InventoryEntry.product_id == exit_data['product_id'],
                InventoryEntry.expiration_date >= datetime.utcnow()
            ).scalar() or 0
            
            if available_stock < exit_data['quantity']:
                abort(400, message='Stock insuficiente')
                
            exit_entry = InventoryEntry(
                product_id=exit_data['product_id'],
                quantity=-exit_data['quantity'],
                expiration_date=exit_data['expiration_date'],
                entry_type='out'
            )
            
            db.session.add(exit_entry)
            db.session.commit()
            return exit_entry
        except Exception as e:
            db.session.rollback()
            abort(400, message=str(e))

@blp.route('/inventory/status')
class InventoryStatusResource(MethodView):
    @blp.response(200, InventoryEntrySchema(many=True))
    def get(self):
        """Obtener el estado actual del inventario"""
        return InventoryEntry.query.all()

@blp.route('/products/<int:product_id>/inventory')
class ProductInventoryResource(MethodView):
    @blp.response(200, InventoryEntrySchema(many=True))
    def get(self, product_id):
        """Obtener el inventario de un producto específico"""
        return InventoryEntry.query.filter_by(product_id=product_id).all()