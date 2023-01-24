import MetaTrader5 as mt5
import time
import json
from cuentas import(cuentas) # Base de datos quemada, se elimina cuando se tenga las credenciales desde HTTP
from datetime import datetime # Para ejecutar con ciclo while, se elimina cuando se acondicione la ejecución, ya sea 
#con un tiempo definido o cada vez que se haga un login(ideal esta opción)

#from path import base_path

# declaramos variables de diccionario a usar
usuario=cuentas["user"] #Pendiente variable desde petición HTTP desde el formulario de login
password= cuentas["password"] #Pendiente variable desde petición HTTP desde el formulario de login
servidor= cuentas["server"] # Servidor unico de brocker Infinox

# mostramos los datos sobre el paquete MetaTrader5
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)

# conectamos con la cuenta indicando la contraseña y el servidor

from_date=datetime(2020,1,1)
to_date=datetime(2023,8,1)
lists=[]
#if not mt5.initialize(Path=base_path):
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()
for k in range (len(usuario)):
    authorized=mt5.login(usuario[k],password[k],servidor[k])
    if authorized:
        account_info=mt5.account_info()

        if account_info!=None:

             # Obtener depositos y retiros 
            arrayDeposit=[]                  
            deposits = mt5.history_deals_get(from_date, to_date, group="*,**")
            if deposits == None:
                print("No deals, error code={}".format(mt5.last_error()))
            elif len(deposits) > 0:
                for deposit in deposits:
                    if deposit.price ==0 :
                        dateDep = time.ctime(deposit.time)
                        arrayDeposit = arrayDeposit + [{
                            "ticket-deposits-withdraw": deposit.ticket,
                            "date-deposits-withdraw":dateDep,
                            "deposits-withdraw": deposit.profit,
                            "type":deposit.type
                        }]



            # Obtener volumen transacciones cerradas   
            closeOperations=[]
            dateClosedVolume=[]
            volumeClosedOrders = mt5.history_deals_get(from_date, to_date, group="*,**")
            if volumeClosedOrders == None:
                print("No deals, error code={}".format(mt5.last_error()))
            elif len(volumeClosedOrders) > 0:
                for volumeClosedOrder in volumeClosedOrders:
                    if volumeClosedOrder.profit !=0 and volumeClosedOrder.position_id!=0:
                        DateTrade = time.ctime(volumeClosedOrder.time)
                        dateClosedVolume = dateClosedVolume + [DateTrade] 
                        closeOperations = closeOperations + [{
                        "date-closed-trade":DateTrade, 
                        "ticket-close-trade":volumeClosedOrder.ticket,
                        "profit-close":volumeClosedOrder.profit,
                        "volumen-closed":volumeClosedOrder.volume,
                        "symbol":volumeClosedOrder.symbol,
                        "type": volumeClosedOrder.type
                        }]

            # Obtener transacciones abiertas 
            openOperations=[]
            dateOpenProfit=[]
            openProfits = mt5.positions_get(group="*,**")
            if openProfits == None:
                print("No deals, error code={}".format(mt5.last_error()))
            elif len(openProfits) > 0:
                for openProfit in openProfits:
                    if openProfit.profit !=0:
                        DateTradeOpen = time.ctime(openProfit.time)
                        openOperations=openOperations + [{
                        "date-open-trade":DateTradeOpen, 
                        "ticket-open-trade":openProfit.ticket,
                        "profit-open":openProfit.profit,
                        "volumen-open":openProfit.volume,
                        "symbol":openProfit.symbol,
                        "type":openProfit.type
                        }] 
    
            list={}   
            
            list = {"Usuario":usuario[k],
                    "Balance":account_info.balance,
                    "Equidad":account_info.equity,
                    "Deposits-withdraw":arrayDeposit,
                    "open-operations": openOperations,
                    "closed-operations":closeOperations
                    }
            lists.append(list)

            
            # mostramos los datos sobre la cuenta comercial en forma de diccionario
    else:
        print("failed to connect to trade account ",usuario[k],"with password=",password[k], "error code =",mt5.last_error())

with open('data.json', 'w') as file:
    json.dump(lists, file, indent=4)

# finalizamos la conexión con el terminal MetaTrader 5
mt5.shutdown()



