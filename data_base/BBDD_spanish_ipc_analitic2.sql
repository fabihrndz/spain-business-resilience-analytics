use ipc_analisis_empresarial;



-- ✅ 1) Query que nos informa de fechas maxima y minima que tenemos para estos datos.

SELECT 
    MIN(id_tiempo) AS fecha_minima, 
    MAX(id_tiempo) AS fecha_maxima 
FROM empresas_constituidas; -- enero de 2008 a abril de 2026



-- ✅ 2)Total empresas creadas , disueltas y total capital invertido en el total de tiempo

SELECT SUM(c.numero_sociedades) AS total_empresas_creadas,
(SELECT SUM(numero_sociedades) FROM empresas_disueltas) AS total_empresas_disuelta,
ROUND(SUM(c.capital) / 1000000, 2) AS total_capital_invertido_millones_euros
FROM empresas_constituidas c;



-- ✅ 3) 10 años que mas empresas se crearon
SELECT  
    LEFT(id_tiempo, 4) AS anio, 
    SUM(numero_sociedades) AS total_empresas_creadas
FROM empresas_constituidas
GROUP BY anio
ORDER BY total_empresas_creadas DESC -- ordenado por numero de empresas creadas
LIMIT 10;



-- ✅ 4) 10 años que mas empresas se disolvieron y motivo

SELECT  
    LEFT(id_tiempo, 4) AS anio, 
    razon, 
    SUM(numero_sociedades) AS total_disueltas
FROM empresas_disueltas
GROUP BY anio,razon
ORDER BY total_disueltas DESC
LIMIT 10; -- 2025 (curiosamente igual que creadas) y por motivo Voluntario



--  ✅ 5)Cuantas empresas son disueltas por Año,Mes, Territorio; Razon Social, ipc mes actual, ipc 3 meses anteriores (lag), nº total empresas disueltas

SELECT t.anio,t.nombre_mes AS mes,
terr.nombre_territorio AS territorio,
sub.razon_disolucion,
sub.ipc_mes_actual,
-- PROMEDIO MÓVIL: Calcula la media del IPC del mes actual y los 2 meses anteriores
	ROUND(AVG(sub.ipc_mes_actual) OVER(
		PARTITION BY sub.id_territorio, sub.razon_disolucion 
		ORDER BY t.anio, t.mes 
		ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS ipc_tendencia_3meses, -- (lag 3 meses)
sub.total_empresas_disueltas
FROM (
		-- Subconsulta para limpiar y agrupar por mes, territorio y la RAZÓN del cierre
		SELECT d.id_tiempo,d.id_territorio,d.razon AS razon_disolucion,
			AVG(i.valor_ipc) AS ipc_mes_actual,
			SUM(d.numero_sociedades) AS total_empresas_disueltas

		FROM empresas_disueltas d

			JOIN ipc i ON d.id_tiempo = i.id_tiempo AND d.id_territorio = i.id_territorio
			WHERE i.id_medida = 1 -- Filtro para evitar duplicados de medida
			AND d.razon IS NOT NULL -- Evitamos filas vacías si las hay
			GROUP BY d.id_tiempo, d.id_territorio, d.razon
		) sub
		JOIN tiempo t ON sub.id_tiempo = t.id_tiempo
		JOIN territorio terr ON sub.id_territorio = terr.id_territorio
		ORDER BY t.anio DESC, t.mes DESC, terr.nombre_territorio, sub.total_empresas_disueltas DESC;
		 -- no es concluyente que el IPC sea la razon de la quiebra ya que el IPC no hace que una empresa cierre de forma inmediata



-- ✅ 6) Por Año, Mes  y Territorio ; ipc, empresas constituidas, empresas disueltas y % disolucion

WITH metricas_empresas AS (
SELECT c.id_tiempo,c.id_territorio,
	SUM(c.numero_sociedades) AS total_constituidas,
	SUM(d.numero_sociedades) AS total_disueltas

FROM empresas_constituidas c

LEFT JOIN empresas_disueltas d 
	ON c.id_tiempo = d.id_tiempo AND c.id_territorio = d.id_territorio
    
GROUP BY c.id_tiempo, c.id_territorio

)
			SELECT t.anio,t.nombre_mes AS mes,terr.nombre_territorio AS territorio,i.valor_ipc AS ipc_variacion, -- Ahora será único
					me.total_constituidas,me.total_disueltas,
				ROUND((me.total_disueltas / me.total_constituidas) * 100, 2) AS tanto_por_ciento_disolucion_empresas

				FROM metricas_empresas me
				JOIN tiempo t ON me.id_tiempo = t.id_tiempo
				JOIN territorio terr ON me.id_territorio = terr.id_territorio
				JOIN ipc i ON me.id_tiempo = i.id_tiempo AND me.id_territorio = i.id_territorio

			WHERE i.id_sector = 1      
			  AND i.id_medida = 1;     



 /* ✅ 7)  Esta query clasifica el IPC por rangos de impacto (Deflación, Estable, Moderada, Alta) 
 y te dice el promedio de empresas creadas y disueltas en cada escenario. 
 Ideal para ver bajo qué niveles de inflación sufre más el tejido empresarial.*/
 
 SELECT 
    resumen.escenario_inflacion,
    COUNT(DISTINCT resumen.id_tiempo) AS meses_en_este_escenario,
    ROUND(AVG(resumen.total_constituidas), 0) AS promedio_empresas_creadas,
    ROUND(AVG(resumen.total_disueltas), 0) AS promedio_empresas_disueltas,
    ROUND(AVG(resumen.total_constituidas) - AVG(resumen.total_disueltas), 0) AS balance_neto_promedio
FROM ( SELECT i.id_tiempo,i.id_territorio,
        -- ADAPTADO: Suponiendo que tus datos están expresados en base 100 (Ej: 102.5 = 2.5% inflación)
        CASE 
            WHEN i.valor_ipc < 100 THEN '1. Deflación / Bajada de precios'
            WHEN i.valor_ipc BETWEEN 100 AND 102.0 THEN '2. Inflación Estable (Objetivo)'
            WHEN i.valor_ipc BETWEEN 102.01 AND 105.0 THEN '3. Inflación Moderada-Alta'
            ELSE '4. Inflación Desbocada / Crisis'
        END AS escenario_inflacion,
        
        COALESCE((
            SELECT SUM(c.numero_sociedades) 
            FROM empresas_constituidas c 
            WHERE c.id_tiempo = i.id_tiempo AND c.id_territorio = i.id_territorio
        ), 0) AS total_constituidas,
        
        COALESCE((
            SELECT SUM(d.numero_sociedades) 
            FROM empresas_disueltas d 
            WHERE d.id_tiempo = i.id_tiempo AND d.id_territorio = i.id_territorio
        ), 0) AS total_disueltas
        
		FROM ipc i
		WHERE i.id_medida = 1 ) resumen
	GROUP BY resumen.escenario_inflacion
	ORDER BY resumen.escenario_inflacion;
/* nos llama la atencion que la inflaccion excesiva no es lo mas concluyente para la disoluccion de la empresa,
ya que cuando hay momento crisis con un IPC superior al 105 no es el dato mas alto para disolucion de empresas,
sino que cuando mas empresas se disuelve es en el momento de Infalccion estable o alta*/



-- ✅  8) Analisis capital invertido vs quiebras, teniendo en cuenta el IPC
/*Esta query analiza si en los meses con mayor variación de IPC el capital medio con el que se fundan las empresas disminuye (por incertidumbre económica)
 y si eso coincide con un mayor volumen de cierres empresariales en el mismo periodo.*/
 
