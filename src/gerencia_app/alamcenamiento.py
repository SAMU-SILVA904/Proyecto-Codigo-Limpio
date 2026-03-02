import json
from pathlib import Path
from typing import List, Type, TypeVar
from dataclasses import asdict
from .models import Usuario, Rol, Carrito, ItemCarrito

variable_universal = TypeVar("Variable_universal")
"""
Esto es un placeholder para indicar que puede ser cualquier tipo de dato. 
Se usa para indicar que el JSONStorage puede manejar cualquier modelo de datos (Usuario, Producto, etc) 
todo esto sin necesidad de crear una clase de almacenamiento específica para cada uno.

Referencia: vscode
"""

class JSONStorage:
    """
    Clase encargada de manejar el almacenamiento en formato JSON para cualquier modelo de datos.
    """
    
    def __init__(self, base_a_guardar: Path, modelo_clase: Type[variable_universal]):
        self.base_a_guardar = base_a_guardar
        self.modelo_clase = modelo_clase
    
    def load(self) -> List[variable_universal]:
        """
        Carga los datos desde el archivo JSON y convierte cada diccionario a una instancia del modelo_clase
        Devuelve la lista de objetos.
        """
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
                
                objetos_finales.append(Usuario(**mi_diccionario_actual))
            else:
                objetos_finales.append(self.modelo_clase(**mi_diccionario_actual))
                
        return objetos_finales
    
    def save(self, items: List[variable_universal]) -> None:
        """
        Toma una lista de objetos, los convierte a diccionarios y los guarda en el archivo JSON.
        """
        
        self.base_a_guardar.parent.mkdir(parents=True, exist_ok=True) # Asegura que la carpeta exista antes de guardar el archivo
        
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
            
