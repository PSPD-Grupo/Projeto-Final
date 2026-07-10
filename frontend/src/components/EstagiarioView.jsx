import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import FHIRVisualizer from './FHIRVisualizer';
import { Search, User, Calendar, Phone, FileText, Activity, ShieldAlert, EyeOff, Lock, HelpCircle, Database } from 'lucide-react';

const EstagiarioView = ({ token }) => {
  const [patients, setPatients] = useState([]);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [patientRecord, setPatientRecord] = useState(null);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [fhirData, setFhirData] = useState(null);
  const [fhirTitle, setFhirTitle] = useState('');

  // Fetch list of supervised patients
  useEffect(() => {
    const fetchPatients = async () => {
      setLoading(true);
      try {
        const data = await api.getPatients(token);
        setPatients(data);
        if (data.length > 0) {
          handleSelectPatient(data[0].id);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchPatients();
  }, [token]);

  const handleSelectPatient = async (patientId) => {
    setLoading(true);
    setError(null);
    setFhirData(null);
    try {
      const details = await api.getPatientDetails(patientId, token);
      setPatientRecord(details);
      setSelectedPatient(patientId);
    } catch (err) {
      // Access DENIED
      setPatientRecord(null);
      setSelectedPatient(patientId);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleViewFHIR = async (resourceType, id, title) => {
    try {
      const fhir = await api.getFHIRResource(resourceType, id, token);
      setFhirData(fhir);
      setFhirTitle(title);
    } catch (err) {
      alert(`Erro ao buscar recurso FHIR: ${err.message}`);
    }
  };

  const filteredPatients = patients.filter(p => 
    p.name.toLowerCase().includes(search.toLowerCase()) ||
    p.id.toLowerCase().includes(search.toLowerCase())
  );



  return (
    <div className="animate-fade-in">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <div>
          <h2 style={{ fontSize: '1.8rem', color: 'var(--color-estagiario)' }}>Painel do Estagiário</h2>
          <p style={{ color: 'var(--text-secondary)' }}>Acesso parcial (PARTIAL) sob supervisão. Identificadores pessoais ocultados pelo Data Transform Service.</p>
        </div>
        <span className="badge badge-estagiario">Estudante • PARTIAL ACCESS</span>
      </div>

      <div className="grid-main">
        {/* Left Side: Patient Selector */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div className="glass-panel" style={{ padding: '1.25rem' }}>
            <h3 style={{ fontSize: '1.1rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Search size={18} />
              Buscar Paciente
            </h3>
            <div style={{ position: 'relative', marginBottom: '1.25rem' }}>
              <input 
                type="text"
                placeholder="Buscar por ID..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                style={{
                  width: '100%',
                  padding: '0.6rem 1rem 0.6rem 2.2rem',
                  border: '1px solid var(--border-color)',
                  borderRadius: 'var(--radius-sm)',
                  background: 'var(--bg-primary)'
                }}
              />
              <Search size={14} style={{ position: 'absolute', left: '0.8rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
            </div>

            <h4 style={{ fontSize: '0.85rem', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.5rem' }}>Pacientes Supervisionados</h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', maxHeight: '200px', overflowY: 'auto' }}>
              {filteredPatients.length === 0 ? (
                <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', padding: '0.5rem' }}>Nenhum paciente ativo</p>
              ) : (
                filteredPatients.map(p => (
                  <button
                    key={p.id}
                    onClick={() => handleSelectPatient(p.id)}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      padding: '0.75rem',
                      borderRadius: 'var(--radius-sm)',
                      background: selectedPatient === p.id && !error ? 'var(--color-estagiario-glow)' : 'transparent',
                      border: `1px solid ${selectedPatient === p.id && !error ? 'var(--color-estagiario)' : 'var(--border-color)'}`,
                      textAlign: 'left',
                      cursor: 'pointer',
                      transition: 'all var(--transition-fast)'
                    }}
                  >
                    <div>
                      <div style={{ fontWeight: 600, fontSize: '0.95rem' }}>{p.name}</div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>ID: {p.id} • {p.cpf}</div>
                    </div>
                    <User size={16} style={{ color: selectedPatient === p.id && !error ? 'var(--color-estagiario)' : 'var(--text-muted)' }} />
                  </button>
                ))
              )}
            </div>


          </div>
        </div>

        {/* Right Side: Detailed Medical Record (Partial Access) */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {loading ? (
            <div className="glass-panel" style={{ padding: '4rem', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
              <div style={{ textAlign: 'center' }}>
                <div style={{ width: '40px', height: '40px', border: '3px solid var(--border-color)', borderTopColor: 'var(--color-estagiario)', borderRadius: '50%', animation: 'spin 1s linear infinite', margin: '0 auto 1rem' }}></div>
                <p style={{ color: 'var(--text-secondary)' }}>Buscando dados autorizados...</p>
              </div>
            </div>
          ) : error ? (
            /* DENY Layout */
            <div className="glass-panel" style={{ padding: '3rem', border: '1px solid var(--color-danger)', background: 'rgba(244, 63, 94, 0.03)' }}>
              <div style={{ textAlign: 'center' }}>
                <ShieldAlert size={48} style={{ color: 'var(--color-danger)', marginBottom: '1rem' }} />
                <h3 style={{ fontSize: '1.4rem', color: 'var(--color-danger)', marginBottom: '0.5rem' }}>Acesso Negado (DENY)</h3>
                <p style={{ color: 'var(--text-primary)', maxWidth: '450px', margin: '0 auto 1rem', fontSize: '0.95rem' }}>
                  {error}
                </p>
                <div className="glass-card" style={{ maxWidth: '500px', margin: '1.5rem auto 0', padding: '1rem', background: 'rgba(0,0,0,0.2)', textAlign: 'left', fontSize: '0.8rem', fontFamily: 'var(--font-mono)' }}>
                  <div style={{ color: 'var(--color-danger)', fontWeight: 'bold', marginBottom: '0.5rem' }}>Decisão do Authorization Service:</div>
                  • Requisitante: est.barros (Estagiário)<br />
                  • Recurso: Patient/{selectedPatient}<br />
                  • Vínculo de supervisão ativa na tabela: NÃO LOCALIZADO<br />
                  • Status: DENY (Bloqueado. Motivo: Fora do escopo supervisionado)
                </div>
              </div>
            </div>
          ) : patientRecord ? (
            /* PARTIAL Medical Record Layout */
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
              {/* Demographics Card with Masking Visualizers */}
              <div className="glass-panel" style={{ padding: '1.5rem', position: 'relative' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
                  <div>
                    <h3 style={{ fontSize: '1.5rem', marginBottom: '0.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      {patientRecord.patient.name}
                      <span className="badge badge-estagiario" style={{ fontSize: '0.6rem', padding: '0.1rem 0.4rem' }}>Nome Mascarado</span>
                    </h3>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
                      <span>ID: {patientRecord.patient.id}</span>
                      <span>•</span>
                      <span style={{ textTransform: 'capitalize' }}>Sexo: {patientRecord.patient.gender === 'male' ? 'Masculino' : 'Feminino'}</span>
                    </p>
                  </div>
                  <button 
                    onClick={() => handleViewFHIR('Patient', patientRecord.patient.id, `Patient Resource: (Partial - Masked)`)}
                    className="btn btn-outline"
                    style={{ fontSize: '0.8rem', padding: '0.4rem 0.8rem', borderColor: 'var(--color-estagiario)', color: 'var(--color-estagiario)' }}
                  >
                    <Database size={14} />
                    Ver FHIR Patient
                  </button>
                </div>

                <div style={{
                  background: 'rgba(245, 158, 11, 0.05)',
                  border: '1px solid rgba(245, 158, 11, 0.15)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '0.5rem 0.75rem',
                  fontSize: '0.75rem',
                  color: 'var(--color-estagiario)',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  marginTop: '0.8rem'
                }}>
                  <EyeOff size={14} />
                  <span>Identificadores pessoais diretos camuflados pelo <strong>Data Transform Service</strong>.</span>
                </div>

                <hr style={{ border: 'none', borderTop: '1px solid var(--border-color)', margin: '1rem 0' }} />

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', fontSize: '0.9rem' }}>
                  <div>
                    <div style={{ color: 'var(--text-muted)' }}>Data de Nascimento</div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', marginTop: '0.2rem' }}>
                      <Calendar size={14} />
                      {patientRecord.patient.birth_date}
                    </div>
                  </div>
                  
                  {/* Masked CPF */}
                  <div>
                    <div style={{ color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                      CPF <Lock size={12} style={{ color: 'var(--color-estagiario)' }} />
                    </div>
                    <div className="masked-container" style={{ marginTop: '0.2rem' }}>
                      <span className="masked-data">{patientRecord.patient.cpf}</span>
                      <span className="badge badge-estagiario" style={{ fontSize: '0.6rem', padding: '0.05rem 0.3rem', scale: '0.85', marginLeft: '-15px' }}>***-**</span>
                    </div>
                  </div>

                  {/* Masked CNS */}
                  <div>
                    <div style={{ color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                      CNS <Lock size={12} style={{ color: 'var(--color-estagiario)' }} />
                    </div>
                    <div className="masked-container" style={{ marginTop: '0.2rem' }}>
                      <span className="masked-data">{patientRecord.patient.cns}</span>
                      <span className="badge badge-estagiario" style={{ fontSize: '0.6rem', padding: '0.05rem 0.3rem', scale: '0.85', marginLeft: '-15px' }}>Anonimizado</span>
                    </div>
                  </div>

                  {/* Masked Phone */}
                  <div>
                    <div style={{ color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                      Telefone <Lock size={12} style={{ color: 'var(--color-estagiario)' }} />
                    </div>
                    <div className="masked-container" style={{ marginTop: '0.2rem' }}>
                      <span className="masked-data">{patientRecord.patient.phone}</span>
                      <span className="badge badge-estagiario" style={{ fontSize: '0.6rem', padding: '0.05rem 0.3rem', scale: '0.85', marginLeft: '-15px' }}>(61) 9****</span>
                    </div>
                  </div>
                </div>

                {/* Masked Address */}
                <div style={{ marginTop: '1rem', fontSize: '0.9rem' }}>
                  <div style={{ color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                    Endereço <Lock size={12} style={{ color: 'var(--color-estagiario)' }} />
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '0.2rem' }}>
                    <span>{patientRecord.patient.address}</span>
                    <span className="badge badge-estagiario" style={{ fontSize: '0.6rem', padding: '0.05rem 0.3rem' }}>Localidade Apenas</span>
                  </div>
                </div>
              </div>

              {/* Resumo Clínico (Exames e Medicamentos) */}
              <div className="glass-panel" style={{ padding: '1.5rem' }}>
                <h3 style={{ fontSize: '1.2rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--color-estagiario)' }}>
                  <FileText size={18} />
                  Dados Clínicos Autorizados
                </h3>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '1.5rem' }}>
                  {/* Conditions */}
                  <div>
                    <h4 style={{ fontSize: '0.9rem', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.5rem' }}>Diagnósticos</h4>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                      {patientRecord.events.filter(e => e.tipo === 'Condição').map(e => (
                        <div key={e.id_evento} className="glass-card" style={{ padding: '0.75rem 1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexGrow: 1 }}>
                          <div>
                            <div style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{e.descricao}</div>
                            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Registrado em {e.data_evento}</div>
                          </div>
                          <button 
                            onClick={() => handleViewFHIR('Condition', e.id_evento, `Condition: ${e.descricao}`)}
                            style={{ background: 'none', border: 'none', color: 'var(--color-estagiario)', cursor: 'pointer', fontSize: '0.75rem' }}
                          >
                            FHIR
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Medications */}
                  <div>
                    <h4 style={{ fontSize: '0.9rem', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.5rem' }}>Medicamentos Prescritos</h4>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                      {patientRecord.events.filter(e => e.tipo === 'Medicação').map(e => (
                        <div key={e.id_evento} className="glass-card" style={{ padding: '0.75rem 1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <div>
                            <div style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{e.descricao}</div>
                            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Prescrito em {e.data_evento}</div>
                          </div>
                          <button 
                            onClick={() => handleViewFHIR('MedicationRequest', e.id_evento, `MedicationRequest: ${e.descricao}`)}
                            style={{ background: 'none', border: 'none', color: 'var(--color-estagiario)', cursor: 'pointer', fontSize: '0.75rem' }}
                          >
                            FHIR
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Observations / Exams */}
                  <div>
                    <h4 style={{ fontSize: '0.9rem', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.5rem' }}>Exames e Sinais Clínicos</h4>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                      {patientRecord.events.filter(e => e.tipo === 'Observação').map(e => (
                        <div key={e.id_evento} className="glass-card" style={{ padding: '0.75rem 1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <div>
                            <div style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{e.descricao}: <span style={{ color: 'var(--color-primary)' }}>{e.valor} {e.unidade}</span></div>
                            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Coleta em {e.data_evento}</div>
                          </div>
                          <button 
                            onClick={() => handleViewFHIR('Observation', e.id_evento, `Observation: ${e.descricao}`)}
                            style={{ background: 'none', border: 'none', color: 'var(--color-estagiario)', cursor: 'pointer', fontSize: '0.75rem' }}
                          >
                            FHIR
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* FHIR Render */}
              {fhirData && (
                <FHIRVisualizer data={fhirData} title={fhirTitle} />
              )}
            </div>
          ) : (
            <div className="glass-panel" style={{ padding: '4rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
              Selecione um paciente supervisionado para acessar o prontuário.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default EstagiarioView;
