

marcos_libres = [0x0,0x1,0x2]
reqs = [ 0x00, 0x12, 0x64, 0x65, 0x8D, 0x8F, 0x19, 0x18, 0xF1, 0x0B, 0xDF, 0x0A ]
segmentos =[('.text', 0x00, 0x1A),
            ('.data', 0x40, 0x28),
            ('.heap', 0x80, 0x1F),
            ('.stack', 0xC0, 0x22),
            ]

def procesar(segmentos, reqs, marcos_libres):
    pagina_tam = 16  # tamaño de una página en palabras
    tabla_paginas = {}  # mapea páginas cargadas: (segmento, num_pagina) -> marco
    uso_reciente = []   # lista que mantiene orden de uso más reciente (LRU)
    marco_a_pagina = {}  # marco -> (segmento, num_pagina)
    resultados = []

    for req in reqs:
        # Encontrar a qué segmento pertenece la dirección
        segmento_encontrado = None
        for nombre, base, limite in segmentos:
            if base <= req < base + limite:
                segmento_encontrado = (nombre, base)
                break

        if not segmento_encontrado:
            # Dirección fuera de los límites de todos los segmentos
            resultados.append((req, 0x1FF, "Segmentation Fault"))
            continue

        nombre_seg, base = segmento_encontrado
        desplazamiento = req - base
        num_pagina = desplazamiento // pagina_tam
        offset = desplazamiento % pagina_tam

        clave_pagina = (nombre_seg, num_pagina)

        if clave_pagina in tabla_paginas:
            # Página ya está en memoria
            marco = tabla_paginas[clave_pagina]
            direccion_fisica = marco * pagina_tam + offset
            resultados.append((req, direccion_fisica, "Marco ya estaba asignado"))

            # Actualizar uso reciente
            if clave_pagina in uso_reciente:
                uso_reciente.remove(clave_pagina)
            uso_reciente.append(clave_pagina)

        else:
            if marcos_libres:
                # Hay marcos disponibles
                marco = marcos_libres.pop(0)
                tabla_paginas[clave_pagina] = marco
                marco_a_pagina[marco] = clave_pagina
                direccion_fisica = marco * pagina_tam + offset
                resultados.append((req, direccion_fisica, "Marco libre asignado"))
            else:
                # Reemplazo con LRU
                pagina_lru = uso_reciente.pop(0)
                marco = tabla_paginas[pagina_lru]
                del tabla_paginas[pagina_lru]

                # Asignar el nuevo
                tabla_paginas[clave_pagina] = marco
                marco_a_pagina[marco] = clave_pagina
                direccion_fisica = marco * pagina_tam + offset
                resultados.append((req, direccion_fisica, "Marco asignado"))

            uso_reciente.append(clave_pagina)

    return resultados
    
def print_results(results):
    for result in results:
        print(f"Req: {result[0]:#0{4}x} Direccion Fisica: {result[1]:#0{4}x} Acción: {result[2]}")

if __name__ == '__main__':
    results = procesar(segmentos, reqs, marcos_libres)
    print_results(results)

