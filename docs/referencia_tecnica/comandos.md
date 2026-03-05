# Comandos del proyecto

## 1. Crear Usuario
!!! Prerequisito
    El usuario que intente realizar este comando debe tener como Rol "gerente".

Para crear un usuario se debe correr el siguiente comando:

```Bash
uv run main.py crear-usuario a "b" "c"
```
>* `a` corresponde a el id del usuario que quiere realizar el comando (debe ser un numero entero).
>* `"b"` corresponde al nombre del nuevo usuario, se debe escribir entre comillas dobles.
>* `"c"` corresponde al Rol que obtendra el nuevo usuario: `"gerente"` o `"empleado"`.

---

