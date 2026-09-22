import tinytuya
from Interface import *
from config import *

lampada_Norte = tinytuya.BulbDevice(
    Device_ID_1,
    IP_1,
    Local_Key_1,
    version=3.5
)

lampada_Sul = tinytuya.BulbDevice(
    Device_ID_2,
    IP_2,
    Local_Key_2,
    version=3.5
)



Desligar_Sul = lampada_Sul.turn_off
Desligar_Norte = lampada_Norte.turn_off

Ligar_Sul = lampada_Sul.turn_on
Ligar_Norte = lampada_Norte.turn_on




