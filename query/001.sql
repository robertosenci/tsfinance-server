CREATE DATABASE tsfinance
    WITH
    OWNER = postgres
    TEMPLATE = template0
    ENCODING = 'LATIN1'
    LC_COLLATE = 'C'
    LC_CTYPE = 'C'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;


CREATE TABLE public."CAD_USUARIO" (
  id_usuario SERIAL NOT NULL,
  ds_nome VARCHAR(50) NOT NULL,
  ds_email VARCHAR(255) NOT NULL,
  ds_senha VARCHAR(255) NOT NULL,
  nr_phone VARCHAR(20) NOT NULL,
  dt_nascimento DATE,
  nr_cpf VARCHAR(14) NOT NULL,
  tp_perfil VARCHAR(1) DEFAULT 'S' NOT NULL,
  sn_ativo BOOLEAN DEFAULT true NOT NULL,
  sn_excluido BOOLEAN DEFAULT false NOT NULL,
  PRIMARY KEY(id_usuario)
) WITH (oids = false);
