const API = 'http://127.0.0.1:5000';

/*  User state (stored in localStorage after login) */
function getUser() {
  try { return JSON.parse(localStorage.getItem('movieapp_user') || 'null'); }
  catch { return null; }
}

/* Render nav links based on login state  */
function renderNav(active) {
  const nav = document.getElementById('navLinks');
  if (!nav) return;
  const user = getUser();
  if (user) {
    nav.innerHTML = `
      <a href="index.html" ${active === 'home'      ? 'class="active"' : ''}>Home</a>
      <a href="watchlist.html" ${active === 'watchlist' ? 'class="active"' : ''}>Watchlist</a>
      ${user.is_admin ? `<a href="admin.html" ${active === 'admin' ? 'class="active"' : ''}>Admin</a>` : ''}
      <span style="color:var(--text-muted);font-size:0.85rem">Hi, <strong style="color:var(--text)">${user.username}</strong></span>
      <button class="btn btn-outline" onclick="logout()" style="padding:6px 14px;font-size:0.82rem">Logout</button>
    `;
  } else {
    nav.innerHTML = `
      <a href="index.html" ${active === 'home' ? 'class="active"' : ''}>Home</a>
      <a href="auth.html" class="btn btn-primary" style="padding:7px 16px;font-size:0.85rem">Login / Register</a>
    `;
  }
}

/*  Logout  */
async function logout() {
  try { await fetch(`${API}/auth/logout`, { method: 'POST', credentials: 'include' }); }
  catch {}
  localStorage.removeItem('movieapp_user');
  window.location.href = 'index.html';
}

/*  Toast notification  */
function toast(msg, type) {
  document.querySelector('.toast')?.remove();
  const el = document.createElement('div');
  el.className = 'toast' + (type ? ' ' + type : '');
  el.textContent = msg;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 3500);
}

/* Search  */
function doSearch() {
  const q = document.getElementById('searchInput')?.value.trim();
  if (q) window.location.href = `search.html?q=${encodeURIComponent(q)}`;
}

function setupSearchInput() {
  document.getElementById('searchInput')?.addEventListener('keydown', e => {
    if (e.key === 'Enter') doSearch();
  });
}

/*  Movie card HTML  */
function movieCard(m) {
  const poster = m.poster_path
    ? `<img src="https://image.tmdb.org/t/p/w300${m.poster_path}" alt="${m.title}" loading="lazy">`
    : `<div class="movie-card-no-poster">No Poster</div>`;
  const year   = m.release_date ? m.release_date.slice(0, 4) : '—';
  const rating = m.vote_average ? Number(m.vote_average).toFixed(1) : '—';
  return `
    <div class="movie-card" onclick="window.location.href='movie.html?id=${m.id}'">
      ${poster}
      <div class="movie-card-overlay">
        <button class="btn btn-primary btn-sm">Quick View</button>
      </div>
      <div class="movie-card-info">
        <div class="movie-card-title" title="${m.title}">${m.title}</div>
        <div class="movie-card-meta">
          <span>${year}</span>
          <span class="movie-card-rating">&#9733; ${rating}</span>
        </div>
      </div>
    </div>`;
}
