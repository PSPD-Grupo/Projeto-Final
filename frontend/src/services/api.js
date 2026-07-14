// API Service with Live API vs Mock Mode toggle

import {
  MOCK_USERS,
  MOCK_PATIENTS,
  MOCK_ASSIGNMENTS,
  MOCK_ENCOUNTERS,
  MOCK_CLINICAL_EVENTS,
  MOCK_PROJECTS,
  MOCK_COHORTS_STATS,
  MOCK_FHIR_RESOURCES
} from '../mockData';

// Configurable API Gateway URL for Live Mode
let API_BASE_URL = localStorage.getItem('API_BASE_URL') || 'http://localhost:8000';
let IS_MOCK_MODE = false; // Default to true for easy demo on GitHub Pages

export const getApiConfig = () => ({
  baseUrl: API_BASE_URL,
  isMock: IS_MOCK_MODE
});

export const setApiConfig = (isMock, baseUrl) => {
  IS_MOCK_MODE = isMock;
  API_BASE_URL = baseUrl;
  localStorage.setItem('IS_MOCK_MODE', isMock);
  localStorage.setItem('API_BASE_URL', baseUrl);
};

// Helper: Simulate delay for realistic feeling
const delay = (ms = 400) => new Promise(resolve => setTimeout(resolve, ms));

// Helper: Simple JWT parser simulation
const parseJwt = (token) => {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    return JSON.parse(jsonPayload);
  } catch (e) {
    return null;
  }
};

// Generate a simulated JWT token containing username, name and role
const generateSimulatedToken = (user) => {
  const header = btoa(JSON.stringify({ alg: "HS256", typ: "JWT" }));
  const payload = btoa(JSON.stringify({
    sub: user.username,
    name: user.name,
    role: user.role,
    exp: Math.floor(Date.now() / 1000) + (60 * 60) // 1 hour expiration
  }));
  const signature = "simulated_signature";
  return `${header}.${payload}.${signature}`;
};

