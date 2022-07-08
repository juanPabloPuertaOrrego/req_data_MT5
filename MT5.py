import MetaTrader5 as mt5
import pandas as pd
from cuentas import(cuentas)
from datetime import datetime
import sched
import time


# declaramos variables de diccionario a usar
usuario=cuentas["user"]
password= cuentas["password"]
servidor= cuentas["server"]

# mostramos los datos sobre el paquete MetaTrader5
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)

# establecemos la conexión con el terminal MetaTrader 5
# obtenemos el número de órdenes en la historia
from_date=datetime(2020,1,1)
to_date=datetime.now()
history_orders=mt5.history_orders_get(from_date, to_date, group="*GBP*")
if history_orders==None:
    print("No history orders with group=\"*GBP*\", error code={}".format(mt5.last_error()))
elif len(history_orders)>0:
    print("history_orders_get({}, {}, group=\"*GBP*\")={}".format(from_date,to_date,len(history_orders)))
print()
    
# Funcion para ejecutar script según tiempo
def  demora(tiempo,mensaje):
	cada_cuanto =  sched.scheduler(time.time,time.sleep)
	cada_cuanto.enterabs(tiempo,1,print,argument=(mensaje,))
	balanceCuentas()
	cada_cuanto.run()
 
# conectamos con la cuenta indicando la contraseña y el servidor

def balanceCuentas():
    from_date=datetime(2020,1,1)

    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()
    for k in range (len(usuario)):

        authorized=mt5.login(usuario[k],password=password[k],server=servidor[k])
        if authorized:
            account_info=mt5.account_info()
            if account_info!=None:
                # mostramos como son los datos sobre la cuenta
                print("Balance actual: ",account_info.balance,"cuenta ",usuario[k])
                # mostramos los datos sobre la cuenta comercial en forma de diccionario
        else:
            print("failed to connect to trade account ",usuario[k],"with password=",password[k], "error code =",mt5.last_error())

# finalizamos la conexión con el terminal MetaTrader 5
mt5.shutdown()
while True:
	demora(time.time()+10,"ejecutando una función")
