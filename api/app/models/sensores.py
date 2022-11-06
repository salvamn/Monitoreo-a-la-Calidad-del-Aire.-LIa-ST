class Dispositivo:
    ubicacion: str
    usuario: str
    
    def __init__(self, ubicacion, usuario) -> None:
        self.ubicacion = ubicacion
        self.usuario = usuario
        
    def __str__(self) -> str:
        return f"Ubicación: {self.ubicacion}"
    
    
    
class Medicion_dht:
    id: int
    humedad: float
    temperatura: float
    fecha: str
    hora: str
    ubicacion_dispositivo: str
    
    def __init__(self, id, humedad, temperatura, fecha, hora, ubicacion_dispositivo) -> None:
        self.id = id
        self.humedad = humedad
        self.temperatura = temperatura
        self.fecha = fecha
        self.hora = hora
        self.ubicacion_dispositivo = ubicacion_dispositivo
        
    def __str__(self) -> str:
        return f"ID: {self.id}, Ubicacion: {self.ubicacion_dispositivo}, Sensor: DHT22"

    
    
class Medicion_uv:
    id: int
    radiacion_uv: float
    fecha: str
    hora: str
    ubicacion_dispositivo: str
    
    def __init__(self, id, radiacion_uv, fecha, hora, ubicacion_dispositivo) -> None:
        self.id = id
        self.radiacion_uv = radiacion_uv
        self.fecha = fecha
        self.hora = hora
        self.ubicacion_dispositivo = ubicacion_dispositivo
        
    def __str__(self) -> str:
        return f"ID: {self.id}, Ubicacion: {self.ubicacion_dispositivo}, Sensor: UV"
    

class Medicion_nova:
    id: int
    pm_dos_punto_cinco: float
    pm_diez: float
    fecha: str
    hora: str
    ubicacion_dispositivo: str
    
    def __init__(self, id, pm_dos_punto_cinco, pm_diez, fecha, hora, ubicacion_dispositivo) -> None:
        self.id = id
        self.pm_dos_punto_cinco = pm_dos_punto_cinco
        self.pm_diez = pm_diez
        self.fecha = fecha
        self.hora = hora
        self.ubicacion_dispositivo = ubicacion_dispositivo
        
    def __str__(self) -> str:
        return f"ID: {self.id}, Ubicacion: {self.ubicacion_dispositivo}, Sensor: Nova"