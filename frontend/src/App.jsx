import React, { useState, useEffect } from 'react';
import { api, getApiConfig, setApiConfig } from './services/api';
import MedicoView from './components/MedicoView';
import StagiarioView from './components/EstagiarioView';
import PesquisadorView from './components/PesquisadorView';
import ObservabilityView from './components/ObservabilityView';

import { 
  LogOut, 
  Settings, 
  Activity, 
  Users, 
  Sun, 
  Moon, 
  Lock, 
  Stethoscope, 
  KeyRound,
  Database
} from 'lucide-react';

const App = () => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [activeTab, setActiveTab] = useState('pacientes'); 
  const [theme, setTheme] = useState('dark');
  const [apiConfig, setApiConfigState] = useState(getApiConfig());
  
  
  const [showLogin, setShowLogin] = useState(true);

  
  const [loginUsername, setLoginUsername] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  const [loginError, setLoginError] = useState('');
  const [loginLoading, setLoginLoading] = useState(false);

  // API Config inputs
  const [inputIsMock, setInputIsMock] = useState(apiConfig.isMock);
  const [inputBaseUrl, setInputBaseUrl] = useState(apiConfig.baseUrl);
  const [settingsSuccess, setSettingsSuccess] = useState(false);

  // Apply theme to body
  useEffect(() => {
    const body = document.body;
    if (theme === 'light') {
      body.classList.add('light-theme');
    } else {
      body.classList.remove('light-theme');
    }
  }, [theme]);

  
  useEffect(() => {
    if (user) {
      if (user.role === 'PESQUISADOR') {
        setActiveTab('pesquisa');
      } else {
        setActiveTab('pacientes');
      }
    }
  }, [user]);

  const handleLoginSubmit = async (e) => {
    if (e) e.preventDefault();
    setLoginError('');
    setLoginLoading(true);
    try {
      const res = await api.login(loginUsername, loginPassword);
      setUser(res.user);
      setToken(res.token);
    } catch (err) {
      setLoginError(err.message);
    } finally {
      setLoginLoading(false);
    }
  };

  const handleQuickLogin = async (username) => {
    setLoginError('');
    setLoginLoading(true);
    try {
      const res = await api.login(username, apiConfig.isMock ? '123456' : 'PseudoPEP2026!');
      setUser(res.user);
      setToken(res.token);
    } catch (err) {
      setLoginError(err.message);
    } finally {
      setLoginLoading(false);
    }
  };

  const handleLogout = () => {
    setUser(null);
    setToken(null);
    setShowLogin(false);
  };

  const handleSaveSettings = (e) => {
    e.preventDefault();
    setApiConfig(inputIsMock, inputBaseUrl);
    setApiConfigState({ isMock: inputIsMock, baseUrl: inputBaseUrl });
    setSettingsSuccess(true);
    setTimeout(() => setSettingsSuccess(false), 3000);
  };

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg-primary)' }}>
      {}
      {!user ? (
        <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
          {}
          <div className="header glass-panel" style={{ 
            borderRadius: 0, 
            borderTop: 'none', 
            borderLeft: 'none', 
            borderRight: 'none',
            position: 'sticky',
            top: 0,
            zIndex: 100,
            padding: '0 2rem'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Stethoscope size={20} className="text-primary" />
              <span style={{ fontWeight: 'bold', fontFamily: 'var(--font-title)', fontSize: '1.1rem' }}>
                PSPD K8S Project
              </span>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              {}
              <button onClick={toggleTheme} className="btn btn-outline" style={{ borderRadius: '50%', padding: '0.5rem' }}>
                {theme === 'dark' ? <Sun size={15} /> : <Moon size={15} />}
              </button>

              {}
            </div>
          </div>

          {}
          <div style={{ 
            flexGrow: 1, 
            display: 'flex', 
            flexDirection: 'column', 
            alignItems: 'center', 
            justifyContent: 'center', 
            padding: '2rem',
            maxWidth: '1200px',
            width: '100%',
            margin: '0 auto'
          }}>
            {}
              <div style={{ 
                display: 'flex', 
                flexDirection: 'column', 
                alignItems: 'center', 
                width: '100%', 
                maxWidth: '480px',
                animation: 'fadeIn var(--transition-normal) forwards'
              }}>
                <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
                  <h1 style={{ fontSize: '1.8rem', marginBottom: '0.25rem', fontFamily: 'var(--font-title)' }}>
                    Portal Hospitalar FHIR
                  </h1>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
                    Identifique-se para acessar prontuários e painéis de observabilidade
                  </p>
                </div>

                {}
                <div className="glass-panel" style={{ width: '100%', padding: '2rem', marginBottom: '1.5rem' }}>
                  <h2 style={{ fontSize: '1.2rem', marginBottom: '1.25rem', textAlign: 'center' }}>Login do Usuário</h2>
                  
                  {loginError && (
                    <div style={{ 
                      background: 'var(--color-danger-glow)', 
                      border: '1px solid var(--color-danger)', 
                      color: 'var(--color-danger)',
                      padding: '0.75rem',
                      borderRadius: 'var(--radius-sm)',
                      fontSize: '0.85rem',
                      marginBottom: '1rem'
                    }}>
                      {loginError}
                    </div>
                  )}

                  <form onSubmit={handleLoginSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    <div>
                      <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', display: 'block', marginBottom: '0.3rem' }}>Usuário / Username</label>
                      <input 
                        type="text" 
                        value={loginUsername}
                        onChange={(e) => setLoginUsername(e.target.value)}
                        placeholder="Ex: dr.cardoso"
                        style={{
                          width: '100%',
                          padding: '0.6rem 0.8rem',
                          border: '1px solid var(--border-color)',
                          borderRadius: 'var(--radius-sm)',
                          background: 'var(--bg-primary)'
                        }}
                        required
                      />
                    </div>

                    <div>
                      <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', display: 'block', marginBottom: '0.3rem' }}>Senha / Password</label>
                      <input 
                        type="password" 
                        value={loginPassword}
                        onChange={(e) => setLoginPassword(e.target.value)}
                        placeholder="••••••••"
                        style={{
                          width: '100%',
                          padding: '0.6rem 0.8rem',
                          border: '1px solid var(--border-color)',
                          borderRadius: 'var(--radius-sm)',
                          background: 'var(--bg-primary)'
                        }}
                        required
                      />
                    </div>

                    <button 
                      type="submit" 
                      className="btn btn-primary" 
                      style={{ width: '100%', marginTop: '0.5rem' }}
                      disabled={loginLoading}
                    >
                      {loginLoading ? 'Conectando...' : 'Entrar via OAuth2'}
                    </button>
                  </form>
                </div>

                {}
                <div className="glass-panel" style={{ width: '100%', padding: '1.25rem' }}>
                  <h4 style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', textAlign: 'center', marginBottom: '0.8rem' }}>
                    Perfis de Atalho (Simular Keycloak)
                  </h4>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                    {}
                    <button 
                      onClick={() => handleQuickLogin('med.cardoso')}
                      className="btn btn-role-medico"
                      style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0.8rem', fontSize: '0.85rem' }}
                    >
                      <span>Entrar como Médico (FULL)</span>
                      <span style={{ fontSize: '0.75rem', opacity: 0.8 }}>med.cardoso</span>
                    </button>

                    {}
                    <button 
                      onClick={() => handleQuickLogin('est.ferreira')}
                      className="btn btn-role-estagiario"
                      style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0.8rem', fontSize: '0.85rem' }}
                    >
                      <span>Entrar como Estagiário (PARTIAL)</span>
                      <span style={{ fontSize: '0.75rem', opacity: 0.8 }}>est.ferreira</span>
                    </button>

                    {}
                    <button 
                      onClick={() => handleQuickLogin('pes.mendes')}
                      className="btn btn-role-pesquisador"
                      style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0.8rem', fontSize: '0.85rem' }}
                    >
                      <span>Entrar como Pesquisador (ANONYMIZED)</span>
                      <span style={{ fontSize: '0.75rem', opacity: 0.8 }}>pes.mendes</span>
                    </button>
                  </div>
                </div>
              </div>
          </div>
        </div>
      ) : (
                <div className="dashboard-layout">
          {}
          <div className="sidebar glass-panel" style={{ borderLeft: 'none', borderTop: 'none', borderBottom: 'none' }}>
            <div style={{ padding: '1.5rem', borderBottom: '1px solid var(--border-color)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Stethoscope size={20} className="text-primary" />
              <span style={{ fontWeight: 'bold', fontFamily: 'var(--font-title)', fontSize: '1.1rem' }}>Portal Clínico</span>
            </div>

            {}
            <div style={{ padding: '1.25rem', borderBottom: '1px solid var(--border-color)', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <img 
                src={user.avatar} 
                alt={user.name} 
                style={{ width: '42px', height: '42px', borderRadius: '50%', objectFit: 'cover', border: '2px solid var(--border-color)' }}
              />
              <div style={{ minWidth: 0 }}>
                <div style={{ fontWeight: 600, fontSize: '0.85rem', color: 'var(--text-primary)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{user.name}</div>
                <span className={`badge ${user.role === 'MEDICO' ? 'badge-medico' : user.role === 'ESTAGIARIO' ? 'badge-estagiario' : 'badge-pesquisador'}`} style={{ scale: '0.75', margin: '0.2rem 0 0 -5px', display: 'inline-flex' }}>
                  {user.role}
                </span>
              </div>
            </div>

            {}
            <div style={{ padding: '1rem', display: 'flex', flexDirection: 'column', gap: '0.25rem', flexGrow: 1 }}>
              {}
              {user.role !== 'PESQUISADOR' && (
                <button 
                  onClick={() => setActiveTab('pacientes')}
                  className={`btn ${activeTab === 'pacientes' ? 'btn-primary' : 'btn-outline'}`}
                  style={{ justifyContent: 'flex-start', width: '100%', fontSize: '0.85rem' }}
                >
                  <Users size={15} />
                  Pacientes
                </button>
              )}

              {}
              {user.role === 'PESQUISADOR' && (
                <button 
                  onClick={() => setActiveTab('pesquisa')}
                  className={`btn ${activeTab === 'pesquisa' ? 'btn-primary' : 'btn-outline'}`}
                  style={{ justifyContent: 'flex-start', width: '100%', fontSize: '0.85rem' }}
                >
                  <Database size={15} />
                  Pesquisa & Coortes
                </button>
              )}


              {}
              <button 
                onClick={() => setActiveTab('configuracoes')}
                className={`btn ${activeTab === 'configuracoes' ? 'btn-primary' : 'btn-outline'}`}
                style={{ justifyContent: 'flex-start', width: '100%', fontSize: '0.85rem' }}
              >
                <Settings size={15} />
                Configurações API
              </button>
            </div>

            {}
            <div style={{ padding: '1rem', borderTop: '1px solid var(--border-color)' }}>
              <button 
                onClick={handleLogout}
                className="btn btn-outline"
                style={{ width: '100%', justifyContent: 'center', borderColor: 'var(--color-danger-glow)', color: 'var(--color-danger)', fontSize: '0.85rem' }}
              >
                <LogOut size={15} />
                Desconectar
              </button>
            </div>
          </div>

          {}
          <div className="main-content">
            {}
            <div className="header glass-panel" style={{ borderTop: 'none', borderLeft: 'none', borderRight: 'none', padding: '0 2rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <span className={`badge ${apiConfig.isMock ? 'badge-medico' : 'badge-estagiario'}`} style={{ fontSize: '0.7rem' }}>
                  {apiConfig.isMock ? 'Demo: Mock Mode' : 'Connected: Live API'}
                </span>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  {apiConfig.isMock ? 'Executando regras localmente' : `Endpoint: ${apiConfig.baseUrl}`}
                </span>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                <button onClick={toggleTheme} className="btn btn-outline" style={{ borderRadius: '50%', padding: '0.5rem' }}>
                  {theme === 'dark' ? <Sun size={14} /> : <Moon size={14} />}
                </button>
              </div>
            </div>

            {}
            <div className="content-body">
              {activeTab === 'pacientes' && user.role === 'MEDICO' && (
                <MedicoView token={token} />
              )}

              {activeTab === 'pacientes' && user.role === 'ESTAGIARIO' && (
                <StagiarioView token={token} />
              )}

              {activeTab === 'pesquisa' && user.role === 'PESQUISADOR' && (
                <PesquisadorView token={token} />
              )}


              {activeTab === 'configuracoes' && (
                <div className="glass-panel animate-fade-in" style={{ padding: '2rem', maxWidth: '600px', margin: '0 auto' }}>
                  <h2 style={{ fontSize: '1.4rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <Settings size={22} className="text-primary" />
                    Configuração de Integração da API
                  </h2>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: '1.5rem' }}>
                    Alterne entre a simulação local (ideal para o GitHub Pages) e a integração real com o cluster Kubernetes rodando localmente ou na nuvem.
                  </p>

                  {settingsSuccess && (
                    <div style={{ background: 'var(--color-medico-glow)', border: '1px solid var(--color-medico)', color: 'var(--color-medico)', padding: '0.75rem', borderRadius: 'var(--radius-sm)', fontSize: '0.85rem', marginBottom: '1rem' }}>
                      Configurações salvas com sucesso! A página foi atualizada.
                    </div>
                  )}

                  <form onSubmit={handleSaveSettings} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                    <div>
                      <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontWeight: 600, fontSize: '0.9rem', cursor: 'pointer' }}>
                        <input 
                          type="checkbox" 
                          checked={inputIsMock}
                          onChange={(e) => setInputIsMock(e.target.checked)}
                          style={{ width: '18px', height: '18px' }}
                        />
                        Ativar Modo Simulação (Mock Mode / GitHub Pages)
                      </label>
                      <span style={{ display: 'block', fontSize: '0.75rem', color: 'var(--text-muted)', marginLeft: '1.65rem', marginTop: '0.2rem' }}>
                        Quando ativado, os dados e regras de autorização rodam diretamente no navegador, sem precisar do backend ativo.
                      </span>
                    </div>

                    <div>
                      <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', display: 'block', marginBottom: '0.3rem', fontWeight: 600 }}>
                        URL do API Gateway (Backend)
                      </label>
                      <input 
                        type="url" 
                        value={inputBaseUrl}
                        onChange={(e) => setInputBaseUrl(e.target.value)}
                        placeholder="http://localhost:8080/api"
                        style={{
                          width: '100%',
                          padding: '0.6rem 0.8rem',
                          border: '1px solid var(--border-color)',
                          borderRadius: 'var(--radius-sm)',
                          background: 'var(--bg-primary)',
                          fontFamily: 'var(--font-mono)'
                        }}
                        disabled={inputIsMock}
                        required={!inputIsMock}
                      />
                      <span style={{ display: 'block', fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.3rem' }}>
                        Endereço da rota base exposta pelo seu API Gateway no Kubernetes.
                      </span>
                    </div>

                    <button type="submit" className="btn btn-primary" style={{ alignSelf: 'flex-start', marginTop: '0.5rem' }}>
                      Salvar Alterações
                    </button>
                  </form>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
