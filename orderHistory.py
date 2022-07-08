import MetaTrader5 as mt5
import pandas as pd
from cuentas import(cuentas)
from datetime import datetime
import sched
import time

pd.set_option('display.max_columns', 500) # cuántas columnas mostramos
pd.set_option('display.width', 1500)      # máx. anchura del recuadro para la muestra

# declaramos variables de diccionario a usar
usuario=cuentas["user"]
password= cuentas["password"]
servidor= cuentas["server"]

# mostramos los datos sobre el paquete MetaTrader5
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)

# establecemos la conexión con el terminal MetaTrader 5
# obtenemos el número de órdenes en la historia
    
# Funcion para ejecutar script según tiempo
def  demora(tiempo,mensaje):
	cada_cuanto =  sched.scheduler(time.time,time.sleep)
	cada_cuanto.enterabs(tiempo,1,print,argument=(mensaje,))
	balanceCuentas()
	cada_cuanto.run()

 
# conectamos con la cuenta indicando la contraseña y el servidor

def balanceCuentas():

    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()
    for k in range (len(usuario)):

        authorized=mt5.login(usuario[k],password=password[k],server=servidor[k])
        if authorized:
            account_info=mt5.account_info()
            if account_info!=None:
                # mostramos como son los datos sobre la cuenta
                print("cuenta ",usuario[k])
                print("Balance actual: ",account_info.balance)
                print("Equidad actual: ",account_info.equity)
                infoCuenta()
                
                # mostramos los datos sobre la cuenta comercial en forma de diccionario
        else:
            print("failed to connect to trade account ",usuario[k],"with password=",password[k], "error code =",mt5.last_error())

def infoCuenta():
    usd_positions=mt5.positions_get(group="*USD*")
    if usd_positions==None:
        print("No positions with group=\"*USD*\", error code={}".format(mt5.last_error()))
    elif len(usd_positions)>0:
        # mostramos estas posiciones en forma de recuadro con la ayuda de pandas.DataFrame
        df=pd.DataFrame(list(usd_positions),columns=usd_positions[0]._asdict().keys())
        print(df.profit)




# finalizamos la conexión con el terminal MetaTrader 5
mt5.shutdown()
while True:
	demora(time.time()+10,"ejecutando una función")

