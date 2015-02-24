CREATE TABLE incidents
(
  gid serial NOT NULL,
  address character varying(100),
  type character varying(100),
  datetime character varying(100),
  latitude character varying(100),
  longitude character varying(100),
  reportlocation character varying(100),
  incident character varying(100),
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


-- Address,Type,Datetime,Latitude,Longitude,Report Location,Incident Number
