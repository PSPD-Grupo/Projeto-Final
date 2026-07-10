// Mock Data for the Portal Hospitalar HL7/FHIR & Observabilidade K8S

export const MOCK_USERS = {
  "dr.cardoso": {
    username: "dr.cardoso",
    name: "Dr. Henrique Cardoso",
    role: "MEDICO",
    crm: "DF-12345",
    supervisorOf: ["est.barros"],
    avatar: "https://images.unsplash.com/photo-1537368910025-700350fe46c7?auto=format&fit=crop&q=80&w=150"
  },
  "est.barros": {
    username: "est.barros",
    name: "Daniel Barros (Estagiário)",
    role: "ESTAGIARIO",
    supervisor: "dr.cardoso",
    avatar: "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&q=80&w=150"
  },
  "pesq.fonseca": {
    username: "pesq.fonseca",
    name: "Pedro Fonseca (Pesquisador)",
    role: "PESQUISADOR",
    institution: "Universidade de Brasília (UnB)",
    avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=150"
  }
};

// Database Patients (raw representation)
export const MOCK_PATIENTS = {
  "P000001": {
    id: "P000001",
    name: "João da Silva",
    birth_date: "1970-05-10",
    gender: "male",
    cpf: "123.456.789-00",
    cns: "898000123456789",
    phone: "(61) 98765-4321",
    address: "Quadra 104 Sul, Alameda 2, Lote 14, Brasília, DF"
  },
  "P000002": {
    id: "P000002",
    name: "Maria Santos Oliveira",
    birth_date: "1985-08-22",
    gender: "female",
    cpf: "234.567.890-11",
    cns: "898000234567890",
    phone: "(61) 99876-5432",
    address: "SQN 206, Bloco G, Apt 304, Asa Norte, Brasília, DF"
  },
  "P000003": {
    id: "P000003",
    name: "Carlos Augusto de Souza",
    birth_date: "1962-03-15",
    gender: "male",
    cpf: "345.678.901-22",
    cns: "898000345678901",
    phone: "(61) 98877-6655",
    address: "Av. Central, Lote 45, Taguatinga Centro, DF"
  },
  "P000004": {
    id: "P000004",
    name: "Francisca das Chagas Lima",
    birth_date: "1953-11-30",
    gender: "female",
    cpf: "456.789.012-33",
    cns: "898000456789012",
    phone: "(61) 97766-5544",
    address: "Setor de Mansões Leste, Chácara 12, Sobradinho, DF"
  }
};

// User Patient Assignments (Authorization linkages)
// Doctor P000001, P000002, P000003
// Intern P000001, P000002
export const MOCK_ASSIGNMENTS = [
  { id: "V001", caregiver: "dr.cardoso", id_paciente: "P000001", type: "MEDICO", supervisor: null, status: "ATIVO" },
  { id: "V002", caregiver: "dr.cardoso", id_paciente: "P000002", type: "MEDICO", supervisor: null, status: "ATIVO" },
  { id: "V003", caregiver: "dr.cardoso", id_paciente: "P000003", type: "MEDICO", supervisor: null, status: "ATIVO" },
  { id: "V004", caregiver: "est.barros", id_paciente: "P000001", type: "ESTAGIARIO", supervisor: "dr.cardoso", status: "ATIVO" },
  { id: "V005", caregiver: "est.barros", id_paciente: "P000002", type: "ESTAGIARIO", supervisor: "dr.cardoso", status: "ATIVO" }
  // Note: P000003 is NOT assigned to est.barros (returns DENY)
  // Note: P000004 is NOT assigned to dr.cardoso or est.barros (returns DENY)
];

// Encounters (Atendimentos)
export const MOCK_ENCOUNTERS = [
  { id: "E000001", id_paciente: "P000001", data_inicio: "2026-02-10", data_fim: "2026-02-10", tipo: "Ambulatorial", setor: "Cardiologia" },
  { id: "E000002", id_paciente: "P000001", data_inicio: "2026-04-18", data_fim: "2026-04-20", tipo: "Internação", setor: "Cardiologia" },
  { id: "E000003", id_paciente: "P000002", data_inicio: "2026-03-15", data_fim: "2026-03-15", tipo: "Ambulatorial", setor: "Endocrinologia" },
  { id: "E000004", id_paciente: "P000003", data_inicio: "2026-05-20", data_fim: "2026-05-20", tipo: "Emergência", setor: "Clínica Médica" }
];

