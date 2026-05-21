"""Repositorio de almacenamiento para la gestión de Carritos e Ítems."""

from src.almacenamiento.base import BaseRepository


class CarritoRepository(BaseRepository):
    """Manejo relacional de las tablas 'carrito' e 'item_carrito' en Supabase."""

    def __init__(self) -> None:
        super().__init__()
        self._table_carrito = "carrito"
        self._table_items = "item_carrito"

    def obtener_carrito_con_items(self, usuario_id: int) -> dict | None:
        """Obtiene la cabecera del carrito y sus ítems anidados usando la relación SQL."""
        op = f"obtener_carrito_usuario_{usuario_id}"
        response = self._execute(
            op,
            lambda: self.client.table(self._table_carrito)
            .select("*, item_carrito(*)")
            .eq("usuario_id", usuario_id)
            .execute()
        )
        data = getattr(response, "data", [])
        return data[0] if data else None

    def crear_carrito(self, usuario_id: int) -> dict:
        """Inicializa un carrito vacío para un usuario específico."""
        op = f"crear_carrito_usuario_{usuario_id}"
        response = self._execute(
            op,
            lambda: self.client.table(self._table_carrito).insert({"usuario_id": usuario_id}).execute()
        )
        return self._require_data(response, op)[0]

    def agregar_o_actualizar_item(self, carrito_id: int, producto_id: int, cantidad: int, datos_prod: dict) -> dict:
        """Suma unidades de un artículo al detalle del carrito o crea el registro si no existe."""
        op = f"modificar_item_en_carrito_{carrito_id}"
        
        # 1. Comprobar si el producto ya está metido en ese carrito
        check_res = self._execute(
            op,
            lambda: self.client.table(self._table_items)
            .select("*")
            .eq("carrito_id", carrito_id)
            .eq("producto_id", producto_id)
            .execute()
        )
        existing_items = getattr(check_res, "data", [])
        
        if existing_items:
            # Si ya existe, sumamos la cantidad vieja con la nueva
            nueva_cantidad = existing_items[0]["cantidad"] + cantidad
            item_id = existing_items[0]["item_id"]
            
            response = self._execute(
                op,
                lambda: self.client.table(self._table_items)
                .update({"cantidad": nueva_cantidad})
                .eq("item_id", item_id)
                .execute()
            )
        else:
            # Si no existe, insertamos el renglón con los datos espejo exigidos por el SQL
            response = self._execute(
                op,
                lambda: self.client.table(self._table_items)
                .insert({
                    "carrito_id": carrito_id,
                    "producto_id": producto_id,
                    "nombre": datos_prod["nombre"],
                    "precio_unitario": datos_prod["precio"],
                    "cantidad": cantidad
                })
                .execute()
            )
        return self._require_data(response, op)[0]

    def eliminar_item_del_carrito(self, carrito_id: int, producto_id: int) -> bool:
        """Remueve por completo un producto del detalle del carrito."""
        op = f"eliminar_item_p_{producto_id}_de_carrito_{carrito_id}"
        response = self._execute(
            op,
            lambda: self.client.table(self._table_items)
            .delete()
            .eq("carrito_id", carrito_id)
            .eq("producto_id", producto_id)
            .execute()
        )
        data = getattr(response, "data", [])
        return len(data) > 0