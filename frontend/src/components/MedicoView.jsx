import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import FHIRVisualizer from './FHIRVisualizer';
import { Search, User, Calendar, Phone, FileText, Activity, ShieldAlert, Heart, Clipboard, Database } from 'lucide-react';

const MedicoView = ({ token }) => {
  const [patients, setPatients] = useState([]);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [patientRecord, setPatientRecord] = useState(null);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [fhirData, setFhirData] = useState(null);
  const [fhirTitle, setFhirTitle] = useState('');

  // Fetch list of doctor's assigned patients
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
          <h2 style={{ fontSize: '1.8rem', color: 'var(--color-medico)' }}>Painel do Médico</h2>
          <p style={{ color: 'var(--text-secondary)' }}>Acesso completo (FULL) aos prontuários eletrônicos sob sua responsabilidade.</p>
        </div>
        <span className="badge badge-medico">CRM Ativo • FULL ACCESS</span>
      </div>

      <div className="grid-main">
        {}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div className="glass-panel" style={{ padding: '1.25rem' }}>
            <h3 style={{ fontSize: '1.1rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Search size={18} />
              Buscar Paciente
            </h3>
            <div style={{ position: 'relative', marginBottom: '1.25rem' }}>
              <input 
                type="text"
                placeholder="Nome ou ID do paciente..."
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

            <h4 style={{ fontSize: '0.85rem', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.5rem' }}>Seus Pacientes</h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', maxHeight: '250px', overflowY: 'auto' }}>
              {filteredPatients.length === 0 ? (
                <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', padding: '0.5rem' }}>Nenhum paciente encontrado</p>
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
                      background: selectedPatient === p.id && !error ? 'var(--color-medico-glow)' : 'transparent',
                      border: `1px solid ${selectedPatient === p.id && !error ? 'var(--color-medico)' : 'var(--border-color)'}`,
                      textAlign: 'left',
                      cursor: 'pointer',
                      transition: 'all var(--transition-fast)'
                    }}
                  >
                    <div>
                      <div style={{ fontWeight: 600, fontSize: '0.95rem' }}>{p.name}</div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>ID: {p.id} • {p.gender === 'male' ? 'Masc' : 'Fem'}</div>
                    </div>
                    <User size={16} style={{ color: selectedPatient === p.id && !error ? 'var(--color-medico)' : 'var(--text-muted)' }} />
                  </button>
                ))
              )}
            </div>


          </div>
        </div>

        {}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {loading ? (
            <div className="glass-panel" style={{ padding: '4rem', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
              <div style={{ textAlign: 'center' }}>
                <div style={{ width: '40px', height: '40px', border: '3px solid var(--border-color)', borderTopColor: 'var(--color-medico)', borderRadius: '50%', animation: 'spin 1s linear infinite', margin: '0 auto 1rem' }}></div>
                <p style={{ color: 'var(--text-secondary)' }}>Carregando prontuário eletrônico...</p>
              </div>
            </div>
          ) : error ? (
                        <div className="glass-panel" style={{ padding: '3rem', border: '1px solid var(--color-danger)', background: 'rgba(244, 63, 94, 0.03)' }}>
              <div style={{ textAlign: 'center' }}>
                <ShieldAlert size={48} style={{ color: 'var(--color-danger)', marginBottom: '1rem' }} />
                <h3 style={{ fontSize: '1.4rem', color: 'var(--color-danger)', marginBottom: '0.5rem' }}>Acesso Negado (DENY)</h3>
                <p style={{ color: 'var(--text-primary)', maxWidth: '450px', margin: '0 auto 1rem', fontSize: '0.95rem' }}>
                  {error}
                </p>
                <div className="glass-card" style={{ maxWidth: '500px', margin: '1.5rem auto 0', padding: '1rem', background: 'rgba(0,0,0,0.2)', textAlign: 'left', fontSize: '0.8rem', fontFamily: 'var(--font-mono)' }}>
                  <div style={{ color: 'var(--color-danger)', fontWeight: 'bold', marginBottom: '0.5rem' }}>Decisão do Authorization Service:</div>
                  • Requisitante: dr.cardoso (Médico)<br />
                  • Recurso: Patient/{selectedPatient}<br />
                  • Vínculo na tabela user_patient_assignments: NÃO ENCONTRADO<br />
                  • Status: DENY (Acesso bloqueado por falta de vínculo clínico)
                </div>
              </div>
            </div>
          ) : patientRecord ? (
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
              {}
              <div className="glass-panel" style={{ padding: '1.5rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
                  <div>
                    <h3 style={{ fontSize: '1.5rem', marginBottom: '0.25rem' }}>{patientRecord.patient.name}</h3>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
                      <span>ID: {patientRecord.patient.id}</span>
                      <span>•</span>
                      <span style={{ textTransform: 'capitalize' }}>Sexo: {patientRecord.patient.gender === 'male' ? 'Masculino' : 'Feminino'}</span>
                    </p>
                  </div>
                  <button 
                    onClick={() => handleViewFHIR('Patient', patientRecord.patient.id, `Patient Resource: ${patientRecord.patient.name}`)}
                    className="btn btn-outline"
                    style={{ fontSize: '0.8rem', padding: '0.4rem 0.8rem', borderColor: 'var(--color-medico)', color: 'var(--color-medico)' }}
                  >
                    <Database size={14} />
                    Ver FHIR Patient
                  </button>
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
                  <div>
                    <div style={{ color: 'var(--text-muted)' }}>CPF</div>
                    <div style={{ fontWeight: 500, marginTop: '0.2rem' }}>{patientRecord.patient.cpf}</div>
                  </div>
                  <div>
                    <div style={{ color: 'var(--text-muted)' }}>CNS (Cartão Nacional de Saúde)</div>
                    <div style={{ fontWeight: 500, marginTop: '0.2rem' }}>{patientRecord.patient.cns}</div>
                  </div>
                  <div>
                    <div style={{ color: 'var(--text-muted)' }}>Telefone</div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', marginTop: '0.2rem' }}>
                      <Phone size={14} />
                      {patientRecord.patient.phone}
                    </div>
                  </div>
                </div>
                <div style={{ marginTop: '1rem', fontSize: '0.9rem' }}>
                  <div style={{ color: 'var(--text-muted)' }}>Endereço Completo</div>
                  <div style={{ marginTop: '0.2rem' }}>{patientRecord.patient.address}</div>
                </div>
              </div>

              {}
              <div className="glass-panel" style={{ padding: '1.5rem' }}>
                <h3 style={{ fontSize: '1.2rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--color-medico)' }}>
                  <Clipboard size={18} />
                  Resumo Clínico (Diagnósticos, Medicamentos e Exames)
                </h3>
                
                <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '1.5rem' }}>
                  {}
                  <div>
                    <h4 style={{ fontSize: '0.9rem', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.5rem' }}>Condições Clínicas Ativas</h4>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                      {patientRecord.events.filter(e => e.tipo === 'Condição').map(e => (
                        <div key={e.id_evento} className="glass-card" style={{ padding: '0.75rem 1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexGrow: 1 }}>
                          <div>
                            <div style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{e.descricao}</div>
                            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Código: {e.codigo} • Registrado em {e.data_evento}</div>
                          </div>
                          <button 
                            onClick={() => handleViewFHIR('Condition', e.id_evento, `Condition Resource: ${e.descricao}`)}
                            style={{ background: 'none', border: 'none', color: 'var(--color-medico)', cursor: 'pointer', fontSize: '0.75rem' }}
                          >
                            FHIR
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>

                  {}
                  <div>
                    <h4 style={{ fontSize: '0.9rem', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.5rem' }}>Prescrições Vigentes</h4>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                      {patientRecord.events.filter(e => e.tipo === 'Medicação').map(e => (
                        <div key={e.id_evento} className="glass-card" style={{ padding: '0.75rem 1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <div>
                            <div style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{e.descricao}</div>
                            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Código ATC: {e.codigo} • Prescrito em {e.data_evento}</div>
                          </div>
                          <button 
                            onClick={() => handleViewFHIR('MedicationRequest', e.id_evento, `MedicationRequest Resource: ${e.codigo}`)}
                            style={{ background: 'none', border: 'none', color: 'var(--color-medico)', cursor: 'pointer', fontSize: '0.75rem' }}
                          >
                            FHIR
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {}
              <div className="glass-panel" style={{ padding: '1.5rem' }}>
                <h3 style={{ fontSize: '1.2rem', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--color-medico)' }}>
                  <Activity size={18} />
                  Histórico Clínico (Linha do Tempo de Atendimentos)
                </h3>

                <div className="timeline">
                  {patientRecord.encounters.map(enc => {
                    const encEvents = patientRecord.events.filter(ev => ev.id_atendimento === enc.id);
                    return (
                      <div key={enc.id} className="timeline-item" style={{ '--timeline-color': 'var(--color-medico)' }}>
                        <div className="glass-card" style={{ padding: '1rem', background: 'rgba(255, 255, 255, 0.01)' }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                            <span style={{ fontWeight: 600, color: 'var(--text-primary)', fontSize: '1rem' }}>
                              Atendimento {enc.tipo} - {enc.setor}
                            </span>
                            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{enc.data_inicio}</span>
                          </div>
                          <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>
                            ID: {enc.id} • Duração: {enc.data_inicio} a {enc.data_fim}
                          </div>
                          
                          {}
                          {encEvents.length > 0 && (
                            <div style={{ borderLeft: '1px dashed var(--border-color)', paddingLeft: '0.75rem', display: 'flex', flexDirection: 'column', gap: '0.5rem', marginTop: '0.5rem' }}>
                              {encEvents.map(evt => (
                                <div key={evt.id_evento} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.8rem' }}>
                                  <div>
                                    <span className="badge" style={{
                                      fontSize: '0.6rem',
                                      padding: '0.1rem 0.4rem',
                                      background: evt.tipo === 'Condição' ? 'rgba(16,185,129,0.1)' : evt.tipo === 'Medicação' ? 'rgba(245,158,11,0.1)' : 'rgba(59,130,246,0.1)',
                                      color: evt.tipo === 'Condição' ? 'var(--color-medico)' : evt.tipo === 'Medicação' ? 'var(--color-estagiario)' : 'var(--color-primary)'
                                    }}>
                                      {evt.tipo}
                                    </span>
                                    <span style={{ marginLeft: '0.5rem', color: 'var(--text-primary)' }}>{evt.descricao}</span>
                                    {evt.valor && <strong style={{ color: 'var(--color-primary)' }}> {evt.valor} {evt.unidade}</strong>}
                                  </div>
                                  <button 
                                    onClick={() => handleViewFHIR(
                                      evt.tipo === 'Condição' ? 'Condition' : evt.tipo === 'Medicação' ? 'MedicationRequest' : 'Observation',
                                      evt.id_evento,
                                      `${evt.tipo} Resource: ${evt.descricao}`
                                    )}
                                    style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', fontSize: '0.7rem' }}
                                  >
                                    Ver FHIR
                                  </button>
                                </div>
                              ))}
                            </div>
                          )}
                          <div style={{ marginTop: '0.75rem', display: 'flex', justifyContent: 'flex-end' }}>
                            <button
                              onClick={() => handleViewFHIR('Encounter', enc.id, `Encounter Resource: ${enc.tipo}`)}
                              className="btn btn-outline"
                              style={{ padding: '0.2rem 0.5rem', fontSize: '0.7rem' }}
                            >
                              Ver FHIR Encounter
                            </button>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {}
              {fhirData && (
                <FHIRVisualizer data={fhirData} title={fhirTitle} />
              )}
            </div>
          ) : (
            <div className="glass-panel" style={{ padding: '4rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
              Selecione um paciente na lista para ver o prontuário.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MedicoView;
