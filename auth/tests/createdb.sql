
DROP TABLE IF EXISTS user_account CASCADE;

DROP TYPE IF EXISTS tipo_funcao;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'tipo_funcao') THEN
        CREATE TYPE tipo_funcao AS ENUM (
            'MEDICO',
            'ESTAGIARIO',
            'PESQUISADOR',
            'ADMINISTRADOR'
        );
    END IF;
END $$;

-- Habilita a extensão pgcrypto (necessária para crypt() e gen_salt())
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Criação da tabela
CREATE TABLE IF NOT EXISTS user_account (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(30) UNIQUE NOT NULL,
    nome VARCHAR(100) NOT NULL,
    password_hash VARCHAR(100) NOT NULL,
    funcao tipo_funcao NOT NULL
);

-- Inserção dos usuários
INSERT INTO user_account (username, nome, password_hash, funcao) VALUES
('med.cardoso',   'Ana Cardoso',        crypt('PseudoPEP2026!', gen_salt('bf')), 'MEDICO'),
('med.lima',      'Bruno Lima',         crypt('PseudoPEP2026!', gen_salt('bf')), 'MEDICO'),
('med.almeida',   'Carolina Almeida',   crypt('PseudoPEP2026!', gen_salt('bf')), 'MEDICO'),
('med.rocha',     'Daniel Rocha',       crypt('PseudoPEP2026!', gen_salt('bf')), 'MEDICO'),
('med.monteiro',  'Elisa Monteiro',     crypt('PseudoPEP2026!', gen_salt('bf')), 'MEDICO'),
('est.ferreira',  'Lucas Ferreira',     crypt('PseudoPEP2026!', gen_salt('bf')), 'ESTAGIARIO'),
('est.gomes',     'Mariana Gomes',      crypt('PseudoPEP2026!', gen_salt('bf')), 'ESTAGIARIO'),
('est.costa',     'Rafael Costa',       crypt('PseudoPEP2026!', gen_salt('bf')), 'ESTAGIARIO'),
('est.melo',      'Beatriz Melo',       crypt('PseudoPEP2026!', gen_salt('bf')), 'ESTAGIARIO'),
('est.dias',      'Pedro Dias',         crypt('PseudoPEP2026!', gen_salt('bf')), 'ESTAGIARIO'),
('pes.mendes',    'Carla Mendes',       crypt('PseudoPEP2026!', gen_salt('bf')), 'PESQUISADOR'),
('pes.araujo',    'Eduardo Araújo',     crypt('PseudoPEP2026!', gen_salt('bf')), 'PESQUISADOR'),
('pes.silveira',  'Fernanda Silveira',  crypt('PseudoPEP2026!', gen_salt('bf')), 'PESQUISADOR');