# Conclusiones EDA y ETL

## Empresas constituidas:

       consta de 16720 y 6 columnas:

0   id_const ->
        - Es el Id de la tabla un int autoincremental 
        - Int

 1   territorio ->
        - Nombra las 19 comunidades autonomas
        - String

 2   id_tiempo -> 
        - Muestra aÃ±o y mes, el mes en digito de 2 numeros, AAAAMM
        - Int 

 3   tipo ->
        -Muestra tipo de empresas :
                Mercantiles, es la suma de Sociedad anÃ³nima y Sociedad Limitada 
                Sociedades anÃ³nimas,
                Sociedades de responsabilidad limitada,
                S. Comanditarias y S. Colectivas.
        -String
        -CategÃ³rica con 4 opciones 
        - Cada categorÃ­a tienen 4180 filas, la razÃ³n que los valores totales coinciden es porque hay una fila por fecha, independientemente si hay disueltas o no.


 4   numero_sociedades ->
        -Muestra el numero de sociedades creadas
        -Int

 5   capital ->
        -Capital con el que se constituye la empresas
        -Int



## Empresas disueltas:

       consta de 12539 y 5 columnas

0   id_dis ->
        - Es el Id de la tabla un int autoincremental 
        - Int

1   territorio ->
        - Nombra las 19 comunidades autonomas
        - String


2   id_tiempo  ->     
       - Se representa aÃ±o y mes , este siempre con dos cifras , es decir ,AAAAMM
       - int
      

 3   razon ->
       - corresponde al motivo de la disolucion de las empresas, categorica:
              Voluntaria    4180
              Por fusiÃ³n    4180
              Otras         4180
       * en la api , a la hora de la llamada, existe un motivo mas, Total, que se elimina de la llamada ya que solo es una suma de las demÃ¡s y da nÃºmeros falseados

        - Cada categorÃ­a tienen 4180 filas, la razÃ³n que los valores totales coinciden es porque hay una fila por fecha, independientemente si hay disueltas o no.

       -str  

 4   numero_sociedades->
       -cantidad de numero de sociedades disueltas
       -int

       
## Sectores IPC:

  consta de 14 y 2 columnas

0   id_sector ->
       - Es el Id que representa la actividad economica
                      1,Ãndice general
                     2,Alimentos y bebidas no alcohÃ³licas
                     3,Bebidas alcohÃ³licas y tabaco
                     4,Vestido y calzado
                     5,"Vivienda, agua, electricidad, gas y otros combustibles"
                     6,"Muebles, artÃ­culos del hogar y artÃ­culos para el mantenimiento corriente del hogar"
                     7,Sanidad
                     8,Transporte
                     9,InformaciÃ³n y comunicaciones
                     10,"Actividades recreativas, deporte y cultura"
                     11,EnseÃ±anza
                     12,Restaurantes y servicios de alojamiento
                     13,Seguros y servicios financieros
                     14,"Cuidado personal, protecciÃ³n social, y bienes y servicios diversos"

       - Int
    

1   Nombre ->
       - Nombre del sector economico
       - String


## Territorio:

  consta de 20 y 2 columnas

0   id_sector ->
       - Es el Id que representa numero con el que representamos cada comunidad autonoma, ademas del 1 que es nacional
                            1,Nacional
                            2,AndalucÃ­a
                            3,AragÃ³n
                            4,"Asturias, Principado de"
                            5,"Balears, Illes"
                            6,Canarias
                            7,Cantabria
                            8,Castilla y LeÃ³n
                            9,Castilla - La Mancha
                            10,CataluÃ±a
                            11,Comunitat Valenciana
                            12,Extremadura
                            13,Galicia
                            14,"Madrid, Comunidad de"
                            15,"Murcia, RegiÃ³n de"
                            16,"Navarra, Comunidad Foral de"
                            17,PaÃ­s Vasco
                            18,"Rioja, La"
                            19,Ceuta
                            20,Melilla

       - Int
    

