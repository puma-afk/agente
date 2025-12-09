from agentes.admin import menu_editar_sucursal
from agentes.ruta import AgenteRuta
from agentes.comprador import AgenteComprador
from agentes.cajero import AgenteCajero
from agentes.navegador import AgenteNavegadorPasillos
from core.entorno import crear_entorno_y_mapa


def main():
    print("=== Sistema Multiagente - Vale Navideño Hipermaxi (Versión 2.1 - Temple Simulado) ===")

    entorno, mapa_ciudad, grafos_pasillos, mapas_producto_pasillo = crear_entorno_y_mapa()

    usar_admin = input("\n¿Desea editar sucursales antes de la simulación? (s/n): ").strip().lower()
    if usar_admin == "s":
        menu_editar_sucursal(entorno)

    try:
        monto_vale = float(input("\nIngrese el monto del vale (Bs): "))
    except ValueError:
        print("Monto inválido. Saliendo...")
        return

    print("\n¿Cómo desea elegir la sucursal?")
    print("1. El usuario elige manualmente.")
    print("2. El Agente de Ruta elige la sucursal más cercana desde 'Casa'.")
    modo = input("Opción (1/2): ").strip()

    if modo == "1":
        entorno.listar_sucursales()
        try:
            idx = int(input("Elija una sucursal por número: ")) - 1
        except ValueError:
            print("Entrada inválida.")
            return
        sucursal = entorno.obtener_por_indice(idx)
        if sucursal is None:
            print("Sucursal inválida. Saliendo...")
            return
        print(f"\nSucursal elegida por el usuario: {sucursal.nombre}")

    elif modo == "2":
        nombres_sucursales = entorno.nombres_sucursales()
        agente_ruta = AgenteRuta(mapa_ciudad, nombres_sucursales)
        nombre_sucursal = agente_ruta.sucursal_mas_cercana("Casa")
        if nombre_sucursal is None:
            print("No se encontró ninguna sucursal alcanzable. Saliendo...")
            return
        sucursal = entorno.obtener_por_nombre(nombre_sucursal)
        print(f"\n[Agente de Ruta] Sucursal más cercana desde 'Casa': {sucursal.nombre}")
    else:
        print("Opción inválida. Saliendo...")
        return

    sucursal.listar_productos()

    # --- Agente Comprador (Temple Simulado) ---
    comprador = AgenteComprador(sucursal, monto_vale)
    print("\n[Agente Comprador] Buscando una buena combinación de productos (Temple Simulado)...")
    compra = comprador.planificar_compra()

    if not compra:
        print("No se encontró ninguna combinación válida (todos los productos superan el monto del vale).")
        return

    # --- Agente Navegador: primero mostrar la ruta interna ---
    grafo_pasillos = grafos_pasillos.get(sucursal.nombre)
    mapa_producto_pasillo = mapas_producto_pasillo.get(sucursal.nombre, {})

    if grafo_pasillos is None:
        print("\n[Agente Navegador] No hay grafo de pasillos definido para esta sucursal.")
    else:
        navegador = AgenteNavegadorPasillos(grafo_pasillos, mapa_producto_pasillo)
        ruta = navegador.planificar_ruta(compra)
        print("\n[Agente Navegador] Ruta interna sugerida dentro de la sucursal:")
        print(" -> ".join(ruta))

    # --- Luego mostrar la compra ---
    print("\nPropuesta de compra (según el Agente Comprador):")
    for p in compra:
        print(f"- {p.nombre}: {p.precio:.2f} Bs")
    total = sum(p.precio for p in compra)
    print(f"Total: {total:.2f} Bs  (Vale: {monto_vale:.2f} Bs)")

    # --- Finalmente el Agente Cajero decide ---
    cajero = AgenteCajero(monto_vale)
    print("\n[Agente Cajero] Verificando compra...")

    if cajero.verificar_compra(compra):
        print("Compra APROBADA. No se excede el monto del vale.")
    else:
        print("Compra RECHAZADA. Se excede el monto del vale.")

    print("\nFin de la simulación.")


if __name__ == "__main__":
    main()
