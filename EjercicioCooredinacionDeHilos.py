import threading

def preparacion(cond, paso):
    for i in range(5):
        with cond:
            cond.wait_for(lambda: paso[0] == 1)  #Espera su turno
            print(f"Preparación {i + 1} completada")
            paso[0] = 2  #Actualiza el estado para el paso de procesamiento
            cond.notify_all()  #Notifica a los otros hilos para que continuen

def procesamiento(cond, paso):
    for i in range(5):
        with cond:
            cond.wait_for(lambda: paso[0] == 2)  #Espera su turno
            print(f"Procesamiento {i + 1} completado")
            paso[0] = 3  #Actualiza el estado para el paso de empaque
            cond.notify_all()  #Notifica a los otros hilos para que continuen

def empaque(cond, paso):
    for i in range(5):
        with cond:
            cond.wait_for(lambda: paso[0] == 3)  #Espera su turno
            print(f"Empaque {i + 1} completado")
            paso[0] = 1  #Reinicia el estado para el paso depreparación
            cond.notify_all()  #Notifica a los otros hilos para que continuen

#Creamos una instancia de Condition para coordinar los hilos
cond = threading.Condition()
paso = [1]  #Lista para saber cual es el paso actual. 1. preparación, 2. procesamiento, 3. empaque

#Creamos los hilos
h1 = threading.Thread(target=preparacion, args=(cond, paso))
h2 = threading.Thread(target=procesamiento, args=(cond, paso))
h3 = threading.Thread(target=empaque, args=(cond, paso))

#Iniciamos los hilos
h1.start()
h2.start()
h3.start()

#Esperamos a que todos los hilos terminen
h1.join()
h2.join()
h3.join()