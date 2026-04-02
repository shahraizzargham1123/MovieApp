// Guard: redirect non-admins away
const user = getUser();
if (!user || !user.is_admin) window.location.href = 'index.html';

renderNav('admin');

// ── Section switching ─────────────────────────────────────────────────────────
function showSection(name) {
  document.getElementById('sectionUsers').style.display   = name === 'users'   ? 'block' : 'none';
  document.getElementById('sectionReviews').style.display = name === 'reviews' ? 'block' : 'none';
  document.getElementById('sidebarUsers').classList.toggle('active',   name === 'users');
  document.getElementById('sidebarReviews').classList.toggle('active', name === 'reviews');

  if (name === 'users')   loadUsers();
  if (name === 'reviews') loadReviews();
}

// ── Users ─────────────────────────────────────────────────────────────────────
async function loadUsers() {
  const tbody = document.getElementById('usersTableBody');
  tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;color:var(--text-muted);padding:24px">Loading...</td></tr>';
  try {
    const res   = await fetch(`${API}/admin/users`, { credentials: 'include' });
    const users = await res.json();

    if (!users.length) {
      tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;color:var(--text-muted);padding:24px">No users found.</td></tr>';
      return;
    }

    tbody.innerHTML = users.map(u => `
      <tr>
        <td>${u.id}</td>
        <td>${u.username}</td>
        <td>${u.email}</td>
        <td><span class="badge ${u.is_active !== false ? 'badge-active' : 'badge-inactive'}">${u.is_active !== false ? 'Active' : 'Inactive'}</span></td>
        <td>
          ${u.is_active !== false
            ? `<button class="btn btn-danger btn-sm" onclick="setUserActive(${u.id}, false, this)">Deactivate</button>`
            : `<button class="btn btn-success btn-sm" onclick="setUserActive(${u.id}, true, this)">Activate</button>`}
        </td>
      </tr>`).join('');
  } catch {
    tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;color:var(--text-muted);padding:24px">Failed to load users.</td></tr>';
  }
}

async function setUserActive(userId, activate, btn) {
  btn.disabled = true;
  const action = activate ? 'activate' : 'deactivate';
  try {
    const res = await fetch(`${API}/admin/users/${userId}/${action}`, { method: 'PUT', credentials: 'include' });
    if (res.ok) { toast(activate ? 'User activated.' : 'User deactivated.', 'success'); loadUsers(); }
    else        { toast('Action failed.', 'error'); btn.disabled = false; }
  } catch {
    toast('Could not connect to server.', 'error');
    btn.disabled = false;
  }
}

// ── Reviews ───────────────────────────────────────────────────────────────────
async function loadReviews() {
  const tbody = document.getElementById('reviewsTableBody');
  tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;color:var(--text-muted);padding:24px">Loading...</td></tr>';
  try {
    const res     = await fetch(`${API}/admin/reviews`, { credentials: 'include' });
    const reviews = await res.json();

    if (!reviews.length) {
      tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;color:var(--text-muted);padding:24px">No reviews found.</td></tr>';
      return;
    }

    tbody.innerHTML = reviews.map(r => `
      <tr>
        <td>${r.id}</td>
        <td>${r.user_id}</td>
        <td>${r.movie_id}</td>
        <td>${r.rating ?? '—'}</td>
        <td style="max-width:280px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title="${r.comment || ''}">${r.comment || '—'}</td>
        <td>${new Date(r.created_at).toLocaleDateString()}</td>
        <td><button class="btn btn-danger btn-sm" onclick="deleteReview(${r.id}, this)">Delete</button></td>
      </tr>`).join('');
  } catch {
    tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;color:var(--text-muted);padding:24px">Failed to load reviews.</td></tr>';
  }
}

async function deleteReview(reviewId, btn) {
  if (!confirm('Delete this review?')) return;
  btn.disabled = true;
  try {
    const res = await fetch(`${API}/admin/reviews/${reviewId}`, { method: 'DELETE', credentials: 'include' });
    if (res.ok) { toast('Review deleted.', 'success'); loadReviews(); }
    else        { toast('Could not delete review.', 'error'); btn.disabled = false; }
  } catch {
    toast('Could not connect to server.', 'error');
    btn.disabled = false;
  }
}

// Load users by default
loadUsers();
