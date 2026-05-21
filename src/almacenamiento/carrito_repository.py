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

    def agregar_o_actualizar_item(self, carrito_id: int, producto_id: int, cantidad: int) -> dict:
        """
        Inserta o incrementa un ítem en el carrito de compras.
        Busca autónomamente el nombre y el precio del catálogo para cumplir el NOT NULL del SQL.
        """
        cid = int(carrito_id)
        pid = int(producto_id)
        qty = int(cantidad)

        prod_res = (
            self.client.table("producto")
            .select("nombre, precio")
            .eq("producto_id", pid)
            .maybe_single()
            .execute()
        )

        if not prod_res or not prod_res.data:
            raise Exception(f"El producto con ID {pid} no existe en el catálogo.")

        nombre_producto = prod_res.data["nombre"]
        precio_producto = float(prod_res.data["precio"])

        existe = (
            self.client.table(self._table_items)
            .select("*")
            .eq("carrito_id", cid)
            .eq("producto_id", pid)
            .maybe_single()
            .execute()
        )

        if existe and existe.data:
            nueva_cantidad = existe.data["cantidad"] + qty
            result = (
                self.client.table(self._table_items)
                .update({"cantidad": nueva_cantidad})
                .eq("item_id", existe.data["item_id"]) 
                .execute()
            )
            return result.data[0]
        else:
            payload = {
                "carrito_id": cid,
                "producto_id": pid,
                "nombre": nombre_producto,
                "precio_unitario": precio_producto,
                "cantidad": qty
            }
            result = (
                self.client.table(self._table_items)
                .insert(payload)
                .execute()
            )
            return result.data[0]

    def eliminar_item_del_carrito(self, usuario_id: int, producto_id: int) -> bool:
            """
            Elimina el renglón de item_carrito cruzando primero el ID del usuario 
            para encontrar su cabecera real.
            """
            try:
                uid = int(usuario_id)
                pid = int(producto_id)

                carrito_res = (
                    self.client.table("carrito")
                    .select("carrito_id")
                    .eq("usuario_id", uid)
                    .maybe_single()
                    .execute()
                )

                if not carrito_res or not carrito_res.data:
                    return False 

                cid = carrito_res.data["carrito_id"]

                delete_res = (
                    self.client.table("item_carrito")
                    .delete()
                    .eq("carrito_id", cid)
                    .eq("producto_id", pid)
                    .execute()
                )

                return len(delete_res.data) > 0

            except Exception as e:
                print(f"[REPOS_ERROR] Fallo al remover ítem: {str(e)}")
                return False