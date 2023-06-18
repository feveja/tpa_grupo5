class Mesa:
    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.ocupada = False

class Restaurante:
    def __init__(self):
        self.mesas = []
        self.salones = []
        self.terrazas = []

        # Creamos las mesas de diferentes tamaños
        for capacidad in [2, 3, 5]:
            for i in range(10):
                self.mesas.append(Mesa(capacidad))

        # Creamos los salones y la terraza
        self.salones.append({"nombre": "CENTRAL", "capacidad": 200})
        self.salones.append({"nombre": "VARAS", "capacidad": 30})
        self.salones.append({"nombre": "MONTT", "capacidad": 30})
        self.terrazas.append({"nombre": "TERRAZA", "capacidad": 40})

    def buscar_mesa(self, capacidad, ambiente):
        # Buscamos una mesa disponible en el ambiente deseado
        for mesa in self.mesas:
            if not mesa.ocupada and mesa.capacidad == capacidad:
                # Comprobamos si la mesa está en el ambiente deseado
                if ambiente == "CENTRAL" or ambiente == "TERRAZA":
                    return mesa
                elif ambiente == "VARAS" or ambiente == "MONTT":
                    for salon in self.salones:
                        if salon["nombre"] == ambiente and len(salon["mesas"]) < salon["capacidad"] / capacidad:
                            salon["mesas"].append(mesa)
                            return mesa

        # Si no encontramos mesa, devolvemos None
        return None

class Reserva:
    def __init__(self, restaurante, cantidad_personas, tipo_reserva, ambiente, plan_comida=None, plan_degustacion=None):
        self.restaurante = restaurante
        self.cantidad_personas = cantidad_personas
        self.tipo_reserva = tipo_reserva
        self.ambiente = ambiente
        self.plan_comida = plan_comida
        self.plan_degustacion = plan_degustacion
        self.mesas = []

    def hacer_reserva(self):
        # Buscamos las mesas necesarias
        mesas_necesarias = self.cantidad_personas // 5 + (1 if self.cantidad_personas % 5 > 0 else 0)
        for i in range(mesas_necesarias):
            mesa = self.restaurante.buscar_mesa(5, self.ambiente)
            if mesa is None:
                # Si no encontramos mesas, liberamos las mesas que ya habíamos reservado y devolvemos False
                for mesa in self.mesas:
                    mesa.ocupada = False
                return False
            else:
                mesa.ocupada = True
                self.mesas.append(mesa)

        # Si llegamos aquí, la reserva fue exitosa
        return True