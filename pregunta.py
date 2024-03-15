"""
Limpieza de datos usando Pandas
-----------------------------------------------------------------------------------------

Realice la limpieza del dataframe. Los tests evaluan si la limpieza fue realizada 
correctamente. Tenga en cuenta datos faltantes y duplicados.

"""
import pandas as pd
#import unidecode


def clean_data():
    df = pd.read_csv("solicitudes_credito.csv", sep=";")
    
    # Eliminar columna 0
    df = df.drop(df.columns[0], axis=1)

    # # #Eliminar acentos y tildes en strings usando unidecode
    # df = df.map(lambda x: unidecode.unidecode(x) if type(x) == str else x)

    #Transformar todos los strings a minúsculas
    df = df.apply(lambda x: x.str.lower() if x.dtype == "object" else x)

    # # #Eliminar espacios al inicio y al final de las strings
    # df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    #Cambiar guiones y guiones bajos por espacios
    df =df.replace({'-':' ', '_':' '}, regex=True)

    # Convertir montos de credito a float
    df.monto_del_credito = df.monto_del_credito.str.strip(" ")
    df.monto_del_credito = df.monto_del_credito.replace('[\,$]|(\.00$)', '', regex=True).astype(float)

    # Convertir comuna_ciudadano a int
    df.comuna_ciudadano = df.comuna_ciudadano.astype(int)

    # Las fechas de fecha_de_beneficio tienen un formato desordenado, se ordenan de la siguiente manera: año-mes-día
    df["fecha_de_beneficio"] = pd.to_datetime(
        df["fecha_de_beneficio"], format="%d/%m/%Y", errors="coerce"
    ).fillna(
        pd.to_datetime(df["fecha_de_beneficio"], format="%Y/%m/%d", errors="coerce")
    )
    df.fecha_de_beneficio=df.fecha_de_beneficio.dt.strftime('%Y-%m-%d')

    # # #Se aprecia que hay barrios con el caracter "?", que significa que hay caracteres especiales como tildes o ñ
    # # #Se crea una lista con los barrios que contienen "?"
    # barrios_con_tilde = df[df['barrio'].str.contains("?",regex=False,na=False)]['barrio'].unique()
    # # #Esto arroja como resultado ['bel?n, 'antonio nari?o]
    # # #Se procede a reemplazar 'bel?n por belen y 'antonio nari?o por antonio narino
    # df.barrio = df.barrio.str.replace("bel?n", "belen")
    # df.barrio = df.barrio.str.replace("antonio nari?o", "antonio narino")

    #Eliminar datos nulos
    df = df.dropna()

    #Eliminar duplicados
    df = df.drop_duplicates()

    return df