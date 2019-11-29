-- create table cities
create table city (
	wsid INTEGER PRIMARY KEY NOT NULL,
	wsnm VARCHAR(255) NOT NULL,
	elvt VARCHAR(10) NOT NULL,
	lat VARCHAR(20) NOT NULL,
	lon VARCHAR(20) NOT NULL,
	inme VARCHAR(4) NOT NULL,
	city VARCHAR(255) NOT NULL,
	prov VARCHAR(2) NOT NULL	
);
-- create table wind
create table wind (
	wsid INTEGER NOT NULL,
	date VARCHAR(10) NOT NULL,
	hr VARCHAR(2) NOT NULL,
	stp VARCHAR(20) NOT NULL,
	temp VARCHAR(20) NOT NULL,
	wdsp VARCHAR(20) NOT NULL,
  	PRIMARY KEY (wsid,date,hr),
  	FOREIGN KEY (wsid) REFERENCES city(wsid)
);