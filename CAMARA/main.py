from time import sleep
import machine
import camera

def main():
    try:
        camera_init()
        sleep (2)
        
        foto = camera.capture()
        print("foto tomada")
        sleep (2)
                
        #Guardar la imagen en el sistema de archivos
        imgFile = open("foto1.jpg", "wb")
        imgFile.write(foto)
        imgFile.close()
        
        sleep (2)
        
        camera.deinit()
                  
        print("foto guardada")
                
        print("camara off")
        
    except Exception as err:
        print ("Error= "+str (err))
        sleep (2)
        pass

def camera_init():
    print("camera init")
    try:# Disable camera initialization
        camera.deinit()
    except:
        pass
    # Enable camera initialization
    camera.init(0, d0=4, d1=5, d2=18, d3=19, d4=36, d5=39, d6=34, d7=35,
                format=camera.JPEG, framesize=camera.FRAME_VGA, 
                xclk_freq=camera.XCLK_20MHz,
                href=23, vsync=25, reset=-1, pwdn=-1,
                sioc=27, siod=26, xclk=21, pclk=22, fb_location=camera.PSRAM)

    camera.framesize(camera.FRAME_VGA) # Set the camera resolution 640x480
    # The options are the following:
    # FRAME_96X96 FRAME_QQVGA FRAME_QCIF FRAME_HQVGA FRAME_240X240
    # FRAME_QVGA FRAME_CIF FRAME_HVGA FRAME_VGA FRAME_SVGA
    # FRAME_XGA FRAME_HD FRAME_SXGA FRAME_UXGA
    # Note: The higher the resolution, the more memory is used.
    # Note: And too much memory may cause the program to fail.
    
    camera.flip(1)                       # Flip up and down window: 0-1
    camera.mirror(1)                     # Flip window left and right: 0-1
    camera.saturation(0)                 # saturation: -2,2 (default 0). -2 grayscale 
    camera.brightness(0)                 # brightness: -2,2 (default 0). 2 brightness
    camera.contrast(0)                   # contrast: -2,2 (default 0). 2 highcontrast
    camera.quality(10)                   # quality: # 10-63 lower number means higher quality
    # Note: The smaller the number, the sharper the image. The larger the number, the more blurry the image
    
    camera.speffect(camera.EFFECT_NONE)  # special effects:
    # EFFECT_NONE (default) EFFECT_NEG EFFECT_BW EFFECT_RED EFFECT_GREEN EFFECT_BLUE EFFECT_RETRO
    camera.whitebalance(camera.WB_NONE)  # white balance
    # WB_NONE (default) WB_SUNNY WB_CLOUDY WB_OFFICE WB_HOME
    print("camera init done")
    pass
    
if __name__ == '__main__':
    main()