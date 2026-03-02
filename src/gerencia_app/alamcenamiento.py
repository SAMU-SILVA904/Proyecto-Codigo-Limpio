import json
from pathlib import Path
from typing import List, Type, TypeVar, Any
from dataclasses import asdict
from .models import Usuario, Producto, Rol, Carrito, ItemCarrito

variable_universal = TypeVar("Variable_universal")

class JSONStorage:
    def __init__(self, base_a_guardar: Path, modelo_clase: Type[variable_universal]):
        self.base_a_guardar = base_a_guardar
        self.modelo_clase = modelo_clase
    
    def load(self) -> List[variable_universal]:
        if not self.base_a_guardar.exists():
            return []
        
        with open(self.base_a_guardar, "r", encoding="utf-8") as datos_en_la_base_de_datos:
            lista_diccionarios = json.load(datos_en_la_base_de_datos) 
        
        objetos_finales = []
        for mi_diccionario_actual in lista_diccionarios:
            if self.modelo_clase == Usuario:
                mi_diccionario_actual["rol"] = Rol(mi_diccionario_actual["rol"])
                
                lista_del_dict_de_carrito = mi_diccionario_actual.get("carrito", [])
                mi_diccionarios_item = [ItemCarrito(**cada_dict) for cada_dict in lista_del_dict_de_carrito] # "**cada_dict" hace que la llave se iguale con el contenido llave = contenido
                mi_diccionario_actual["carrito"] = Carrito(items=mi_diccionarios_item)
                
                objetos_finales.append(Usuario(**mi_dicciop))
            else:
                objetos_finales.append(self.modelo_clase(**mi_dicciop))
                
        return objetos_finales
    
    def save(self, items: List[variable_universal]) -> None:
        self.base_a_guardar.parent.mkdir(parents=True, exist_ok=True)
        
        datos_preparados = []
        for objetos in items:
            # asdict convierte TODA la jerarquía de objetos a diccionarios
            dicccionario_objetos = asdict(objetos)
            
            if "rol" in dicccionario_objetos:
                dicccionario_objetos["rol"] = objetos.rol.value
            
            if "carrito" in dicccionario_objetos:
                dicccionario_objetos["carrito"] = dicccionario_objetos["carrito"]["items"]
                
            datos_preparados.append(dicccionario_objetos)
        
        with open(self.base_a_guardar, "w", encoding="utf-8") as f:
            json.dump(datos_preparados, f, indent=4, ensure_ascii=False)
            
