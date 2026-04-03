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
    const initial = user.username.charAt(0).toUpperCase();
    nav.innerHTML = `
      <a href="index.html" ${active === 'home'      ? 'class="active"' : ''}>Home</a>
      <a href="watchlist.html" ${active === 'watchlist' ? 'class="active"' : ''}>Watchlist</a>
      ${user.is_admin ? `<a href="admin.html" ${active === 'admin' ? 'class="active"' : ''}>Admin</a>` : ''}
      <div class="user-menu" id="userMenu">
        <button class="user-avatar" id="userAvatarBtn" onclick="toggleUserMenu()" aria-label="User menu">${initial}</button>
        <div class="user-dropdown" id="userDropdown">
          <div class="user-dropdown-header">
            <strong>${user.username}</strong>
            <span>${user.email || ''}</span>
          </div>
          <a href="#" class="user-dropdown-item" onclick="showProfileDetails(event)">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg>
            Profile Details
          </a>
          <div class="user-dropdown-divider"></div>
          <button class="user-dropdown-item user-dropdown-logout" onclick="logout()">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
            Logout
          </button>
        </div>
      </div>
    `;
    document.addEventListener('click', closeUserMenuOnOutsideClick);
  } else {
    nav.innerHTML = `
      <a href="index.html" ${active === 'home' ? 'class="active"' : ''}>Home</a>
      <a href="auth.html" class="btn btn-primary" style="padding:7px 16px;font-size:0.85rem">Login / Register</a>
    `;
  }
}

function toggleUserMenu() {
  document.getElementById('userDropdown')?.classList.toggle('open');
}

function closeUserMenuOnOutsideClick(e) {
  const menu = document.getElementById('userMenu');
  if (menu && !menu.contains(e.target)) {
    document.getElementById('userDropdown')?.classList.remove('open');
  }
}

function showProfileDetails(e) {
  e.preventDefault();
  const user = getUser();
  if (!user) return;
  document.getElementById('userDropdown')?.classList.remove('open');
  document.querySelector('.profile-modal-overlay')?.remove();
  const initial = user.username.charAt(0).toUpperCase();
  const overlay = document.createElement('div');
  overlay.className = 'profile-modal-overlay';
  overlay.innerHTML = `
    <div class="profile-modal">
      <button class="profile-modal-close" onclick="this.closest('.profile-modal-overlay').remove()">&times;</button>
      <div class="profile-modal-avatar">${initial}</div>
      <div class="profile-modal-name">${user.username}</div>
      <div class="profile-modal-email">${user.email || '—'}</div>
      <div class="profile-modal-badge">${user.is_admin ? 'Administrator' : 'Member'}</div>
    </div>
  `;
  overlay.addEventListener('click', function(ev) {
    if (ev.target === overlay) overlay.remove();
  });
  document.body.appendChild(overlay);
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
