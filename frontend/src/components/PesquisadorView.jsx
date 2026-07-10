import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Folder, Users, BarChart2, ShieldAlert, Award, FileSpreadsheet, Lock, CheckCircle, HelpCircle } from 'lucide-react';

const PesquisadorView = ({ token }) => {
  const [projects, setProjects] = useState([]);
  const [selectedProjectId, setSelectedProjectId] = useState(null);
  const [selectedProject, setSelectedProject] = useState(null);
  const [cohortData, setCohortData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch researcher projects
  useEffect(() => {
    const fetchProjects = async () => {
      setLoading(true);
      try {
        const data = await api.getProjects(token);
        setProjects(data);
        if (data.length > 0) {
          handleSelectProject(data[0]);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchProjects();
  }, [token]);

  const handleSelectProject = async (project) => {
    setLoading(true);
    setError(null);
    setSelectedProjectId(project.id_projeto);
    setSelectedProject(project);
    setCohortData(null);
    try {
      // Fetch cohort data for the project's condition
      const data = await api.getCohortData(project.codigo_condicao, project.id_projeto, token);
      setCohortData(data);
    } catch (err) {
      // In case of DENY (e.g., project is Suspended)
      setCohortData(null);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="animate-fade-in">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <div>
          <h2 style={{ fontSize: '1.8rem', color: 'var(--color-pesquisador)' }}>Painel do Pesquisador</h2>
          <p style={{ color: 'var(--text-secondary)' }}>Acesso anonimizado e agregado (ANONYMIZED/AGGREGATED) para fins de pesquisa científica.</p>
        </div>
        <span className="badge badge-pesquisador">Cientista • ANONYMIZED ACCESS</span>
      </div>

      <div className="grid-main">
        {/* Left Side: Projects List */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div className="glass-panel" style={{ padding: '1.25rem' }}>
            <h3 style={{ fontSize: '1.1rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Folder size={18} />
              Projetos de Pesquisa
            </h3>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {projects.map(p => {
                const isActive = selectedProjectId === p.id_projeto;
                return (
                  <button
                    key={p.id_projeto}
                    onClick={() => handleSelectProject(p)}
                    style={{
                      display: 'flex',
                      flexDirection: 'column',
                      width: '100%',
                      padding: '1rem',
                      borderRadius: 'var(--radius-sm)',
                      background: isActive ? 'var(--color-pesquisador-glow)' : 'var(--bg-card)',
                      border: `1px solid ${isActive ? 'var(--color-pesquisador)' : 'var(--border-color)'}`,
                      textAlign: 'left',
                      cursor: 'pointer',
                      transition: 'all var(--transition-fast)'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', width: '100%', marginBottom: '0.5rem' }}>
                      <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600 }}>{p.id_projeto}</span>
                      <span className={`badge ${p.status === 'Aprovado' ? 'badge-active' : 'badge-danger'}`} style={{ scale: '0.85', transformOrigin: 'top right' }}>
                        {p.status}
                      </span>
                    </div>
                    <div style={{ fontWeight: 600, fontSize: '0.95rem', color: 'var(--text-primary)', marginBottom: '0.5rem', lineHeight: '1.25' }}>
                      {p.titulo}
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: 'var(--text-secondary)', width: '100%', borderTop: '1px solid rgba(255, 255, 255, 0.05)', paddingTop: '0.4rem' }}>
                      <span>Coorte: <strong>{p.codigo_condicao}</strong></span>
                      <span>Validade: {p.validade}</span>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Right Side: Cohort & Aggregated Stats or DENY */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {loading ? (
            <div className="glass-panel" style={{ padding: '4rem', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
              <div style={{ textAlign: 'center' }}>
                <div style={{ width: '40px', height: '40px', border: '3px solid var(--border-color)', borderTopColor: 'var(--color-pesquisador)', borderRadius: '50%', animation: 'spin 1s linear infinite', margin: '0 auto 1rem' }}></div>
                <p style={{ color: 'var(--text-secondary)' }}>Calculando estatísticas agregadas e aplicando hash de anonimização...</p>
              </div>
            </div>
          ) : error ? (
            /* DENY Layout (e.g. Suspended Project) */
            <div className="glass-panel" style={{ padding: '3rem', border: '1px solid var(--color-danger)', background: 'rgba(244, 63, 94, 0.03)' }}>
              <div style={{ textAlign: 'center' }}>
                <ShieldAlert size={48} style={{ color: 'var(--color-danger)', marginBottom: '1rem' }} />
                <h3 style={{ fontSize: '1.4rem', color: 'var(--color-danger)', marginBottom: '0.5rem' }}>Acesso Negado (DENY)</h3>
                <p style={{ color: 'var(--text-primary)', maxWidth: '450px', margin: '0 auto 1rem', fontSize: '0.95rem' }}>
                  {error}
                </p>
                <div className="glass-card" style={{ maxWidth: '500px', margin: '1.5rem auto 0', padding: '1rem', background: 'rgba(0,0,0,0.2)', textAlign: 'left', fontSize: '0.8rem', fontFamily: 'var(--font-mono)' }}>
                  <div style={{ color: 'var(--color-danger)', fontWeight: 'bold', marginBottom: '0.5rem' }}>Decisão do Authorization Service:</div>
                  • Requisitante: pesq.fonseca (Pesquisador)<br />
                  • Recurso: Cohort/{selectedProject?.codigo_condicao} (via Projeto {selectedProject?.id_projeto})<br />
                  • Status do Projeto: {selectedProject?.status}<br />
                  • Status: DENY (Consulta negada. Motivo: Projeto de pesquisa suspenso/expirado)
                </div>
              </div>
            </div>
          ) : cohortData ? (
            /* AGGREGATED & ANONYMIZED View */
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
              {/* Aggregation Panel Header */}
              <div className="glass-panel" style={{ padding: '1.5rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                  <h3 style={{ fontSize: '1.4rem', color: 'var(--color-pesquisador)' }}>
                    Dados do Coorte: {selectedProject.codigo_condicao}
                  </h3>
                  <span className="badge badge-pesquisador" style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                    <CheckCircle size={12} />
                    Projeto Vigente
                  </span>
                </div>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: '1.4' }}>
                  Mostrando dados clínicos consolidados da população hospitalar sob diagnóstico de <strong>{selectedProject.codigo_condicao}</strong>.
                </p>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', background: 'rgba(6, 182, 212, 0.05)', border: '1px solid rgba(6, 182, 212, 0.15)', borderRadius: 'var(--radius-sm)', padding: '0.5rem 0.75rem', fontSize: '0.75rem', color: 'var(--color-pesquisador)', marginTop: '0.8rem' }}>
                  <Lock size={14} />
                  <span>Anonimização por pseudonimização ativa. Prontuários originais blindados pelo <strong>Data Transform Service</strong>.</span>
                </div>
              </div>

              {/* Statistics Grid */}
              <div className="grid-stats">
                {/* Total Cases */}
                <div className="glass-panel" style={{ padding: '1.25rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
                  <div style={{ background: 'var(--color-pesquisador-glow)', color: 'var(--color-pesquisador)', padding: '0.75rem', borderRadius: 'var(--radius-sm)' }}>
                    <Users size={24} />
                  </div>
                  <div>
                    <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Casos no Coorte</div>
                    <div style={{ fontSize: '1.6rem', fontWeight: 'bold' }}>{cohortData.totalCases.toLocaleString('pt-BR')}</div>
                  </div>
                </div>

                {/* Gender Ratio */}
                <div className="glass-panel" style={{ padding: '1.25rem' }}>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>Distribuição de Gênero</div>
                  <div style={{ display: 'flex', height: '18px', borderRadius: '9px', overflow: 'hidden', background: '#3b82f6', position: 'relative' }}>
                    <div style={{ width: `${cohortData.demographics.women}%`, background: '#ec4899', height: '100%' }} title={`Mulheres: ${cohortData.demographics.women}%`}></div>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.7rem', marginTop: '0.4rem', color: 'var(--text-secondary)' }}>
                    <span style={{ color: '#ec4899' }}>Feminino: {cohortData.demographics.women}%</span>
                    <span style={{ color: '#3b82f6' }}>Masculino: {cohortData.demographics.men}%</span>
                  </div>
                </div>
              </div>

              {/* Graphical Distribution */}
              <div className="grid-stats" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))' }}>
                {/* Age Bands */}
                <div className="glass-panel" style={{ padding: '1.25rem' }}>
                  <h4 style={{ fontSize: '0.9rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                    <BarChart2 size={16} /> Faixa Etária (%)
                  </h4>
                  <div className="chart-container">
                    {cohortData.demographics.ageBands.map(band => (
                      <div key={band.label} className="chart-bar-wrapper">
                        <div 
                          className="chart-bar" 
                          style={{ height: `${band.value * 2.2}px`, '--chart-color': 'var(--color-pesquisador)' }}
                        >
                          <div className="chart-tooltip">{band.value}%</div>
                        </div>
                        <div className="chart-label">{band.label}</div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Top Departments */}
                <div className="glass-panel" style={{ padding: '1.25rem' }}>
                  <h4 style={{ fontSize: '0.9rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                    <BarChart2 size={16} /> Setores Mais Acessados
                  </h4>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', height: '250px', justifyContent: 'center' }}>
                    {cohortData.departments.map(dept => (
                      <div key={dept.name}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', marginBottom: '0.25rem' }}>
                          <span>{dept.name}</span>
                          <span style={{ fontWeight: 600 }}>{dept.pct}%</span>
                        </div>
                        <div style={{ height: '6px', background: 'var(--border-color)', borderRadius: '3px', overflow: 'hidden' }}>
                          <div style={{ width: `${dept.pct}%`, background: 'var(--color-pesquisador)', height: '100%', borderRadius: '3px' }}></div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Anonymized Patients Lab Data */}
              <div className="glass-panel" style={{ padding: '1.5rem' }}>
                <h3 style={{ fontSize: '1.1rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <FileSpreadsheet size={18} />
                  Dados Clínicos e Exames Pseudonimizados (Amostragem)
                </h3>
                
                <div className="table-wrapper">
                  <table className="table-custom">
                    <thead>
                      <tr>
                        <th>Hash Identificador</th>
                        <th>Sexo</th>
                        <th>Idade</th>
                        <th>Resultados Laboratoriais FHIR Convertidos</th>
                      </tr>
                    </thead>
                    <tbody>
                      {cohortData.anonymizedPatients.map(ap => (
                        <tr key={ap.hash}>
                          <td style={{ fontFamily: 'var(--font-mono)', fontSize: '0.8rem', color: 'var(--color-pesquisador)' }}>
                            {ap.hash}
                          </td>
                          <td>{ap.gender === 'F' ? 'Feminino' : 'Masculino'}</td>
                          <td>{ap.age} anos</td>
                          <td>
                            <span style={{
                              fontFamily: 'var(--font-mono)',
                              fontSize: '0.75rem',
                              background: 'var(--bg-primary)',
                              padding: '0.25rem 0.5rem',
                              borderRadius: '4px',
                              border: '1px solid var(--border-color)',
                              color: 'var(--text-primary)'
                            }}>
                              {ap.exams}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                <p style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: '0.8rem', fontStyle: 'italic' }}>
                  * Nota: A decodificação destes hashes para IDs reais de prontuário só é possível sob auditoria do Comitê de Ética em Pesquisa (CEP) do hospital.
                </p>
              </div>
            </div>
          ) : (
            <div className="glass-panel" style={{ padding: '4rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
              Selecione um projeto de pesquisa à esquerda para visualizar os dados de coorte.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PesquisadorView;
