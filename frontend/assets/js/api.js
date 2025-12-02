const BASE_URL = 'http://localhost:8000/api/v1';

/**
 * @param {string} path 
 * @param {object} options 
 * @returns {Promise} 
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

    if (response.status === 204) {
      return null;
    }

    return await response.json();
  } catch (error) {
    console.error('Erro na requisição:', error);
    throw error;
  }
}


export const api = {

  get: (path) => request(path, { method: 'GET' }),


  post: (path, body) => request(path, { 
    method: 'POST', 
    body: JSON.stringify(body) 
  }),


  put: (path, body) => request(path, { 
    method: 'PUT', 
    body: JSON.stringify(body) 
  }),


  patch: (path, body) => request(path, { 
    method: 'PATCH', 
    body: JSON.stringify(body) 
  }),


  delete: (path) => request(path, { method: 'DELETE' })
};

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
