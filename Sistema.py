import csv

class SistemaReserva:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        self.reservas = self.cargar_reservas()

    def cargar_reservas(self):
        reservas = []
        with open(self.nombre_archivo, 'r') as archivo:
            lector_csv = csv.reader(archivo)
            for fila in lector_csv:
                reserva = {
                    'tipo': fila[0],
                    'cliente': fila[1],
                    'mesas': int(fila[2]),
                    'ambiente': fila[3],
                    'plan_comida': fila[4],
                    'plan_degustacion': fila[5]
                }
                reservas.append(reserva)
        return reservas

    def guardar_reservas(self):
        with open(self.nombre_archivo, 'w', newline='') as archivo:
            escritor_csv = csv.writer(archivo)
            for reserva in self.reservas:
                fila = [
                    reserva['tipo'],
                    reserva['cliente'],
                    str(reserva['mesas']),
                    reserva['ambiente'],
                    reserva['plan_comida'],
                    reserva['plan_degustacion']
                ]
                escritor_csv.writerow(fila)

    def agregar_reserva(self, tipo, cliente, mesas, ambiente, plan_comida='', plan_degustacion=''):
        reserva = {
            'tipo': tipo,
            'cliente': cliente,
            'mesas': mesas,
            'ambiente': ambiente,
            'plan_comida': plan_comida,
            'plan_degustacion': plan_degustacion
        }
        self.reservas.append(reserva)

    def buscar_reservas_por_cliente(self, cliente):
        reservas_cliente = []
        for reserva in self.reservas:
            if reserva['cliente'] == cliente:
                reservas_cliente.append(reserva)
        return reservas_cliente

    def calcular_precio(self, reserva):
        precio_total = 0
        if reserva['tipo'] == 'NORMAL':
            if reserva['plan_comida'] == 'Inicial':
                precio_total += 20000
            elif reserva['plan_comida'] == 'Intermedio':
                precio_total += 45000
            elif reserva['plan_comida'] == 'Avanzado':
                precio_total += 60000
        elif reserva['tipo'] == 'EVENTO':
            # Implementar la lógica para calcular el precio de un evento personalizado según los servicios adicionales y el menú confeccionado con el chef
            pass
        return precio_total

    def liberar_mesas(self, cliente):
        reservas_cliente = self.buscar_reservas_por_cliente(cliente)
        for reserva in reservas_cliente:
            mesas_liberadas = reserva['mesas']
            reserva['mesas'] = 0
            self.reservas.remove(reserva)
            print(f"Se han liberado {mesas_liberadas} mesas de la reserva de {cliente}")

    def verificar_disponibilidad(self, mesas_necesarias, ambiente):
        mesas_disponibles = 0
        for reserva in self.reservas:
            if reserva['ambiente'] == ambiente:
                mesas_disponibles += reserva['mesas']
        return mesas_disponibles >= mesas_necesarias

    def reservar_normal(self, cliente, mesas, ambiente, plan_comida='', plan_degustacion=''):
        if self.verificar_disponibilidad(mesas, ambiente):
            self.agregar_reserva('NORMAL', cliente, mesas, ambiente, plan_comida, plan_degustacion)
            print(f"Reserva exitosa para {cliente}.")
        else:
            print("No hay suficientes mesas disponibles en el ambiente solicitado.")

    def reservar_evento(self, tipo_evento, cliente, mesas, ambiente, servicios_adicionales=[], menu_personalizado=[]):
        if self.verificar_disponibilidad(mesas, ambiente):
            self.agregar_reserva('EVENTO', cliente, mesas, ambiente)
            reserva_evento = self.buscar_reservas_por_cliente(cliente)[-1]
            reserva_evento['tipo_evento'] = tipo_evento
            reserva_evento['servicios_adicionales'] = servicios_adicionales
            reserva_evento['menu_personalizado'] = menu_personalizado
            print(f"Reserva de evento exitosa para {cliente}.")
        else:
            print("No hay suficientes mesas disponibles en el ambiente solicitado.")


# Ejemplo de uso de la clase SistemaReserva
sistema_reserva = SistemaReserva('reservas.csv')

# Cargar las reservas desde el archivo
print(sistema_reserva.reservas)

# Agregar una nueva reserva
sistema_reserva.agregar_reserva('NORMAL', 'Juan', 5, 'Interior', 'Intermedio')
print(sistema_reserva.reservas)

# Buscar las reservas de un cliente
reservas_cliente = sistema_reserva.buscar_reservas_por_cliente('Juan')
print(reservas_cliente)

# Calcular el precio de una reserva
reserva = reservas_cliente[0]
precio = sistema_reserva.calcular_precio(reserva)
print(f"Precio de la reserva: {precio}")

# Liberar mesas de un cliente
sistema_reserva.liberar_mesas('Juan')
print(sistema_reserva.reservas)

# Reservar una mesa normal
sistema_reserva.reservar_normal('María', 3, 'Exterior', 'Inicial', 'Degustación')
print(sistema_reserva.reservas)

# Reservar un evento
sistema_reserva.reservar_evento('Boda', 'Pedro', 10, 'Salón', ['Decoración', 'Música'], ['Entrada', 'Plato principal'])
print(sistema_reserva.reservas)

# Guardar las reservas en el archivo
sistema_reserva.guardar_reservas()
