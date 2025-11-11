// Módulo API - Wrapper para requisições à API Django
const BASE_URL = 'http://localhost:8000/api/v1';

/**
 * Realiza requisição HTTP à API
 * @param {string} path - Caminho do endpoint (ex: '/alunos/')
 * @param {object} options - Opções do fetch
 * @returns {Promise} - Resposta JSON ou null
 */
async function request(path, options = {}) {
  try {
    const response = await fetch(`${BASE_URL}${path}`, {
      headers: { 
        'Content-Type': 'application/json',
        ...(options.headers || {})
      },
      ...options
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Erro ${response.status}: ${errorText}`);
    }

    // Resposta 204 No Content (DELETE)
    if (response.status === 204) {
      return null;
    }

    return await response.json();
  } catch (error) {
    console.error('Erro na requisição:', error);
    throw error;
  }
}

/**
 * API com métodos HTTP
 */
export const api = {
  /**
   * GET - Buscar dados
   */
  get: (path) => request(path, { method: 'GET' }),

  /**
   * POST - Criar novo recurso
   */
  post: (path, body) => request(path, { 
    method: 'POST', 
    body: JSON.stringify(body) 
  }),

  /**
   * PUT - Atualizar recurso completo
   */
  put: (path, body) => request(path, { 
    method: 'PUT', 
    body: JSON.stringify(body) 
  }),

  /**
   * PATCH - Atualizar recurso parcialmente
   */
  patch: (path, body) => request(path, { 
    method: 'PATCH', 
    body: JSON.stringify(body) 
  }),

  /**
   * DELETE - Remover recurso
   */
  delete: (path) => request(path, { method: 'DELETE' })
};

/**
 * Utilitários para mensagens de feedback
 */
export const feedback = {
  success: (message) => {
    alert(`✅ ${message}`);
  },
  
  error: (message) => {
    alert(`❌ ${message}`);
  },
  
  confirm: (message) => {
    return confirm(`⚠️ ${message}`);
  }
};
