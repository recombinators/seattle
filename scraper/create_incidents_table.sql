CREATE TABLE incidents
(
  gid serial NOT NULL,
  units character varying(1000),
  date_time character varying(50),
  incident_type character varying(50),
  address character varying(1000),
  incident_number character varying(50),
  latitude character varying(50),
  longitude character varying(50),
  the_geom geometry,
  CONSTRAINT incidents_pkey PRIMARY KEY (gid),
  CONSTRAINT enforce_dims_the_geom CHECK (st_ndims(the_geom) = 2),
  CONSTRAINT enforce_geotype_geom CHECK (geometrytype(the_geom) = 'POINT'::text OR the_geom IS NULL),
  CONSTRAINT enforce_srid_the_geom CHECK (st_srid(the_geom) = 4326)
);
 
-- Index: incidents_the_geom_gist
 
-- DROP INDEX incidents_the_geom_gist;
 
CREATE INDEX incidents_the_geom_gist
  ON incidents
  USING gist
  (the_geom );


-- units,date,type,location,incident_number,latitude,longitude
