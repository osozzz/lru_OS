# algo_rem_mem_2025_parcial_3

Desarrollo del simulador de algoritmos de reemplazo de páginas

Este es el parcial de la materia Sistemas Operativos. Como parte de la actividad, se debe hacer un fork del repositorio correspondiente e invitar al profesor `fcardonaEAFIT (fcardona@eafit.edu.co)` como colaborador.

### Enunciado

Dependiendo del grupo asignado:

- **Grupos I y III →** deben implementar **FIFO**
- **Grupos II y IV →** deben implementar **LRU**

En el archivo `sim_algo_reem_mem.py` se debe implementar únicamente la función `procesar`, la cual tiene la siguiente estructura:

### Parámetros de entrada:

- `segmentos`: lista de tuplas que contienen el nombre del segmento, la base y el límite.  
  Ejemplo: `('.text', 0x00, 0x1A)`

- `reqs`: lista de direcciones que el programa solicita.  
  Ejemplo: `[0x00, 0x10, 0x20]`

- `marcos_libres`: lista de marcos disponibles en la memoria física.

### La función debe retornar, para cada requerimiento, una tripleta con:

- **`Req`**: la dirección lógica solicitada.
- **`Dirección Física`**: la dirección física equivalente o `0x1FF` si hay error.
- **`Acción`**: mensaje indicando qué se hizo, puede ser uno de los siguientes:

  - `"Marco libre asignado"`: se asignó un marco disponible.
  - `"Marco ya estaba asignado"`: ya existía el marco para esa página.
  - `"Marco asignado"`: se reemplazó una página (por LRU o FIFO según el grupo).
  - `"Segmentation Fault"`: la dirección lógica no pertenece a ningún segmento válido.

---

### Ejemplo de ejecución

```python
marcos_libres = [0x0, 0x1, 0x2]
reqs = [0x00, 0x12, 0x64, 0x65, 0x8D, 0x8F, 0x19, 0x18, 0xF1, 0x0B, 0xDF, 0x0A]
segmentos = [
    ('.text', 0x00, 0x1A),
    ('.data', 0x40, 0x28),
    ('.heap', 0x80, 0x1F),
    ('.stack', 0xC0, 0x22)
]
```

Se obtiene la siguiente salida:

```shell
Req: 0x00 Direccion Fisica: 0x20 Acción: Marco libre asignado
Req: 0x12 Direccion Fisica: 0x12 Acción: Marco libre asignado
Req: 0x64 Direccion Fisica: 0x04 Acción: Marco libre asignado
Req: 0x65 Direccion Fisica: 0x05 Acción: Marco ya estaba asignado
Req: 0x8d Direccion Fisica: 0x2d Acción: Marco asignado
Req: 0x8f Direccion Fisica: 0x2f Acción: Marco ya estaba asignado
Req: 0x19 Direccion Fisica: 0x19 Acción: Marco ya estaba asignado
Req: 0x18 Direccion Fisica: 0x18 Acción: Marco ya estaba asignado
Req: 0xf1 Direccion Fisica: 0x1ff Acción: Segmention Fault
```

## Autor.

 * Juan Alejandro Osorno Bustamante
