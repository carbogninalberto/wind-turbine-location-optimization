-- tutte le citta'
select * from city;

-- tutti gli id
select wsid from wind as w group by w.wsid ;

-- join delle due tabelle
select w.wsid, c.city from wind as w join city as c on c.wsid = w.wsid group by w.wsid, c.city;

-- numero di record per la stazione 305
select COUNT(*) from wind where wsid = 305;

-- tutti i valori m/s maggiori di 11 m/s per l'id 305
select * from wind where wsid = 305 and wdsp != '' and (cast(wdsp as float)) > 11.0;

-- tutti i valori m/s maggiori di 11 m/s su 9mln di records!! in ordine decrescente
select * from wind where wdsp != '' and (cast(wdsp as float)) > 11.0 order by (cast(wdsp as float)) desc;

-- numero di righe nel db
select COUNT(*) from wind;

--cancella la tabella commentato per sicurezza
--delete from wind where 1=1;