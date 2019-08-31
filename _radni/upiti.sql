SQLCommand = "CREATE TABLE public.gs_of_bbox_mreza (id integer, bbox character varying(64), datum timestamp with time zone, dl smallint, min_x double precision, min_y double precision, max_x double precision, max_y double precision, koord_sistem character varying(64), mergelist smallint, mi_style character varying(254), mi_prinx serial NOT NULL, sp_geometry geometry(Geometry,32634), CONSTRAINT gs_of_bbox_mreza_pkey PRIMARY KEY (mi_prinx)) WITH (OIDS=FALSE)"
cursor.execute(SQLCommand)
cursor.commit()

SQLCommand = "ALTER TABLE public.gs_of_bbox_mreza OWNER TO postgres"
cursor.execute(SQLCommand)
cursor.commit()

SQLCommand = "CREATE INDEX spindex_gs_of_bbox_mreza_sp_geometry ON public.gs_of_bbox_mreza USING gist (sp_geometry)"
cursor.execute(SQLCommand)
cursor.commit()
