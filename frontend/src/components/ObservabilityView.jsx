import React, { useState } from 'react';
import { MOCK_OBSERVABILITY_DATA } from '../mockData';
import { Activity, Cpu, Layers, HardDrive, AlertTriangle, Play, HelpCircle } from 'lucide-react';

const ObservabilityView = () => {
  const [selectedLoad, setSelectedLoad] = useState(10);
  const data = MOCK_OBSERVABILITY_DATA[selectedLoad];

  const loadScenarios = [10, 50, 100, 500, 1000];

  return (
    <div className="animate-fade-in">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <div>
          <h2 style={{ fontSize: '1.8rem', color: 'var(--color-primary)' }}>Métricas de Observabilidade K8S</h2>
          <p style={{ color: 'var(--text-secondary)' }}>Métricas integradas via Prometheus e simulação de teste de carga (k6/Locust) no cluster Kubernetes.</p>
        </div>
        <span className="badge badge-active" style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
          <Activity size={12} />
          Prometheus Ativo
        </span>
      </div>

      {/* Load Selection Bar */}
      <div className="glass-panel" style={{ padding: '1.25rem', marginBottom: '2rem' }}>
        <h3 style={{ fontSize: '1rem', marginBottom: '0.8rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Play size={16} className="text-primary" />
          Simular Cenário de Teste de Carga (Usuários Simultâneos)
        </h3>
        <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
          {loadScenarios.map(load => (
            <button
              key={load}
              onClick={() => setSelectedLoad(load)}
              className="btn"
              style={{
                flexGrow: 1,
                background: selectedLoad === load ? 'var(--color-primary)' : 'var(--bg-card)',
                color: selectedLoad === load ? 'white' : 'var(--text-primary)',
                border: `1px solid ${selectedLoad === load ? 'var(--color-primary)' : 'var(--border-color)'}`
              }}
            >
              {load} Usuários
            </button>
          ))}
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid-stats">
        {/* Throughput */}
        <div className="glass-panel" style={{ padding: '1.25rem' }}>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Throughput (Vazão)</div>
          <div style={{ fontSize: '1.8rem', fontWeight: 'bold', margin: '0.2rem 0', color: 'var(--text-primary)' }}>
            {data.throughput.toLocaleString('pt-BR')} <span style={{ fontSize: '0.9rem', fontWeight: 'normal', color: 'var(--text-secondary)' }}>req/s</span>
          </div>
          <div style={{ height: '4px', background: 'var(--border-color)', borderRadius: '2px', overflow: 'hidden' }}>
            <div style={{ width: `${Math.min(data.throughput / 100, 100)}%`, background: 'var(--color-primary)', height: '100%' }}></div>
          </div>
        </div>

        {/* Latency */}
        <div className="glass-panel" style={{ padding: '1.25rem' }}>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Latência Média</div>
          <div style={{ fontSize: '1.8rem', fontWeight: 'bold', margin: '0.2rem 0', color: data.latency > 100 ? 'var(--color-warning)' : 'var(--color-success)' }}>
            {data.latency} <span style={{ fontSize: '0.9rem', fontWeight: 'normal', color: 'var(--text-secondary)' }}>ms</span>
          </div>
          <div style={{ height: '4px', background: 'var(--border-color)', borderRadius: '2px', overflow: 'hidden' }}>
            <div style={{ width: `${Math.min(data.latency / 2.5, 100)}%`, background: data.latency > 100 ? 'var(--color-warning)' : 'var(--color-success)', height: '100%' }}></div>
          </div>
        </div>

        {/* Error Rate */}
        <div className="glass-panel" style={{ padding: '1.25rem' }}>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Taxa de Erro HTTP/gRPC</div>
          <div style={{ fontSize: '1.8rem', fontWeight: 'bold', margin: '0.2rem 0', color: data.errorRate > 1 ? 'var(--color-danger)' : 'var(--color-success)' }}>
            {data.errorRate.toFixed(2)}<span style={{ fontSize: '0.9rem', fontWeight: 'normal', color: 'var(--text-secondary)' }}>%</span>
          </div>
          <div style={{ height: '4px', background: 'var(--border-color)', borderRadius: '2px', overflow: 'hidden' }}>
            <div style={{ width: `${Math.min(data.errorRate * 50, 100)}%`, background: data.errorRate > 1 ? 'var(--color-danger)' : 'var(--color-success)', height: '100%' }}></div>
          </div>
        </div>
      </div>

      <div className="grid-main" style={{ gridTemplateColumns: '1fr' }}>
        {/* Kubernetes Cluster Scaling Map */}
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
            <h3 style={{ fontSize: '1.2rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Layers size={20} className="text-primary" />
              Mapeamento de Pods no Cluster K8S (Replica Count)
            </h3>
            <span className="badge badge-primary" style={{ background: 'var(--color-primary-glow)', color: 'var(--color-primary)', border: '1px solid rgba(59, 130, 246, 0.3)' }}>
              Total de Réplicas: {data.pods}
            </span>
          </div>

          <div style={{ background: 'rgba(0, 0, 0, 0.2)', border: '1px solid var(--border-color)', borderRadius: 'var(--radius-md)', padding: '1.5rem', marginBottom: '1.5rem' }}>
            {/* Visual Pod Grid */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem', justifyContent: 'center' }}>
              {Array.from({ length: 10 }).map((_, idx) => {
                const isOnline = idx < data.pods;
                return (
                  <div
                    key={idx}
                    className="glass-card"
                    style={{
                      flexBasis: 'calc(20% - 1rem)',
                      minWidth: '100px',
                      padding: '1rem',
                      textAlign: 'center',
                      background: isOnline ? 'rgba(16, 185, 129, 0.08)' : 'rgba(255, 255, 255, 0.01)',
                      borderColor: isOnline ? 'var(--color-medico)' : 'var(--border-color)',
                      opacity: isOnline ? 1 : 0.45,
                      transform: isOnline ? 'scale(1.02)' : 'scale(1)',
                      boxShadow: isOnline ? '0 0 10px rgba(16, 185, 129, 0.15)' : 'none',
                      transition: 'all var(--transition-normal)'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '0.5rem' }}>
                      <div style={{
                        width: '12px',
                        height: '12px',
                        borderRadius: '50%',
                        background: isOnline ? 'var(--color-medico)' : 'var(--text-muted)',
                        boxShadow: isOnline ? '0 0 6px var(--color-medico)' : 'none'
                      }}></div>
                    </div>
                    <div style={{ fontWeight: 600, fontSize: '0.85rem' }}>
                      patient-service
                    </div>
                    <div style={{ fontSize: '0.65rem', color: 'var(--text-secondary)', fontFamily: 'var(--font-mono)' }}>
                      {isOnline ? `pod-${idx + 1}-online` : 'offline'}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Scale Event Logger */}
          <div className="glass-card" style={{ background: 'rgba(0,0,0,0.15)', padding: '1rem', borderStyle: 'dashed' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--color-warning)', fontWeight: 600, fontSize: '0.85rem', marginBottom: '0.4rem' }}>
              <AlertTriangle size={14} />
              Último Evento de Escalonamento (HPA Engine):
            </div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.8rem', color: 'var(--text-primary)' }}>
              {data.scaleEvent}
            </div>
          </div>
        </div>

        {/* Resources Usage Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem' }}>
          {/* CPU Usage Graph */}
          <div className="glass-panel" style={{ padding: '1.5rem' }}>
            <h4 style={{ fontSize: '1rem', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Cpu size={16} className="text-primary" /> Uso de CPU dos Pods (Médio)
            </h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', alignItems: 'center', justifyContent: 'center', height: '120px' }}>
              <div style={{ fontSize: '2.5rem', fontWeight: 800, color: data.cpuUsage > 70 ? 'var(--color-danger)' : 'var(--text-primary)' }}>
                {data.cpuUsage}%
              </div>
              <div style={{ width: '80%', height: '8px', background: 'var(--border-color)', borderRadius: '4px', overflow: 'hidden' }}>
                <div style={{
                  width: `${data.cpuUsage}%`,
                  background: data.cpuUsage > 70 ? 'var(--color-danger)' : 'var(--color-primary)',
                  height: '100%',
                  borderRadius: '4px'
                }}></div>
              </div>
              <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Limiar HPA configurado: &gt;70% de CPU</div>
            </div>
          </div>

          {/* Memory Usage Graph */}
          <div className="glass-panel" style={{ padding: '1.5rem' }}>
            <h4 style={{ fontSize: '1rem', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <HardDrive size={16} className="text-primary" /> Uso de Memória dos Pods (Médio)
            </h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', alignItems: 'center', justifyContent: 'center', height: '120px' }}>
              <div style={{ fontSize: '2.5rem', fontWeight: 800 }}>
                {data.memUsage}%
              </div>
              <div style={{ width: '80%', height: '8px', background: 'var(--border-color)', borderRadius: '4px', overflow: 'hidden' }}>
                <div style={{
                  width: `${data.memUsage}%`,
                  background: 'var(--color-primary)',
                  height: '100%',
                  borderRadius: '4px'
                }}></div>
              </div>
              <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Memória limite alocada: 512Mi por Pod</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ObservabilityView;
