// Redirect if already logged in
if (getUser()) window.location.href = 'index.html';

renderNav();

function showLogin() {
  document.getElementById('loginSection').style.display = 'block';
  document.getElementById('registerSection').style.display = 'none';
  document.title = 'Login – CineApp';
}

function showRegister() {
  document.getElementById('loginSection').style.display = 'none';
  document.getElementById('registerSection').style.display = 'block';
  document.title = 'Register – CineApp';
}

function showError(id, msg) {
  const el = document.getElementById(id);
  el.textContent = msg;
  el.style.display = 'block';
}

function clearError(id) {
  const el = document.getElementById(id);
  el.textContent = '';
  el.style.display = 'none';
}

async function doLogin() {
  clearError('loginError');
  const email    = document.getElementById('loginEmail').value.trim();
  const password = document.getElementById('loginPassword').value;

  if (!email || !password) {
    showError('loginError', 'Please fill in all fields.');
    return;
  }

  try {
    const res  = await fetch(`${API}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();

    if (!res.ok) {
      showError('loginError', data.error || 'Login failed.');
      return;
    }

    localStorage.setItem('movieapp_user', JSON.stringify(data.user));
    window.location.href = 'index.html';

  } catch {
    showError('loginError', 'Could not connect to the server.');
  }
}

async function doRegister() {
  clearError('registerError');
  const username = document.getElementById('regUsername').value.trim();
  const email    = document.getElementById('regEmail').value.trim();
  const password = document.getElementById('regPassword').value;

  if (!username || !email || !password) {
    showError('registerError', 'Please fill in all fields.');
    return;
  }
  if (password.length < 6) {
    showError('registerError', 'Password must be at least 6 characters.');
    return;
  }

  try {
    const res  = await fetch(`${API}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ username, email, password })
    });
    const data = await res.json();

    if (!res.ok) {
      showError('registerError', data.error || 'Registration failed.');
      return;
    }

    toast('Account created! Please sign in.', 'success');
    showLogin();

  } catch {
    showError('registerError', 'Could not connect to the server.');
  }
}

// Allow Enter key to submit
document.getElementById('loginPassword').addEventListener('keydown', e => {
  if (e.key === 'Enter') doLogin();
});
document.getElementById('regPassword').addEventListener('keydown', e => {
  if (e.key === 'Enter') doRegister();
});
