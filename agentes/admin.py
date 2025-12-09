from core.entorno import EntornoHipermaxi


def menu_editar_sucursal(entorno: EntornoHipermaxi):
    while True:
        print("\n=== MODO ADMINISTRADOR DE SUCURSALES ===")
        entorno.listar_sucursales()
        print("0. Salir del modo administrador")
        opcion = input("Seleccione una sucursal para editar (número): ").strip()

        if opcion == "0":
            break

        try:
            idx = int(opcion) - 1
        except ValueError:
            print("Entrada inválida.")
            continue

        sucursal = entorno.obtener_por_indice(idx)
        if sucursal is None:
            print("Sucursal inválida.")
            continue

        while True:
            print(f"\n--- Editando {sucursal.nombre} ---")
            sucursal.listar_productos()
            print("\nOpciones:")
            print("1. Agregar nuevo producto")
            print("2. Cambiar precio de un producto")
            print("3. Eliminar un producto")
            print("4. Volver a la lista de sucursales")

            op2 = input("Elija opción: ").strip()

            if op2 == "1":
                nombre = input("Nombre del nuevo producto: ")
                try:
                    precio = float(input("Precio (Bs): "))
                except ValueError:
                    print("Precio inválido.")
                    continue
                sucursal.agregar_producto(nombre, precio)
                print("Producto agregado.")

            elif op2 == "2":
                try:
                    num = int(input("Número de producto a modificar: ")) - 1
                    nuevo = float(input("Nuevo precio (Bs): "))
                except ValueError:
                    print("Entrada inválida.")
                    continue
                sucursal.actualizar_precio_por_indice(num, nuevo)
                print("Precio actualizado (si el índice era válido).")

            elif op2 == "3":
                try:
                    num = int(input("Número de producto a eliminar: ")) - 1
                except ValueError:
                    print("Entrada inválida.")
                    continue
                sucursal.eliminar_producto_por_indice(num)

            elif op2 == "4":
                break
            else:
                print("Opción inválida.")

