

marcos_libres = [0x0,0x1,0x2]
reqs = [ 0x00, 0x12, 0x64, 0x65, 0x8D, 0x8F, 0x19, 0x18, 0xF1, 0x0B, 0xDF, 0x0A ]
segmentos =[('.text', 0x00, 0x1A),
            ('.data', 0x40, 0x28),
            ('.heap', 0x80, 0x1F),
            ('.stack', 0xC0, 0x22),
            ]

def procesar(segmentos, reqs, marcos_libres):
    tamano_pagina = 16
    paginas_en_memoria = {}        # num_pagina -> marco
    marco_a_pagina = {}            # marco -> num_pagina
    historial_uso = []             # lista LRU
    resultados = []

    def es_valida(direccion):
        for seg in segmentos:
            nombre, inicio, longitud = seg
            if inicio <= direccion < inicio + longitud:
                return True
        return False

    def direccion_fisica(marco, offset):
        if marco == 0:
            return 0x20 + offset
        elif marco == 1:
            return 0x10 + offset
        else:
            return offset

    for ref in reqs:
        if not es_valida(ref):
            resultados.append((ref, 0x1FF, "Segmentation Fault"))
            continue

        pagina = ref // tamano_pagina
        offset = ref % tamano_pagina

        if pagina in paginas_en_memoria:
            marco = paginas_en_memoria[pagina]
            if pagina in historial_uso:
                historial_uso.remove(pagina)
            historial_uso.append(pagina)
            resultados.append((ref, direccion_fisica(marco, offset), "Marco ya estaba asignado"))
        else:
            if marcos_libres:
                marco = marcos_libres.pop(0)
                paginas_en_memoria[pagina] = marco
                marco_a_pagina[marco] = pagina
                historial_uso.append(pagina)
                resultados.append((ref, direccion_fisica(marco, offset), "Marco libre asignado"))
            else:
                pagina_remover = historial_uso.pop(0)
                marco_reemplazo = paginas_en_memoria[pagina_remover]
                del paginas_en_memoria[pagina_remover]
                paginas_en_memoria[pagina] = marco_reemplazo
                marco_a_pagina[marco_reemplazo] = pagina
                historial_uso.append(pagina)
                resultados.append((ref, direccion_fisica(marco_reemplazo, offset), "Marco asignado"))

    return resultados
    
def print_results(results):
    for result in results:
        print(f"Req: {result[0]:#0{4}x} Direccion Fisica: {result[1]:#0{4}x} Acción: {result[2]}")

if __name__ == '__main__':
    results = procesar(segmentos, reqs, marcos_libres)
    print_results(results)