// Clinical Events
export const MOCK_CLINICAL_EVENTS = [
  // Patient 1 - Encounter 1
  { id_evento: "EV001", id_paciente: "P000001", id_atendimento: "E000001", tipo: "Condição", codigo: "Hipertensão", descricao: "Hipertensão Arterial Sistêmica", data_evento: "2026-02-10" },
  { id_evento: "EV002", id_paciente: "P000001", id_atendimento: "E000001", tipo: "Medicação", codigo: "Losartana", descricao: "Losartana Potássica 50mg, via oral, uma vez ao dia", data_evento: "2026-02-10" },
  // Patient 1 - Encounter 2
  { id_evento: "EV003", id_paciente: "P000001", id_atendimento: "E000002", tipo: "Observação", codigo: "Pressão Arterial", descricao: "Pressão Arterial aferida na internação: 150/95 mmHg", data_evento: "2026-04-18", valor: "150/95", unidade: "mmHg" },
  // Patient 2 - Encounter 3
  { id_evento: "EV004", id_paciente: "P000002", id_atendimento: "E000003", tipo: "Condição", codigo: "Diabetes", descricao: "Diabetes Mellitus Tipo 2", data_evento: "2026-03-15" },
  { id_evento: "EV005", id_paciente: "P000002", id_atendimento: "E000003", tipo: "Medicação", codigo: "Metformina", descricao: "Cloridrato de Metformina 850mg, via oral, duas vezes ao dia", data_evento: "2026-03-15" },
  { id_evento: "EV006", id_paciente: "P000002", id_atendimento: "E000003", tipo: "Observação", codigo: "Glicemia", descricao: "Glicemia de jejum", data_evento: "2026-03-15", valor: "182", unidade: "mg/dL" },
  { id_evento: "EV007", id_paciente: "P000002", id_atendimento: "E000003", tipo: "Observação", codigo: "HbA1c", descricao: "Hemoglobina Glicada", data_evento: "2026-03-15", valor: "8.1", unidade: "%" },
  { id_evento: "EV008", id_paciente: "P000002", id_atendimento: "E000003", tipo: "Observação", codigo: "IMC", descricao: "Índice de Massa Corporal", data_evento: "2026-03-15", valor: "31.2", unidade: "kg/m²" },
  // Patient 3 - Encounter 4
  { id_evento: "EV009", id_paciente: "P000003", id_atendimento: "E000004", tipo: "Condição", codigo: "Pneumonia", descricao: "Pneumonia Comunitária Aguda", data_evento: "2026-05-20" },
  { id_evento: "EV010", id_paciente: "P000003", id_atendimento: "E000004", tipo: "Medicação", codigo: "Amoxicilina", descricao: "Amoxicilina + Clavulanato de Potássio 875mg + 125mg, via oral, a cada 12h por 7 dias", data_evento: "2026-05-20" }
];

// Research Projects
export const MOCK_PROJECTS = [
  { id_projeto: "PRJ01", titulo: "Estudo Epidemiológico de Diabetes em Jovens e Adultos", pesquisador: "pesq.fonseca", codigo_condicao: "Diabetes", status: "Aprovado", validade: "2028-12-31" },
  { id_projeto: "PRJ02", titulo: "Análise de Hipertensão Arterial e Fatores de Risco na Atenção Primária", pesquisador: "pesq.fonseca", codigo_condicao: "Hipertensão", status: "Aprovado", validade: "2027-06-30" },
  { id_projeto: "PRJ03", titulo: "Pesquisa Experimental de Obesidade e Perfil Glicêmico", pesquisador: "pesq.fonseca", codigo_condicao: "Obesidade", status: "Suspenso", validade: "2025-01-01" }
];

