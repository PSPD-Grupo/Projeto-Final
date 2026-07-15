import React, { useState } from 'react';
import { Copy, Check, FileCode } from 'lucide-react';

const FHIRVisualizer = ({ data, title }) => {
  const [copied, setCopied] = useState(false);

  const formatJson = (obj) => {
    return JSON.stringify(obj, null, 2);
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(formatJson(data));
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy text', err);
    }
  };

  
  const syntaxHighlight = (json) => {
    if (typeof json !== 'string') {
      json = formatJson(json);
    }
    
    
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?)/g, function (match) {
      let cls = 'fhir-number';
      if (/^"/.test(match)) {
        if (/:$/.test(match)) {
          cls = 'fhir-key';
        } else {
          cls = 'fhir-string';
        }
      } else if (/true|false/.test(match)) {
        cls = 'fhir-boolean';
      } else if (/null/.test(match)) {
        cls = 'fhir-null';
      }
      return `<span class="${cls}">${match}</span>`;
    });
  };

  if (!data) return null;

  return (
    <div className="glass-card animate-fade-in" style={{ padding: '1rem', marginTop: '1rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
        <h4 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', margin: 0, fontSize: '0.95rem' }}>
          <FileCode size={16} className="text-primary" />
          {title || "Recurso HL7/FHIR"}
        </h4>
        <button 
          onClick={handleCopy}
          className="btn btn-outline"
          style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem', borderRadius: '4px', display: 'flex', alignItems: 'center', gap: '0.25rem' }}
          title="Copiar JSON"
        >
          {copied ? (
            <>
              <Check size={12} style={{ color: 'var(--color-success)' }} />
              <span style={{ color: 'var(--color-success)' }}>Copiado!</span>
            </>
          ) : (
            <>
              <Copy size={12} />
              <span>Copiar</span>
            </>
          )}
        </button>
      </div>
      <pre 
        className="fhir-container"
        dangerouslySetInnerHTML={{ __html: syntaxHighlight(data) }}
      />
    </div>
  );
};

export default FHIRVisualizer;
