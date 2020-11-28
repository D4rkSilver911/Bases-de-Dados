BEGIN;
--
-- Create model equipa
--
CREATE TABLE "projeto_equipa" ("nome" varchar(512) NOT NULL PRIMARY KEY, "isfull" boolean NOT NULL, "n_jogadores" integer NOT NULL);
--
-- Create model utilizador
--
CREATE TABLE "projeto_utilizador" ("cc" varchar(512) NOT NULL PRIMARY KEY, "username" varchar(512) NOT NULL UNIQUE, "password" varchar(512) NOT NULL, "nome" varchar(512) NOT NULL, "apelido" varchar(512) NOT NULL, "email" varchar(254) NOT NULL UNIQUE, "isadmin" boolean NOT NULL, "contacto" integer NOT NULL UNIQUE, "n_vitorias" integer NULL, "saldo" numeric(8, 2) NOT NULL, "dinheiroGasto" numeric(8, 2) NOT NULL, "pagamentosRegularizados" boolean NOT NULL, "posicao_preferida" text NULL, "bio" text NULL, "isgestor" boolean NOT NULL, "isOnline" boolean NOT NULL, "pedidoSubs" boolean NOT NULL);
--
-- Create model torneio
--
CREATE TABLE "projeto_torneio" ("nome" varchar(512) NOT NULL PRIMARY KEY, "data_inicio" date NOT NULL, "data_fim" date NOT NULL, "dias" varchar(512) NOT NULL, "hora_inicio" varchar(512) NOT NULL, "campos" varchar(512) NOT NULL, "dia_sem_jogo" date NOT NULL, "n_jogos" integer NOT NULL, "gestor_utilizador_cc_id" varchar(512) NOT NULL);
--
-- Create model substituicao
--
CREATE TABLE "projeto_substituicao" ("id" serial NOT NULL PRIMARY KEY, "equipaDest" varchar(512) NOT NULL, "duracao" integer NOT NULL, "deUser_id" varchar(512) NOT NULL, "paraUser_id" varchar(512) NOT NULL);
--
-- Create model reserva_torneio
--
CREATE TABLE "projeto_reserva_torneio" ("id" serial NOT NULL PRIMARY KEY, "posicao" varchar(512) NOT NULL, "pedidoSubs" boolean NOT NULL, "cc_id" varchar(512) NOT NULL, "torneio_id" varchar(512) NOT NULL);
--
-- Create model notificacao
--
CREATE TABLE "projeto_notificacao" ("id" serial NOT NULL PRIMARY KEY, "texto" varchar(512) NOT NULL, "nome_equipa_a_id" varchar(512) NOT NULL, "nome_equipa_b_id" varchar(512) NOT NULL, "nome_torneio_id" varchar(512) NOT NULL);
--
-- Create model movimentos
--
CREATE TABLE "projeto_movimentos" ("id" serial NOT NULL PRIMARY KEY, "ano" integer NOT NULL, "pago" text NULL, "montante" integer NULL, "cc_id" varchar(512) NOT NULL);
--
-- Create model jogo
--
CREATE TABLE "projeto_jogo" ("id" serial NOT NULL PRIMARY KEY, "data_inicio" date NOT NULL, "golos_equipa_a" integer NULL, "golos_equipa_b" integer NULL, "campo" varchar(512) NOT NULL, "nome_equipa_a_id" varchar(512) NOT NULL, "nome_equipa_b_id" varchar(512) NOT NULL, "nome_torneio_id" varchar(512) NOT NULL);
--
-- Create model jogador_equipa
--
CREATE TABLE "projeto_jogador_equipa" ("id" serial NOT NULL PRIMARY KEY, "posicao" varchar(512) NOT NULL, "estatuto" text NOT NULL, "equipa_nome_id" varchar(512) NOT NULL, "jogador_utilizador_cc_id" varchar(512) NOT NULL);
--
-- Create model jogador
--
CREATE TABLE "projeto_jogador" ("id" serial NOT NULL PRIMARY KEY, "estatuto" text NULL, "iscaptain" boolean NOT NULL, "utilizador_cc_id" varchar(512) NOT NULL);
--
-- Add field jogador_utilizador_cc to equipa
--
ALTER TABLE "projeto_equipa" ADD COLUMN "jogador_utilizador_cc_id" varchar(512) DEFAULT '' NOT NULL REFERENCES "projeto_utilizador"("cc") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "projeto_equipa" ALTER COLUMN "jogador_utilizador_cc_id" DROP DEFAULT;
--
-- Add field torneio_nome to equipa
--
ALTER TABLE "projeto_equipa" ADD COLUMN "torneio_nome_id" varchar(512) NOT NULL REFERENCES "projeto_torneio"("nome") DEFERRABLE INITIALLY DEFERRED;
--
-- Create model classificacao
--
CREATE TABLE "projeto_classificacao" ("id" serial NOT NULL PRIMARY KEY, "cPontos" integer NOT NULL, "cMarcados" integer NOT NULL, "cSofridos" integer NOT NULL, "cEquipa_id" varchar(512) NOT NULL, "cTorneio_id" varchar(512) NOT NULL);
CREATE INDEX "projeto_equipa_nome_0e1d1fbf_like" ON "projeto_equipa" ("nome" varchar_pattern_ops);
CREATE INDEX "projeto_utilizador_cc_85983e01_like" ON "projeto_utilizador" ("cc" varchar_pattern_ops);
CREATE INDEX "projeto_utilizador_username_a4dff12f_like" ON "projeto_utilizador" ("username" varchar_pattern_ops);
CREATE INDEX "projeto_utilizador_email_54a69e13_like" ON "projeto_utilizador" ("email" varchar_pattern_ops);
ALTER TABLE "projeto_torneio" ADD CONSTRAINT "projeto_torneio_gestor_utilizador_cc_a7ee40bf_fk_projeto_u" FOREIGN KEY ("gestor_utilizador_cc_id") REFERENCES "projeto_utilizador" ("cc") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "projeto_torneio_nome_78487801_like" ON "projeto_torneio" ("nome" varchar_pattern_ops);
CREATE INDEX "projeto_torneio_gestor_utilizador_cc_id_a7ee40bf" ON "projeto_torneio" ("gestor_utilizador_cc_id");
CREATE INDEX "projeto_torneio_gestor_utilizador_cc_id_a7ee40bf_like" ON "projeto_torneio" ("gestor_utilizador_cc_id" varchar_pattern_ops);
ALTER TABLE "projeto_substituicao" ADD CONSTRAINT "projeto_substituicao_deUser_id_e9216af7_fk_projeto_u" FOREIGN KEY ("deUser_id") REFERENCES "projeto_utilizador" ("cc") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "projeto_substituicao" ADD CONSTRAINT "projeto_substituicao_paraUser_id_fdd9913b_fk_projeto_u" FOREIGN KEY ("paraUser_id") REFERENCES "projeto_utilizador" ("cc") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "projeto_substituicao_deUser_id_e9216af7" ON "projeto_substituicao" ("deUser_id");
CREATE INDEX "projeto_substituicao_deUser_id_e9216af7_like" ON "projeto_substituicao" ("deUser_id" varchar_pattern_ops);
CREATE INDEX "projeto_substituicao_paraUser_id_fdd9913b" ON "projeto_substituicao" ("paraUser_id");
CREATE INDEX "projeto_substituicao_paraUser_id_fdd9913b_like" ON "projeto_substituicao" ("paraUser_id" varchar_pattern_ops);
ALTER TABLE "projeto_reserva_torneio" ADD CONSTRAINT "projeto_reserva_torneio_cc_id_82e8b1d8_fk_projeto_utilizador_cc" FOREIGN KEY ("cc_id") REFERENCES "projeto_utilizador" ("cc") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "projeto_reserva_torneio" ADD CONSTRAINT "projeto_reserva_torn_torneio_id_46c1300a_fk_projeto_t" FOREIGN KEY ("torneio_id") REFERENCES "projeto_torneio" ("nome") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "projeto_reserva_torneio_cc_id_82e8b1d8" ON "projeto_reserva_torneio" ("cc_id");
CREATE INDEX "projeto_reserva_torneio_cc_id_82e8b1d8_like" ON "projeto_reserva_torneio" ("cc_id" varchar_pattern_ops);
CREATE INDEX "projeto_reserva_torneio_torneio_id_46c1300a" ON "projeto_reserva_torneio" ("torneio_id");
CREATE INDEX "projeto_reserva_torneio_torneio_id_46c1300a_like" ON "projeto_reserva_torneio" ("torneio_id" varchar_pattern_ops);
ALTER TABLE "projeto_notificacao" ADD CONSTRAINT "projeto_notificacao_nome_equipa_a_id_0d2eb3f7_fk_projeto_e" FOREIGN KEY ("nome_equipa_a_id") REFERENCES "projeto_equipa" ("nome") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "projeto_notificacao" ADD CONSTRAINT "projeto_notificacao_nome_equipa_b_id_d92ecf46_fk_projeto_e" FOREIGN KEY ("nome_equipa_b_id") REFERENCES "projeto_equipa" ("nome") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "projeto_notificacao" ADD CONSTRAINT "projeto_notificacao_nome_torneio_id_4703db4f_fk_projeto_t" FOREIGN KEY ("nome_torneio_id") REFERENCES "projeto_torneio" ("nome") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "projeto_notificacao_nome_equipa_a_id_0d2eb3f7" ON "projeto_notificacao" ("nome_equipa_a_id");
CREATE INDEX "projeto_notificacao_nome_equipa_a_id_0d2eb3f7_like" ON "projeto_notificacao" ("nome_equipa_a_id" varchar_pattern_ops);
CREATE INDEX "projeto_notificacao_nome_equipa_b_id_d92ecf46" ON "projeto_notificacao" ("nome_equipa_b_id");
CREATE INDEX "projeto_notificacao_nome_equipa_b_id_d92ecf46_like" ON "projeto_notificacao" ("nome_equipa_b_id" varchar_pattern_ops);
CREATE INDEX "projeto_notificacao_nome_torneio_id_4703db4f" ON "projeto_notificacao" ("nome_torneio_id");
CREATE INDEX "projeto_notificacao_nome_torneio_id_4703db4f_like" ON "projeto_notificacao" ("nome_torneio_id" varchar_pattern_ops);
ALTER TABLE "projeto_movimentos" ADD CONSTRAINT "projeto_movimentos_cc_id_3d21a70b_fk_projeto_utilizador_cc" FOREIGN KEY ("cc_id") REFERENCES "projeto_utilizador" ("cc") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "projeto_movimentos_cc_id_3d21a70b" ON "projeto_movimentos" ("cc_id");
CREATE INDEX "projeto_movimentos_cc_id_3d21a70b_like" ON "projeto_movimentos" ("cc_id" varchar_pattern_ops);
ALTER TABLE "projeto_jogo" ADD CONSTRAINT "projeto_jogo_nome_equipa_a_id_e9b54093_fk_projeto_equipa_nome" FOREIGN KEY ("nome_equipa_a_id") REFERENCES "projeto_equipa" ("nome") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "projeto_jogo" ADD CONSTRAINT "projeto_jogo_nome_equipa_b_id_b6521287_fk_projeto_equipa_nome" FOREIGN KEY ("nome_equipa_b_id") REFERENCES "projeto_equipa" ("nome") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "projeto_jogo" ADD CONSTRAINT "projeto_jogo_nome_torneio_id_0e4be767_fk_projeto_torneio_nome" FOREIGN KEY ("nome_torneio_id") REFERENCES "projeto_torneio" ("nome") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "projeto_jogo_nome_equipa_a_id_e9b54093" ON "projeto_jogo" ("nome_equipa_a_id");
CREATE INDEX "projeto_jogo_nome_equipa_a_id_e9b54093_like" ON "projeto_jogo" ("nome_equipa_a_id" varchar_pattern_ops);
CREATE INDEX "projeto_jogo_nome_equipa_b_id_b6521287" ON "projeto_jogo" ("nome_equipa_b_id");
CREATE INDEX "projeto_jogo_nome_equipa_b_id_b6521287_like" ON "projeto_jogo" ("nome_equipa_b_id" varchar_pattern_ops);
CREATE INDEX "projeto_jogo_nome_torneio_id_0e4be767" ON "projeto_jogo" ("nome_torneio_id");
CREATE INDEX "projeto_jogo_nome_torneio_id_0e4be767_like" ON "projeto_jogo" ("nome_torneio_id" varchar_pattern_ops);
ALTER TABLE "projeto_jogador_equipa" ADD CONSTRAINT "projeto_jogador_equi_equipa_nome_id_b912dd95_fk_projeto_e" FOREIGN KEY ("equipa_nome_id") REFERENCES "projeto_equipa" ("nome") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "projeto_jogador_equipa" ADD CONSTRAINT "projeto_jogador_equi_jogador_utilizador_c_4b1e3466_fk_projeto_u" FOREIGN KEY ("jogador_utilizador_cc_id") REFERENCES "projeto_utilizador" ("cc") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "projeto_jogador_equipa_equipa_nome_id_b912dd95" ON "projeto_jogador_equipa" ("equipa_nome_id");
CREATE INDEX "projeto_jogador_equipa_equipa_nome_id_b912dd95_like" ON "projeto_jogador_equipa" ("equipa_nome_id" varchar_pattern_ops);
CREATE INDEX "projeto_jogador_equipa_jogador_utilizador_cc_id_4b1e3466" ON "projeto_jogador_equipa" ("jogador_utilizador_cc_id");
CREATE INDEX "projeto_jogador_equipa_jogador_utilizador_cc_id_4b1e3466_like" ON "projeto_jogador_equipa" ("jogador_utilizador_cc_id" varchar_pattern_ops);
ALTER TABLE "projeto_jogador" ADD CONSTRAINT "projeto_jogador_utilizador_cc_id_fbef6b5f_fk_projeto_u" FOREIGN KEY ("utilizador_cc_id") REFERENCES "projeto_utilizador" ("cc") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "projeto_jogador_utilizador_cc_id_fbef6b5f" ON "projeto_jogador" ("utilizador_cc_id");
CREATE INDEX "projeto_jogador_utilizador_cc_id_fbef6b5f_like" ON "projeto_jogador" ("utilizador_cc_id" varchar_pattern_ops);
CREATE INDEX "projeto_equipa_jogador_utilizador_cc_id_f64d9a5f" ON "projeto_equipa" ("jogador_utilizador_cc_id");
CREATE INDEX "projeto_equipa_jogador_utilizador_cc_id_f64d9a5f_like" ON "projeto_equipa" ("jogador_utilizador_cc_id" varchar_pattern_ops);
CREATE INDEX "projeto_equipa_torneio_nome_id_439acc37" ON "projeto_equipa" ("torneio_nome_id");
CREATE INDEX "projeto_equipa_torneio_nome_id_439acc37_like" ON "projeto_equipa" ("torneio_nome_id" varchar_pattern_ops);
ALTER TABLE "projeto_classificacao" ADD CONSTRAINT "projeto_classificaca_cEquipa_id_451d9d00_fk_projeto_e" FOREIGN KEY ("cEquipa_id") REFERENCES "projeto_equipa" ("nome") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "projeto_classificacao" ADD CONSTRAINT "projeto_classificaca_cTorneio_id_5b937b93_fk_projeto_t" FOREIGN KEY ("cTorneio_id") REFERENCES "projeto_torneio" ("nome") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "projeto_classificacao_cEquipa_id_451d9d00" ON "projeto_classificacao" ("cEquipa_id");
CREATE INDEX "projeto_classificacao_cEquipa_id_451d9d00_like" ON "projeto_classificacao" ("cEquipa_id" varchar_pattern_ops);
CREATE INDEX "projeto_classificacao_cTorneio_id_5b937b93" ON "projeto_classificacao" ("cTorneio_id");
CREATE INDEX "projeto_classificacao_cTorneio_id_5b937b93_like" ON "projeto_classificacao" ("cTorneio_id" varchar_pattern_ops);
COMMIT;
