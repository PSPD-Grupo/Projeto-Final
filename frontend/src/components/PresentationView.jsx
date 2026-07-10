import React, { useState } from 'react';
import { ChevronLeft, ChevronRight, Play, Users, Layers, Award, Terminal, Shield, Cpu } from 'lucide-react';

const PresentationView = () => {
  const [currentSlide, setCurrentSlide] = useState(0);

  const slides = [
    // Slide 0: Title Slide
    {
      title: "Monitoramento e Observabilidade em Clusters K8S",
      subtitle: "Estudo de Caso: Portal Hospitalar HL7/FHIR de Microsserviços",
      icon: <Award size={48} className="text-primary" />,
      content: (
        <div style={{ textAlign: 'center', marginTop: '2rem' }}>
          <p style={{ color: 'var(--text-secondary)', fontSize: '1.1rem', marginBottom: '2rem' }}>
            Trabalho Prático de PSPD (Programação para Sistemas Paralelos e Distribuídos)
          </p>
          <div className="glass-card" style={{ maxWidth: '600px', margin: '0 auto', textAlign: 'left', padding: '1.5rem' }}>
            <h4 style={{ color: 'var(--text-primary)', marginBottom: '1rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Users size={16} /> Integrantes do Grupo:
            </h4>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr auto', gap: '0.5rem 2rem', fontSize: '0.95rem' }}>
              <strong>Milena Baruc Rodrigues Morais</strong> <span style={{ color: 'var(--text-secondary)', fontFamily: 'var(--font-mono)' }}>211062339</span>
              <strong>Pedro Fonseca Cruz</strong> <span style={{ color: 'var(--text-secondary)', fontFamily: 'var(--font-mono)' }}>212005444</span>
              <strong>Daniel dos Santos Barros de Sousa</strong> <span style={{ color: 'var(--text-secondary)', fontFamily: 'var(--font-mono)' }}>211030980</span>
              <strong>Gabriel Freitas Balbino</strong> <span style={{ color: 'var(--text-secondary)', fontFamily: 'var(--font-mono)' }}>180075462</span>
            </div>
          </div>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginTop: '2rem' }}>
            Professor Orientador: Fernando W. Cruz • Universidade de Brasília (FGA)
          </p>
        </div>
      )
    },
    // Slide 1: Problem & Objective
    {
      title: "Objetivo do Projeto",
      subtitle: "O Desafio Clínico e a Observabilidade K8S",
      icon: <Shield size={48} style={{ color: 'var(--color-medico)' }} />,
      content: (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', marginTop: '1.5rem' }}>
          <div className="glass-card">
            <h4 style={{ color: 'var(--color-medico)', marginBottom: '0.8rem' }}>1. Desafio de Segurança & FHIR</h4>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '1rem', lineHeight: '1.6' }}>
              Disponibilizar prontuários médicos com controle rígido de segurança em padrão <strong>HL7/FHIR</strong>.
            </p>
            <ul style={{ paddingLeft: '1.25rem', fontSize: '0.85rem', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              <li><strong>Médicos (FULL)</strong>: Acesso total aos dados de pacientes sob responsabilidade.</li>
              <li><strong>Estagiários (PARTIAL)</strong>: Acesso sob supervisão com dados sensíveis (CPF, CNS, endereço) camuflados.</li>
              <li><strong>Pesquisadores (ANON/AGREG)</strong>: Acesso restrito a coortes e estatísticas de projetos aprovados.</li>
            </ul>
          </div>
          <div className="glass-card">
            <h4 style={{ color: 'var(--color-primary)', marginBottom: '0.8rem' }}>2. Infraestrutura & Observabilidade</h4>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '1rem', lineHeight: '1.6' }}>
              Garantir que a arquitetura distribuída no Kubernetes responda a picos de tráfego com estabilidade.
            </p>
            <ul style={{ paddingLeft: '1.25rem', fontSize: '0.85rem', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              <li>Preparação do Kubernetes em modo cluster (1 Master + 3 Workers).</li>
              <li>Execução de testes de carga (10 a 1000 usuários simultâneos).</li>
              <li>Estruturação de observabilidade com métricas Prometheus / Grafana.</li>
              <li>Autoscaling horizontal (HPA) baseado em CPU.</li>
            </ul>
          </div>
        </div>
      )
    },
    // Slide 2: System Architecture
    {
      title: "Arquitetura da Aplicação",
      subtitle: "Divisão de Responsabilidades e gRPC",
      icon: <Layers size={48} style={{ color: 'var(--color-pesquisador)' }} />,
      content: (
        <div style={{ textAlign: 'center', marginTop: '1rem' }}>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
            Fluxo de requisições do navegador ao banco de dados passando pelo cluster Kubernetes:
          </p>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem' }}>
            <div className="glass-card" style={{ padding: '0.8rem' }}>
              <div style={{ fontWeight: 600, color: 'var(--color-primary)' }}>Navegador</div>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '0.4rem' }}>
                React SPA gerencia autenticação e monta visões baseadas em JWT
              </p>
            </div>
            <div className="glass-card" style={{ padding: '0.8rem' }}>
              <div style={{ fontWeight: 600, color: 'var(--color-warning)' }}>API Gateway</div>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '0.4rem' }}>
                Recebe REST, valida tokens JWT, aplica rate-limit e roteia requisições
              </p>
            </div>
            <div className="glass-card" style={{ padding: '0.8rem' }}>
              <div style={{ fontWeight: 600, color: 'var(--color-medico)' }}>gRPC Services</div>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '0.4rem' }}>
                Três microsserviços (Auth, Patient Data, Transform) comunicando via HTTP/2
              </p>
            </div>
            <div className="glass-card" style={{ padding: '0.8rem' }}>
              <div style={{ fontWeight: 600 }}>PostgreSQL</div>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '0.4rem' }}>
                Banco relacional central contendo dados clínicos estruturados
              </p>
            </div>
          </div>
          <div className="glass-card" style={{ marginTop: '1.5rem', padding: '0.75rem', background: 'rgba(0,0,0,0.2)', display: 'inline-block', fontSize: '0.85rem' }}>
            🔑 <strong>Data Transform Service</strong>: Realiza a conversão de banco relacional para recursos <strong>HL7/FHIR</strong> JSON e aplica as máscaras de anonimização.
          </div>
        </div>
      )
    },
    // Slide 3: Kubernetes Infrastructure
    {
      title: "Cluster Kubernetes",
      subtitle: "Montagem da Infraestrutura do Experimento",
      icon: <Cpu size={48} className="text-primary" />,
      content: (
        <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '2rem', marginTop: '1.5rem' }}>
          <div className="glass-card" style={{ padding: '1.25rem' }}>
            <h4 style={{ color: 'var(--color-primary)', marginBottom: '0.75rem' }}>Topologia do Cluster</h4>
            <ul style={{ paddingLeft: '1.25rem', fontSize: '0.85rem', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              <li><strong>Nó Mestre (Control Plane)</strong>: Orquestrador da API, agendamento de pods e controle de estados.</li>
              <li><strong>Nós Trabalhadores (3 Worker Nodes)</strong>: Hospedam os pods da aplicação distribuída, promovendo escalabilidade.</li>
              <li><strong>HPA (Horizontal Pod Autoscaler)</strong>:
                <br /><span style={{ color: 'var(--text-muted)' }}>Configurado para escalonar o <code>patient-service</code> de 1 para até 10 réplicas quando o uso médio de CPU cruzar o limiar de 70%.</span>
              </li>
            </ul>
          </div>
          <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', justifyBlock: 'center' }}>
            <h4 style={{ color: 'var(--color-warning)', marginBottom: '0.75rem' }}>Ferramenta de Observabilidade</h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
              <div>📈 <strong>Prometheus</strong>: Agente ativo dentro do cluster, raspando métricas de CPU, uso de memória, latência HTTP/gRPC e taxas de erro.</div>
              <div>🖥️ <strong>Grafana</strong>: Integrado para plotar visualmente as métricas e consolidar relatórios de escalabilidade.</div>
            </div>
          </div>
        </div>
      )
    },
    // Slide 4: Load Testing & Performance
    {
      title: "Resultados dos Testes de Carga",
      subtitle: "Análise de Elasticidade e Desempenho",
      icon: <Terminal size={48} style={{ color: 'var(--color-warning)' }} />,
      content: (
        <div style={{ marginTop: '1rem' }}>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
            Comportamento do cluster com tráfego simultâneo (k6 / Locust):
          </p>
          <div className="table-wrapper">
            <table className="table-custom" style={{ fontSize: '0.8rem' }}>
              <thead>
                <tr style={{ background: 'var(--bg-hover)' }}>
                  <th>Cenário (Usuários)</th>
                  <th>Throughput (req/s)</th>
                  <th>Latência Média</th>
                  <th>Taxa de Erro</th>
                  <th>Pods Ativos (HPA)</th>
                  <th>Status do Sistema</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>10</strong></td>
                  <td>120 req/s</td>
                  <td>18 ms</td>
                  <td>0.00%</td>
                  <td>1 Pod</td>
                  <td style={{ color: 'var(--color-success)' }}>Excelente / Mínimo</td>
                </tr>
                <tr>
                  <td><strong>50</strong></td>
                  <td>580 req/s</td>
                  <td>24 ms</td>
                  <td>0.00%</td>
                  <td>1 Pod</td>
                  <td style={{ color: 'var(--color-success)' }}>Estável</td>
                </tr>
                <tr>
                  <td><strong>100</strong></td>
                  <td>1.120 req/s</td>
                  <td>38 ms</td>
                  <td>0.10%</td>
                  <td>2 Pods</td>
                  <td style={{ color: 'var(--color-success)' }}>HPA Escalonado</td>
                </tr>
                <tr>
                  <td><strong>500</strong></td>
                  <td>4.950 req/s</td>
                  <td>85 ms</td>
                  <td>0.30%</td>
                  <td>5 Pods</td>
                  <td style={{ color: 'var(--color-warning)' }}>Carga Elevada</td>
                </tr>
                <tr>
                  <td><strong>1000</strong></td>
                  <td>9.210 req/s</td>
                  <td>195 ms</td>
                  <td>1.40%</td>
                  <td>10 Pods</td>
                  <td style={{ color: 'var(--color-danger)' }}>Limite de Réplicas</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.6rem', textAlign: 'center' }}>
            💡 <strong>Conclusão do Teste</strong>: O autoscaling HPA respondeu com eficácia, estabilizando as taxas de erro em menos de 2% mesmo sob tráfego massivo.
          </p>
        </div>
      )
    }
  ];

  const handleNext = () => {
    if (currentSlide < slides.length - 1) {
      setCurrentSlide(currentSlide + 1);
    }
  };

  const handlePrev = () => {
    if (currentSlide > 0) {
      setCurrentSlide(currentSlide - 1);
    }
  };

  const activeSlide = slides[currentSlide];

  return (
    <div className="glass-panel animate-fade-in" style={{ padding: '2.5rem', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', minHeight: '480px' }}>
      
      {/* Slide Header */}
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem', marginBottom: '1rem' }}>
          {activeSlide.icon}
          <div>
            <h3 style={{ fontSize: '1.6rem', color: 'var(--text-primary)', lineHeight: '1.2' }}>{activeSlide.title}</h3>
            <p style={{ color: 'var(--color-primary)', fontSize: '0.95rem' }}>{activeSlide.subtitle}</p>
          </div>
        </div>
        <hr style={{ border: 'none', borderTop: '1px solid var(--border-color)', margin: '1rem 0' }} />
      </div>

      {/* Slide Body */}
      <div style={{ flexGrow: 1, padding: '1rem 0' }}>
        {activeSlide.content}
      </div>

      {/* Slide Footer / Navigation */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '2rem', borderTop: '1px solid var(--border-color)', paddingTop: '1.25rem' }}>
        <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
          Slide {currentSlide + 1} de {slides.length}
        </span>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button 
            onClick={handlePrev} 
            disabled={currentSlide === 0}
            className="btn btn-outline"
            style={{ padding: '0.4rem 0.8rem', opacity: currentSlide === 0 ? 0.3 : 1, cursor: currentSlide === 0 ? 'not-allowed' : 'pointer' }}
          >
            <ChevronLeft size={16} />
            Anterior
          </button>
          <button 
            onClick={handleNext} 
            disabled={currentSlide === slides.length - 1}
            className="btn btn-primary"
            style={{ padding: '0.4rem 0.8rem', opacity: currentSlide === slides.length - 1 ? 0.3 : 1, cursor: currentSlide === slides.length - 1 ? 'not-allowed' : 'pointer' }}
          >
            Avançar
            <ChevronRight size={16} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default PresentationView;