SELECT t.anio, t.nombre_mes AS mes,
    -- 1. Promedio de IPC para este mes en concreto	
    (SELECT ROUND(AVG(i.valor_ipc), 2)
	FROM ipc i
	WHERE i.id_tiempo = t.id_tiempo AND i.id_medida = 1
    ) AS promedio_ipc,
		-- 2. Total de capital invertido en este mes
		COALESCE(resumen_empresas.total_capital, 0) AS total_capital_invertido,
		-- 3. Capital promedio por empresa constituida
		IF(resumen_empresas.total_constituidas > 0, 
		   ROUND(resumen_empresas.total_capital / resumen_empresas.total_constituidas, 2), 
		   0) AS capital_promedio_por_empresa,
		-- 4. Total de empresas disueltas en este mes
		COALESCE(resumen_empresas.total_disueltas, 0) AS total_disueltas
		FROM tiempo t
						JOIN (
							-- Agrupamos las métricas de empresas directamente por tiempo para que sea un proceso lineal rápido
							SELECT c.id_tiempo,
								SUM(c.capital) AS total_capital,
								SUM(c.numero_sociedades) AS total_constituidas,
								(
							SELECT SUM(d.numero_sociedades)
									FROM empresas_disueltas d
									WHERE d.id_tiempo = c.id_tiempo) AS total_disueltas
									FROM empresas_constituidas c
									GROUP BY c.id_tiempo) resumen_empresas ON t.id_tiempo = resumen_empresas.id_tiempo
						ORDER BY t.anio DESC, t.id_tiempo DESC;



--  ✅ 10) Minimo y maximo de cada año y mes y comunidad autonoma de ipc

SELECT t.anio,'MÁXIMO' AS tipo,
		t.nombre_mes AS mes,
		terr.nombre_territorio AS comunidad_autonoma,
		i.valor_ipc AS valor
FROM ipc i
		JOIN tiempo t ON i.id_tiempo = t.id_tiempo
		JOIN territorio terr ON i.id_territorio = terr.id_territorio
		-- Cruzamos directamente con los máximos ya precalculados por año
		JOIN (SELECT t2.anio, MAX(i2.valor_ipc) AS max_ipc
			FROM ipc i2
			JOIN tiempo t2 ON i2.id_tiempo = t2.id_tiempo
			WHERE i2.id_medida = 1
			GROUP BY t2.anio
		) mx ON t.anio = mx.anio AND i.valor_ipc = mx.max_ipc
		WHERE i.id_medida = 1
 UNION ALL
	SELECT t.anio,'MÍNIMO' AS tipo,
		t.nombre_mes AS mes,
		terr.nombre_territorio AS comunidad_autonoma,
		i.valor_ipc AS valor
	FROM ipc i
			JOIN tiempo t ON i.id_tiempo = t.id_tiempo
			JOIN territorio terr ON i.id_territorio = terr.id_territorio -- Cruzamos directamente con los mínimos ya precalculados por año
			JOIN (
				SELECT t3.anio, MIN(i3.valor_ipc) AS min_ipc
				FROM ipc i3
				JOIN tiempo t3 ON i3.id_tiempo = t3.id_tiempo
				WHERE i3.id_medida = 1
				GROUP BY t3.anio
				) mn ON t.anio = mn.anio AND i.valor_ipc = mn.min_ipc
WHERE i.id_medida = 1
ORDER BY anio DESC, tipo DESC;
