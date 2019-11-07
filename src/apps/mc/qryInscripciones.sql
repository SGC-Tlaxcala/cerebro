SELECT
       extract(year from c.fecha_tramite) as yyyy,

       COUNT(c.folio)
FROM cecyrd_tramites c
WHERE
      c.movimiento_definitivo LIKE 'INSCRIP%'
GROUP BY 1