// Pre-generated FHIR Resources for Demo Mode Visualizer
export const MOCK_FHIR_RESOURCES = {
  Patient: {
    "P000001": {
      "resourceType": "Patient",
      "id": "P000001",
      "active": true,
      "name": [
        {
          "use": "official",
          "family": "Silva",
          "given": ["João"],
          "text": "João da Silva"
        }
      ],
      "telecom": [
        { "system": "phone", "value": "(61) 98765-4321", "use": "mobile" }
      ],
      "gender": "male",
      "birthDate": "1970-05-10",
      "address": [
        {
          "line": ["Quadra 104 Sul, Alameda 2, Lote 14"],
          "city": "Brasília",
          "state": "DF",
          "country": "Brazil"
        }
      ],
      "identifier": [
        { "system": "http://gov.br/cpf", "value": "123.456.789-00" },
        { "system": "http://gov.br/cns", "value": "898000123456789" }
      ]
    },
    "P000002": {
      "resourceType": "Patient",
      "id": "P000002",
      "active": true,
      "name": [
        {
          "use": "official",
          "family": "Oliveira",
          "given": ["Maria", "Santos"],
          "text": "Maria Santos Oliveira"
        }
      ],
      "telecom": [
        { "system": "phone", "value": "(61) 99876-5432", "use": "mobile" }
      ],
      "gender": "female",
      "birthDate": "1985-08-22",
      "address": [
        {
          "line": ["SQN 206, Bloco G, Apt 304, Asa Norte"],
          "city": "Brasília",
          "state": "DF",
          "country": "Brazil"
        }
      ],
      "identifier": [
        { "system": "http://gov.br/cpf", "value": "234.567.890-11" },
        { "system": "http://gov.br/cns", "value": "898000234567890" }
      ]
    }
  },
  Encounter: {
    "E000001": {
      "resourceType": "Encounter",
      "id": "E000001",
      "status": "finished",
      "class": {
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
        "code": "AMB",
        "display": "ambulatory"
      },
      "subject": { "reference": "Patient/P000001" },
      "period": { "start": "2026-02-10T09:00:00-03:00", "end": "2026-02-10T09:30:00-03:00" },
      "serviceProvider": { "display": "Departamento de Cardiologia" }
    },
    "E000003": {
      "resourceType": "Encounter",
      "id": "E000003",
      "status": "finished",
      "class": {
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
        "code": "AMB",
        "display": "ambulatory"
      },
      "subject": { "reference": "Patient/P000002" },
      "period": { "start": "2026-03-15T14:00:00-03:00", "end": "2026-03-15T14:45:00-03:00" },
      "serviceProvider": { "display": "Departamento de Endocrinologia" }
    }
  },
  Condition: {
    "EV001": {
      "resourceType": "Condition",
      "id": "EV001",
      "clinicalStatus": {
        "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active" }]
      },
      "verificationStatus": {
        "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status", "code": "confirmed" }]
      },
      "code": {
        "coding": [{ "system": "http://hl7.org/fhir/sid/icd-10", "code": "I10", "display": "Hipertensão essencial (primária)" }],
        "text": "Hipertensão Arterial Sistêmica"
      },
      "subject": { "reference": "Patient/P000001" },
      "encounter": { "reference": "Encounter/E000001" },
      "recordedDate": "2026-02-10"
    },
    "EV004": {
      "resourceType": "Condition",
      "id": "EV004",
      "clinicalStatus": {
        "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active" }]
      },
      "verificationStatus": {
        "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status", "code": "confirmed" }]
      },
      "code": {
        "coding": [{ "system": "http://hl7.org/fhir/sid/icd-10", "code": "E11", "display": "Diabetes mellitus não-insulino-dependente" }],
        "text": "Diabetes Mellitus Tipo 2"
      },
      "subject": { "reference": "Patient/P000002" },
      "encounter": { "reference": "Encounter/E000003" },
      "recordedDate": "2026-03-15"
    }
  },
  Observation: {
    "EV003": {
      "resourceType": "Observation",
      "id": "EV003",
      "status": "final",
      "code": {
        "coding": [{ "system": "http://loinc.org", "code": "85354-9", "display": "Blood pressure panel" }],
        "text": "Pressão Arterial"
      },
      "subject": { "reference": "Patient/P000001" },
      "encounter": { "reference": "Encounter/E000002" },
      "effectiveDateTime": "2026-04-18",
      "valueQuantity": { "value": 150, "unit": "mmHg" }
    },
    "EV007": {
      "resourceType": "Observation",
      "id": "EV007",
      "status": "final",
      "code": {
        "coding": [{ "system": "http://loinc.org", "code": "4548-4", "display": "Hemoglobin A1c/Hemoglobin.total in Blood" }],
        "text": "Hemoglobina Glicada (HbA1c)"
      },
      "subject": { "reference": "Patient/P000002" },
      "encounter": { "reference": "Encounter/E000003" },
      "effectiveDateTime": "2026-03-15",
      "valueQuantity": { "value": 8.1, "unit": "%", "system": "http://unitsofmeasure.org", "code": "%" }
    }
  },
  MedicationRequest: {
    "EV002": {
      "resourceType": "MedicationRequest",
      "id": "EV002",
      "status": "active",
      "intent": "order",
      "medicationCodeableConcept": {
        "coding": [{ "system": "http://www.whocc.no/atc", "code": "C09CA01", "display": "Losartan" }],
        "text": "Losartana Potássica 50mg"
      },
      "subject": { "reference": "Patient/P000001" },
      "encounter": { "reference": "Encounter/E000001" },
      "authoredOn": "2026-02-10",
      "dosageInstruction": [
        { "text": "Tomar uma vez ao dia via oral" }
      ]
    },
    "EV005": {
      "resourceType": "MedicationRequest",
      "id": "EV005",
      "status": "active",
      "intent": "order",
      "medicationCodeableConcept": {
        "coding": [{ "system": "http://www.whocc.no/atc", "code": "A10BA02", "display": "Metformin" }],
        "text": "Cloridrato de Metformina 850mg"
      },
      "subject": { "reference": "Patient/P000002" },
      "encounter": { "reference": "Encounter/E000003" },
      "authoredOn": "2026-03-15",
      "dosageInstruction": [
        { "text": "Tomar duas vezes ao dia via oral junto às refeições" }
      ]
    }
  }
};

