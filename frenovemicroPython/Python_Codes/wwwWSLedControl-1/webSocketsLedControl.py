# FUNCIÓN PARA ESTABLECER LA CONEXIÓN WIFI (STATION)

def do_connect(SSID, PASSWORD):
    import network                            # importa el módulo network
    global sta_if
    sta_if = network.WLAN(network.AP_IF)     # instancia el objeto -sta_if- para realizar la conexión en modo STA 
    if not sta_if.isconnected():              # si no existe conexión...
        sta_if.active(True)                       # activa el interfaz STA del ESP32
        sta_if.config(essid=SSID,authmode=network.AUTH_WPA_WPA2_PSK, password=PASSWORD)            # inicia la conexión con el AP
        print('Conectando a la red', SSID +"...")
        print('Configuración de red (IP/netmask/gw/DNS):', sta_if.ifconfig())
    
                                                  # ¡¡¡IMPORTANTE!!!
do_connect("ESP32_AP","xcom1234")    # RELLENAR CON EL  nombre/clave_de_red

def convert(x,a,b,c=0,d=1):
    """converts values in the range [a,b] to values in the range [c,d]"""
    return c + float(x-a)*float(d-c)/(b-a)


# IMPORTA LOS MÓDULOS/CLASES PARA CONTROLAR EL SERVIDOR

from MicroWebSrv2  import *                          # importa el módulo MicroWebSrv2  
import time


#  INICIALIZA EL LED BUILT-IN (PIN 21  - PLACA TTGO-T8 v1.7)

from myservo import myServo
global servo

servo=myServo(15)
servo.myServoWriteAngle(0)
time.sleep_ms(10)

# ============================================================================
# ============================================================================
# ============================================================================

def OnWebSocketAccepted(microWebSrv2, webSocket) :
    print('Example WebSocket accepted:')
    print('   - User   : %s:%s' % webSocket.Request.UserAddress)
    print('   - Path   : %s'    % webSocket.Request.Path)
    print('   - Origin : %s'    % webSocket.Request.Origin)
    WSJoin(webSocket)

# ============================================================================
# ============================================================================
# ============================================================================

# ------------------------------------------------------------------------

def WSJoin(webSocket) :
    webSocket.OnTextMessage = OnWSMsg
    webSocket.OnClosed      = OnWSClosed
    value = convert(servo.getPos(),0,180,0,100)
    webSocket.SendTextMessage(str(value))  

# ------------------------------------------------------------------------

def OnWSMsg(webSocket, msg) :
    value = convert(int(msg),0,100,0,180)
    servo.myServoWriteAngle(value)
                                     
    
def OnWSClosed(webSocket) :
    pass

# ------------------------------------------------------------------------

# ============================================================================
# ============================================================================
# ============================================================================

print()

wsMod = MicroWebSrv2.LoadModule('WebSockets')     # Carga el módulo WebSockets y lo configura
wsMod.OnWebSocketAccepted = OnWebSocketAccepted

mws2 = MicroWebSrv2()                             # Instanciala clase MicroWebSrv2  
mws2.RootPath = "/"
mws2.SetEmbeddedConfig()                          # Utiliza una configuración ligera para MicroPython
mws2.StartManaged()                               # Inicia el servidor de una forma sencilla en modo "managed"


try :                                             # Ejecuta el programa hasta que el teclado lo interrumpe
    while mws2.IsRunning :
        time.sleep_ms(1)
except KeyboardInterrupt :
    pass

# End,
print()
mws2.Stop()
print('Bye')
print()

# ============================================================================
# ============================================================================
# ============================================================================