export const api = {
  // 1. Authentication
  login: async (username, password) => {
    await delay(600);
    if (!IS_MOCK_MODE) {
      // Live Mode Call to Keycloak / Gateway
      try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, password })
        });
        if (!response.ok) throw new Error('Credenciais inválidas');

        const data = await response.json();
        // Real API returns { access_token, refresh_token, expires_at }
        const token = data.access_token;
        const decoded = parseJwt(token);
        if (!decoded) throw new Error('Token inválido recebido do servidor');

        // Build the user object from the token payload
        const user = {
          username: decoded.sub,
          name: decoded.name || decoded.sub, // Fallback if name is not in JWT
          role: decoded.role || 'MEDICO'
        };

        return { token, user };
      } catch (err) {
        throw new Error(err.message || 'Falha ao conectar ao servidor de autenticação');
      }
    }

    // Mock Mode
    const user = MOCK_USERS[username.toLowerCase()];
    if (user && password === '123456') { // Simple default password for all mock accounts
      const token = generateSimulatedToken(user);
      return { token, user };
    }
    throw new Error('Usuário ou senha inválidos. Utilize a senha padrão "123456" ou selecione um perfil de atalho.');
  },

  // 2. Fetch Patients List based on active role
  getPatients: async (token) => {
    await delay(500);
    if (!IS_MOCK_MODE) {
      const response = await fetch(`${API_BASE_URL}/patients`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!response.ok) {
        if (response.status === 403) throw new Error('Acesso negado');
        throw new Error('Erro ao buscar pacientes');
      }
      const data = await response.json();
      return data.map(p => ({
        ...p,
        id: p.patient_ref || p.id,
        name: p.full_name || p.name || p.initials || 'Paciente Oculto',
        gender: p.gender === 'M' ? 'male' : p.gender === 'F' ? 'female' : p.gender
      }));
    }

    // Mock Mode Authorization & Filtering Logic
    const decoded = parseJwt(token);
    if (!decoded) throw new Error('Token JWT inválido ou ausente');
    const { sub: username, role } = decoded;

    if (role === 'MEDICO') {
      // Return patients assigned to this doctor
      const assignedIds = MOCK_ASSIGNMENTS
        .filter(a => a.caregiver === username && a.type === 'MEDICO' && a.status === 'ATIVO')
        .map(a => a.id_paciente);

      return Object.values(MOCK_PATIENTS).filter(p => assignedIds.includes(p.id));
    }

    if (role === 'ESTAGIARIO') {
      // Return patients assigned to supervised activity
      const assignedIds = MOCK_ASSIGNMENTS
        .filter(a => a.caregiver === username && a.type === 'ESTAGIARIO' && a.status === 'ATIVO')
        .map(a => a.id_paciente);

      const rawPatients = Object.values(MOCK_PATIENTS).filter(p => assignedIds.includes(p.id));

      // Data Transform Service Action: Mask sensitive fields!
      return rawPatients.map(p => ({
        ...p,
        name: p.name.split(' ').map((word, i) => i === 0 ? word : word[0] + '...').join(' '), // Initials only
        cpf: '***.***.***-**',
        cns: '***************',
        phone: '(61) 9****-****',
        address: p.address.split(',').slice(-2).join(', ').trim() // Show city/state only
      }));
    }

    if (role === 'PESQUISADOR') {
      // Researchers do not get raw patient lists (Acesso ANONYMIZED ou AGGREGATED apenas)
      throw new Error('Acesso negado: Pesquisadores não possuem permissão para listar prontuários diretos de pacientes.');
    }

    throw new Error('Papel de usuário desconhecido');
  },

  // 3. Fetch Patient clinical timeline and events
  getPatientDetails: async (patientId, token) => {
    await delay(600);
    if (!IS_MOCK_MODE) {
      const response = await fetch(`${API_BASE_URL}/patients/${patientId}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!response.ok) {
        if (response.status === 403) throw new Error('Acesso negado');
        throw new Error('Erro ao buscar prontuário');
      }
      const data = await response.json();
      return {
        patient: {
          ...data.patient,
          id: data.patient?.patient_ref || data.patient?.id,
          name: data.patient?.full_name || data.patient?.name || data.patient?.initials || 'Paciente Oculto',
          gender: data.patient?.gender === 'M' ? 'male' : data.patient?.gender === 'F' ? 'female' : data.patient?.gender
        },
        encounters: (data.encounters || []).map(e => ({
          ...e,
          id: e.encounter_id || e.id,
          tipo: e.encounter_type || e.tipo,
          setor: e.department || e.setor,
          data_inicio: e.start_date || e.data_inicio,
          data_fim: e.end_date || e.data_fim || 'Atual'
        })),
        events: (data.events || []).map(e => ({
          ...e,
          id_evento: e.event_id || e.id_evento,
          id_atendimento: e.encounter_id || e.id_atendimento,
          tipo: e.event_type === 'CONDITION' ? 'Condição' : e.event_type === 'OBSERVATION' ? 'Observação' : e.event_type === 'MEDICATION' ? 'Medicação' : e.event_type || e.tipo,
          codigo: e.code || e.codigo,
          descricao: e.description || e.descricao,
          data_evento: e.event_date || e.data_evento,
          valor: e.value || e.valor,
          unidade: e.unit || e.unidade
        }))
      };
    }

    // Mock Mode detailed verification & masking
    const decoded = parseJwt(token);
    if (!decoded) throw new Error('Token JWT inválido');
    const { sub: username, role } = decoded;

    // Check relationship
    const hasAssignment = MOCK_ASSIGNMENTS.some(a =>
      a.caregiver === username &&
      a.id_paciente === patientId &&
      a.status === 'ATIVO' &&
      a.type === role
    );

    if (!hasAssignment) {
      // Authorization Service simulation: Return DENY
      throw new Error(`Acesso negado (DENY): Usuário '${username}' com papel '${role}' não possui vínculo ativo com o paciente '${patientId}'.`);
    }

    let patient = MOCK_PATIENTS[patientId];
    if (role === 'ESTAGIARIO') {
      // Data Transform Service: Masking data (PARTIAL access)
      patient = {
        ...patient,
        name: patient.name.split(' ').map((word, i) => i === 0 ? word : word[0] + '...').join(' '),
        cpf: '***.***.***-**',
        cns: '***************',
        phone: '(61) 9****-****',
        address: patient.address.split(',').slice(-2).join(', ').trim()
      };
    }

    const encounters = MOCK_ENCOUNTERS.filter(e => e.id_paciente === patientId);
    const events = MOCK_CLINICAL_EVENTS.filter(ev => ev.id_paciente === patientId);

    return { patient, encounters, events };
  },

  // 4. Researchers specific: Cohorts filter
  getCohortData: async (cohortCode, projectId, token) => {
    await delay(600);
    if (!IS_MOCK_MODE) {
      const response = await fetch(`${API_BASE_URL}/cohorts?code=${cohortCode}&projectId=${projectId}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!response.ok) {
        if (response.status === 403) throw new Error('Acesso negado (Projeto não aprovado/vigente)');
        throw new Error('Erro ao buscar dados do coorte');
      }
      const data = await response.json();
      
      const menPct = (data.gender_distribution || []).find(g => g.label === 'M' || g.label === 'male')?.percentage || 0;
      const womenPct = (data.gender_distribution || []).find(g => g.label === 'F' || g.label === 'female')?.percentage || 0;
      
      const ageBands = (data.age_distribution || []).map(a => ({
        label: a.label,
        value: Math.round(a.percentage)
      }));
      
      const departments = (data.department_distribution || []).map(d => ({
        name: d.label,
        pct: Math.round(d.percentage)
      }));

      return {
        totalCases: data.total_patients || 0,
        demographics: {
          men: Math.round(menPct),
          women: Math.round(womenPct),
          ageBands: ageBands.length ? ageBands : [{ label: 'N/A', value: 0 }]
        },
        departments: departments.length ? departments : [{ name: 'N/A', pct: 0 }],
        anonymizedPatients: [] 
      };
    }

    // Mock Mode Researcher rules
    const decoded = parseJwt(token);
    if (!decoded || decoded.role !== 'PESQUISADOR') throw new Error('Acesso permitido apenas para pesquisadores');

    const project = MOCK_PROJECTS.find(p => p.id_projeto === projectId);
    if (!project) throw new Error('Projeto não encontrado');

    // Rule: "O pesquisador só pode acessar se o projeto estiver aprovado e vigente"
    if (project.status !== 'Aprovado') {
      throw new Error(`Acesso negado (DENY): O projeto '${projectId}' (${project.titulo}) está com status '${project.status}' (Não vigente).`);
    }

    if (project.codigo_condicao !== cohortCode) {
      throw new Error(`Acesso negado (DENY): O projeto '${projectId}' está vinculado ao coorte de '${project.codigo_condicao}' e não '${cohortCode}'.`);
    }

    const stats = MOCK_COHORTS_STATS[cohortCode];
    if (!stats) throw new Error('Dados de coorte não cadastrados');

    return stats;
  },

  // 5. Fetch Projects List
  getProjects: async (token) => {
    await delay(300);
    if (!IS_MOCK_MODE) {
      const response = await fetch(`${API_BASE_URL}/projects`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!response.ok) throw new Error('Erro ao buscar projetos');
      const data = await response.json();
      return data.map(p => ({
        id_projeto: p.project_id,
        titulo: p.title,
        pesquisador: p.researcher_username,
        codigo_condicao: p.target_condition_code,
        status: p.status === 'APPROVED' ? 'Aprovado' : p.status
      }));
    }

    const decoded = parseJwt(token);
    if (!decoded) throw new Error('Não autenticado');
    return MOCK_PROJECTS.filter(p => p.pesquisador === decoded.sub);
  },

  // 6. Fetch FHIR JSON format
  getFHIRResource: async (resourceType, id, token) => {
    await delay(400);
    if (!IS_MOCK_MODE) {
      const response = await fetch(`${API_BASE_URL}/fhir/${resourceType}/${id}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!response.ok) throw new Error('Erro ao buscar recurso FHIR');
      return await response.json();
    }

    // Mock Mode FHIR dictionary lookup
    const list = MOCK_FHIR_RESOURCES[resourceType];
    if (list && list[id]) {
      return list[id];
    }

    // Otherwise fallback/generate a minimal FHIR representation dynamically
    if (resourceType === 'Patient') {
      const p = MOCK_PATIENTS[id];
      if (p) {
        return {
          resourceType: "Patient",
          id: p.id,
          name: [{ text: p.name }],
          gender: p.gender,
          birthDate: p.birth_date
        };
      }
    }

    // Default dynamic mock FHIR
    const event = MOCK_CLINICAL_EVENTS.find(e => e.id_evento === id);
    if (event) {
      if (resourceType === 'Condition') {
        return {
          resourceType: "Condition",
          id: event.id_evento,
          clinicalStatus: { coding: [{ code: "active" }] },
          code: { text: event.descricao },
          subject: { reference: `Patient/${event.id_paciente}` }
        };
      }
      if (resourceType === 'MedicationRequest') {
        return {
          resourceType: "MedicationRequest",
          id: event.id_evento,
          status: "active",
          intent: "order",
          medicationCodeableConcept: { text: event.descricao },
          subject: { reference: `Patient/${event.id_paciente}` }
        };
      }
    }

    throw new Error(`Recurso FHIR '${resourceType}/${id}' não disponível.`);
  }
};
