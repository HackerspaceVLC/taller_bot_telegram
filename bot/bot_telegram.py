import api
import private
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler, filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): #Función asincrona para gestiona el comando de bot /start
    usuario= update.message.from_user
    await context.bot.send_message(chat_id=update.effective_chat.id, 
            text=f"Hola {usuario.first_name}, para saber la predicción en una población manda /predict seguido de la población (primera letra en mayúsculas, ej. Valencia)")

async def prediccion_municipio(update: Update, context: ContextTypes.DEFAULT_TYPE): #Función asincrona que gestiona el comando de bot /predict
    #Obtenemos el nombre de la población que ha sido enviado en el mensaje tras el /predict
    poblacion=context.args[0]

    #Obtenemos el array con todas las poblaciones que coinciden con la que nos ha enviado 
    # el usuario tras el /predict
    lista_poblaciones=api.seleccionar_municipio(poblacion)
    
    if len(lista_poblaciones)==0: #No hay ninguna población con ese nombre
        mensaje=f"Introduce otra población ya que '{poblacion}' no existe en la BD de AEMET"
    if len(lista_poblaciones)==1: #Solo hay una población en la BD de AEMET con ese nombre
        mensaje=api.prediccion(poblacion)
    if len(lista_poblaciones)>1: #Hay varias poblaciones con el mismo nombre
        # Esta parte no está programada, ¿te atreves?
        mensaje=f"Ups, parece que hay más de una población con el nombre '{poblacion}' y esta parte no está programada. ¿Te atreves a intentarlo?"
   
    await context.bot.send_message(chat_id=update.effective_chat.id, text=mensaje) #Mandamos el mensaje al usuario

if __name__ == '__main__':
    application = ApplicationBuilder().token(private.TOKEN_TELEGRAM).build()
    #/START
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler) 
    #/PREDICT
    predict_handler = CommandHandler('predict', prediccion_municipio)
    application.add_handler(predict_handler)
    
    application.run_polling()


    