1   Nombre ->
       - Nombre de cada comunidad autonoma , mas el total del computo que es nacional 
       - String


## TIEMPO:

  consta de 294 y 4 columnas
       Representa el periodo de tiempo


 0   id_tiempo->  
       - Es el Id de la tabla un int autoincremental 
       - Int
      
 1   anio ->
       - int
       - AAAA
 2   mes->
       -int
       - MM
 3   nombre_mes->   
       -str 
       -Nombre del mes



## TIPO MEDIDA:
       consta de 4 filas y 2 columnas

 0   id_tipo_medida->  
       - Es el Id de la tabla un int autoincremental ,
       - Int

1   nombre_medida->   
       -str 
       -categorica que representa el tiempo de la comparativa

              Ãndice
              VariaciÃ³n mensual
              VariaciÃ³n anual
              VariaciÃ³n en lo que va de aÃ±o


## IPC:

  consta de 311752 y 5 columnas

0   id_tiempo s ->
       - Es el Id de la tabla un int autoincremental 
       - Int
       - FK tiempo

1   id_territorio ->
       - el id del territorio que nombra las 19 comunidades autonomas
       - Int
       - FK territorio


2   id_sector    ->     
       -Es el Id de la tabla un int autoincremental que representa sector economico de la actividad
       - int
       - FK sectores_ipc
      

 3   Id_medida->
       - el id del tipo de medida, categorica con 4 categorias:
                     1,Ãndice
                     2,VariaciÃ³n mensual
                     3,VariaciÃ³n anual
                     4,VariaciÃ³n en lo que va de aÃ±o
            - Int
            - FK territoriotipo_medida

 4   numero_sociedades->
       -cantidad de numero de sociedades disueltas
       -int




## TRANSFORMACIONES:

1.     TRANS_STRING->

    pasamos id's, id_cons, id_tiempo  a string ya que no son matemÃ¡ticas para hacer operaciones y 
    tiene mas sentido que las trate como categÃ³rico
    vamos a cambiar topo de columna string y hacemos funcion en un en punto py. (trans_str) src/transformation

            df_empr_const =id_constutias y id_tiempo 
            df_empr_dis = id_dis, id_tiempo
            df_ipc =id_tiempo,id_territorio,id_sector,id_medida
            df_sectores_ipc = id_sector
            df_territorio = id_territorio
            df_tiempo = id_tiempo, anyo, mes
            df_tipo_medida = id_medida

2.     Normalizacion en texto->
    cambiar nombre comunidades, cambiar orden, sin acento, con minuscula y separacion con guion bajo 
    lo hacemos en un replace , funcion en .py (trans_normal) src/transformation

        empresas constituidas - territorio 
        empresas disueltas - territorio
        territorio nombre - territorio 




3.  Eliminar Tipo ['Mercantil']->
    es la suma del resto de categorias y daria falsos resultados , con ello eliminamos 4180 filas


4.     sustituimos el nombre de tipo de empresa->

    Sociedad Limitada por las siglas --> S.L., 
    Sociedad Anonima -->S.A. 
    S. comanditarias y s. Colectivas -->S.Com/S.C.

5.     poner el nombre de las comunidades todos en castellano


6.     Guardados nuevos CSV transformados en files/data_processed

7.     Creamos base de datos con SQLAlchemy , llamÃ¡ndolo desde un .py (load.py)

8.     Creamos .env con los datos y las claves para acceder a MySQL desde Python (no se puede observar puesto que esta en GitIgnore)
       * para que la base de datos funcione debe crear un doc .env con esta base:

       DB_HOST=localhost
       DB_PORT=3306
       DB_USER=tu_usuario
       DB_PASSWORD=tu_contraseÃ±a
       DB_NAME=nombre_de_tu_base_de_datos


9.  Crear un GitIgnore para proteger los datos sensibles, metiendo en este el archivo .env
