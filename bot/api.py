from aemet import Aemet, Municipio
import private

aemet_client = Aemet(private.API_KEY_AEMET)

def seleccionar_municipio(nombre_municipio): #Entrada: municipio; Salida: array con los municipios que contienen dicho nombre
    lista_municipios=Municipio.buscar(nombre_municipio)
    return lista_municipios

def obtener_codigo_municipio(nombre_municipio): #Le paso un municipio y devuelve el código de AEMET
    municipios=seleccionar_municipio(nombre_municipio)
    return municipios[0].cpro+municipios[0].cmun

def componer_mensaje_prediccion(prediccion): #Construye el mensaje a mandar a partir un array con los datos meteorológicos
    mensaje=""
    for i in range(7):
        mensaje=mensaje + f"Día: {prediccion[0][i]} - Mín: {prediccion[2][i]:2.0f}ºC - \
            Máx: {prediccion[1][i]:2.0f}ºC - Prob.Prec.: {prediccion[3][i]:2.0f}% - Cielo: {prediccion[4][i]}\n"
    return mensaje

def prediccion(nombre_municipio): #Le paso el municipio y me devuelve el mensaje a enviar al usuario
    cod_municipio=obtener_codigo_municipio(nombre_municipio)
    prediccion=aemet_client.get_prediccion(codigo_municipio=cod_municipio, periodo='PERIODO_SEMANA',raw=True)
    dias=[]
    temperaturas_maximas=[]
    temperaturas_minimas=[]
    probabilidades_precipitacion=[]
    estados_cielo=[]
    for i in range(7):
        dias.append(prediccion['prediccion']['dia'][i]['fecha'][8:10])
        temperaturas_maximas.append(prediccion['prediccion']['dia'][i]['temperatura']['maxima'])
        temperaturas_minimas.append(prediccion['prediccion']['dia'][i]['temperatura']['minima'])
        probabilidades_precipitacion.append(prediccion['prediccion']['dia'][i]['probPrecipitacion'][0]['value'])
        estados_cielo.append(prediccion['prediccion']['dia'][i]['estadoCielo'][0]['descripcion'])
    resultado=[dias, temperaturas_maximas, temperaturas_minimas, probabilidades_precipitacion, estados_cielo]
    mensaje = componer_mensaje_prediccion(resultado)
    return mensaje