// Cohort & Statistics Mock Data for Researchers
export const MOCK_COHORTS_STATS = {
  "Diabetes": {
    totalCases: 14238,
    demographics: {
      men: 30,
      women: 70,
      ageBands: [
        { label: "18-39", value: 12 },
        { label: "40-59", value: 44 },
        { label: "60+", value: 44 }
      ]
    },
    departments: [
      { name: "Endocrinologia", pct: 55 },
      { name: "Clínica Médica", pct: 30 },
      { name: "Cardiologia", pct: 15 }
    ],
    anonymizedPatients: [
      { hash: "hash001", gender: "F", age: 63, exams: "HbA1c=8.1, Glicemia=182 mg/dL, IMC=31.2" },
      { hash: "hash002", gender: "M", age: 58, exams: "HbA1c=7.2, Glicemia=150 mg/dL, IMC=28.4" },
      { hash: "hash005", gender: "F", age: 41, exams: "HbA1c=6.9, Glicemia=138 mg/dL, IMC=26.8" },
      { hash: "hash009", gender: "F", age: 67, exams: "HbA1c=8.8, Glicemia=201 mg/dL, IMC=32.9" },
      { hash: "hash012", gender: "M", age: 49, exams: "HbA1c=7.0, Glicemia=144 mg/dL, IMC=29.1" }
    ]
  },
  "Hipertensão": {
    totalCases: 8520,
    demographics: {
      men: 48,
      women: 52,
      ageBands: [
        { label: "18-39", value: 5 },
        { label: "40-59", value: 35 },
        { label: "60+", value: 60 }
      ]
    },
    departments: [
      { name: "Cardiologia", pct: 65 },
      { name: "Clínica Médica", pct: 20 },
      { name: "Geriatria", pct: 15 }
    ],
    anonymizedPatients: [
      { hash: "hash003", gender: "M", age: 72, exams: "PA=155/96 mmHg, Creatinina=1.1 mg/dL" },
      { hash: "hash004", gender: "F", age: 65, exams: "PA=142/88 mmHg, Creatinina=0.9 mg/dL" },
      { hash: "hash007", gender: "M", age: 50, exams: "PA=138/90 mmHg, Creatinina=1.0 mg/dL" },
      { hash: "hash011", gender: "F", age: 61, exams: "PA=149/92 mmHg, Creatinina=0.8 mg/dL" }
    ]
  }
};

// K8S Observability Statistics for each Load Scenario
// Scenarios: 10, 50, 100, 500, 1000 simultaneous users
export const MOCK_OBSERVABILITY_DATA = {
  10: {
    throughput: 120, // req/sec
    latency: 18, // ms
    errorRate: 0.0, // %
    cpuUsage: 14, // % average per pod
    memUsage: 35, // % average per pod
    pods: 1, // replica count
    scaleEvent: "Estável (mínimo de réplicas)"
  },
  50: {
    throughput: 580,
    latency: 24,
    errorRate: 0.0,
    cpuUsage: 38,
    memUsage: 45,
    pods: 1,
    scaleEvent: "Estável"
  },
  100: {
    throughput: 1120,
    latency: 38,
    errorRate: 0.1,
    cpuUsage: 72, // HPA threshold crossed (>70% CPU)
    memUsage: 58,
    pods: 2, // Scales up to 2
    scaleEvent: "HPA ativado: Pods escalados de 1 para 2"
  },
  500: {
    throughput: 4950,
    latency: 85,
    errorRate: 0.3,
    cpuUsage: 81,
    memUsage: 64,
    pods: 5, // Scales up to 5
    scaleEvent: "HPA ativado: Pods escalados de 2 para 5"
  },
  1000: {
    throughput: 9210,
    latency: 195,
    errorRate: 1.4,
    cpuUsage: 89,
    memUsage: 78,
    pods: 10, // Scales to max (10 replicas)
    scaleEvent: "Tráfego Máximo: Replicas escaladas para o limite (10 pods)"
  }
};
