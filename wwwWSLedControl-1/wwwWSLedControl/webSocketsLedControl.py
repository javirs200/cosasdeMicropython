# FUNCIÓN PARA ESTABLECER LA CONEXIÓN WIFI (STATION)

def do_connect(SSID, PASSWORD):
    import network                            # importa el módulo network
    global sta_if
    sta_if = network.WLAN(network.STA_IF)     # instancia el objeto -sta_if- para realizar la conexión en modo STA 
    if not sta_if.isconnected():              # si no existe conexión...
        sta_if.active(True)                       # activa el interfaz STA del ESP32
        sta_if.connect(SSID, PASSWORD)            # inicia la conexión con el AP
        print('Conectando a la red', SSID +"...")
        while not sta_if.isconnected():           # ...si no se ha establecido la conexión...
            pass                                  # ...repite el bucle...
    print('Configuración de red (IP/netmask/gw/DNS):', sta_if.ifconfig())
    
                                                  # ¡¡¡IMPORTANTE!!!
do_connect("<nombre_de_red>","<clave_de_red>")    # RELLENAR CON EL  nombre/clave_de_red 


# IMPORTA LOS MÓDULOS/CLASES PARA CONTROLAR EL SERVIDOR

from MicroWebSrv2  import *                          # importa el módulo MicroWebSrv2  
from time          import sleep
from _thread       import allocate_lock


#  INICIALIZA EL LED BUILT-IN (PIN 21  - PLACA TTGO-T8 v1.7)

from machine import Pin,PWM
pwmLED = PWM(Pin(21), freq=78100, duty=512) 

# ============================================================================
# ============================================================================
# ============================================================================

def OnWebSocketAccepted(microWebSrv2, webSocket) :
    print('Example WebSocket accepted:')
    print('   - User   : %s:%s' % webSocket.Request.UserAddress)
    print('   - Path   : %s'    % webSocket.Request.Path)
    print('   - Origin : %s'    % webSocket.Request.Origin)
    WSJoinChat(webSocket)

# ============================================================================
# ============================================================================
# ============================================================================

global _chatWebSockets
_chatWebSockets = [ ]

global _chatLock
_chatLock = allocate_lock()

# ------------------------------------------------------------------------

def WSJoinChat(webSocket) :
    webSocket.OnTextMessage = OnWSChatTextMsg
    webSocket.OnClosed      = OnWSChatClosed
    addr = webSocket.Request.UserAddress
    with _chatLock :
        _chatWebSockets.append(webSocket)
        webSocket.SendTextMessage(str(pwmLED.duty()))  #Cuanto se inica una conexión envia al cliente la intensidad del LED (0-1023)

# ------------------------------------------------------------------------

def OnWSChatTextMsg(webSocket, msg) :
    addr = webSocket.Request.UserAddress
    with _chatLock :
        for ws in _chatWebSockets :                    #Cuanto un cliente envía un mensaje, el servidor lo reenvía al resto de los clientes...
            if ws != webSocket :
                ws.SendTextMessage(msg)
    pwmLED.duty(int(msg))                              #... y se regula la intensidad del LED (0-1023) de acuerdo al mensaje recibido.

# ------------------------------------------------------------------------

def OnWSChatClosed(webSocket) :
    addr = webSocket.Request.UserAddress
    with _chatLock :
        if webSocket in _chatWebSockets :
            _chatWebSockets.remove(webSocket)

# ============================================================================
# ============================================================================
# ============================================================================

print()

wsMod = MicroWebSrv2.LoadModule('WebSockets')     # Carga el módulo WebSockets y lo configura
wsMod.OnWebSocketAccepted = OnWebSocketAccepted

mws2 = MicroWebSrv2()                             # Instanciala clase MicroWebSrv2  
mws2.RootPath = "/wwwWSLedControl"
mws2.SetEmbeddedConfig()                          # Utiliza una configuración ligera para MicroPython
mws2.StartManaged()                               # Inicia el servidor de una forma sencilla en modo "managed"


try :                                             # Ejecuta el programa hasta que el teclado lo interrumpe
    while mws2.IsRunning :
        sleep(1)
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
