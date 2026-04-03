const params  = new URLSearchParams(window.location.search);
const movieId = params.get('id');

let currentMovie   = null;
let userReviewId   = null;
let watchlistIds   = [];

if (!movieId) window.location.href = 'index.html';

renderNav('');
setupSearchInput();

// ── Load everything in parallel ──────────────────────────────────────────────
async function init() {
  const user = getUser();
  const tasks = [
    fetchMovie(),
    fetchReviews(),
    fetchRecommendations(),
  ];
  if (user) tasks.push(fetchWatchlist());
  await Promise.all(tasks);
}

// ── Movie details ─────────────────────────────────────────────────────────────
async function fetchMovie() {
  try {
    const res  = await fetch(`${API}/movies/${movieId}`, { credentials: 'include' });
    const data = await res.json();
    currentMovie = data;
    document.title = `${data.title} – Cinestream`;
    renderMovieDetails(data);
  } catch {
    document.getElementById('movieDetails').innerHTML =
      '<p class="loading">Failed to load movie details.</p>';
  }
}

function renderMovieDetails(m) {
  const user   = getUser();
  const year   = m.release_date ? m.release_date.slice(0, 4) : '';
  const rating = m.vote_average ? Number(m.vote_average).toFixed(1) : 'N/A';
  const runtime = m.runtime ? `${m.runtime} min` : '';
  const genres  = (m.genres || []).map(g => `<span class="genre-tag">${g.name}</span>`).join('');
  const cast    = (m.credits?.cast || []).slice(0, 5).map(c => c.name).join(', ');

  const poster = m.poster_path
    ? `<img src="https://image.tmdb.org/t/p/w400${m.poster_path}" alt="${m.title}">`
    : `<div class="movie-poster-placeholder">No Poster</div>`;

  const inWatchlist = watchlistIds.includes(Number(movieId));

  document.getElementById('movieDetails').innerHTML = `
    <div class="movie-poster">${poster}</div>
    <div class="movie-info">
      <h1>${m.title}</h1>
      <div class="movie-meta">
        ${year ? `<span>${year}</span>` : ''}
        ${runtime ? `<span>${runtime}</span>` : ''}
        <span class="tmdb-rating">&#9733; ${rating} TMDB</span>
      </div>
      <div class="genre-tags">${genres}</div>
      <p class="movie-overview">${m.overview || 'No overview available.'}</p>
      ${cast ? `<p class="movie-cast"><strong>Cast:</strong> ${cast}</p>` : ''}
      <div class="movie-actions">
        ${user ? `
          <button class="btn ${inWatchlist ? 'btn-outline' : 'btn-primary'}" id="watchlistBtn" onclick="toggleWatchlist()">
            ${inWatchlist ? '✓ In Watchlist' : '+ Add to Watchlist'}
          </button>
        ` : ''}
      </div>
    </div>
  `;
}

// ── Watchlist ─────────────────────────────────────────────────────────────────
async function fetchWatchlist() {
  try {
    const res  = await fetch(`${API}/watchlist/`, { credentials: 'include' });
    if (!res.ok) return;
    const data = await res.json();
    watchlistIds = data.map(item => item.tmdb_id);
  } catch {}
}

async function toggleWatchlist() {
  const user = getUser();
  if (!user) { window.location.href = 'auth.html'; return; }

  const inList = watchlistIds.includes(Number(movieId));

  if (inList) {
    await fetch(`${API}/watchlist/remove/${movieId}`, { method: 'DELETE', credentials: 'include' });
    watchlistIds = watchlistIds.filter(id => id !== Number(movieId));
    toast('Removed from watchlist');
  } else {
    await fetch(`${API}/watchlist/add`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        tmdb_id: Number(movieId),
        title: currentMovie.title,
        poster_path: currentMovie.poster_path || null
      })
    });
    watchlistIds.push(Number(movieId));
    toast('Added to watchlist', 'success');
  }

  // Update button state
  const btn = document.getElementById('watchlistBtn');
  if (btn) {
    const nowIn = watchlistIds.includes(Number(movieId));
    btn.textContent = nowIn ? '✓ In Watchlist' : '+ Add to Watchlist';
    btn.className   = `btn ${nowIn ? 'btn-outline' : 'btn-primary'}`;
  }
}

// ── Reviews ───────────────────────────────────────────────────────────────────
async function fetchReviews() {
  try {
    const res   = await fetch(`${API}/movies/${movieId}/reviews`, { credentials: 'include' });
    const reviews = await res.json();
    renderReviews(reviews);
  } catch {
    document.getElementById('reviewsList').innerHTML = '<p style="color:var(--text-muted)">Could not load reviews.</p>';
  }
}

function renderReviews(reviews) {
  const user = getUser();
  const list = document.getElementById('reviewsList');
  const box  = document.getElementById('reviewFormBox');

  if (!reviews.length) {
    list.innerHTML = '<p style="color:var(--text-muted);padding:12px 0">No reviews yet. Be the first!</p>';
  } else {
    list.innerHTML = reviews.map(r => {
      const isOwn = user && r.user_id === user.id;
      userReviewId = isOwn ? r.id : userReviewId;
      return `
        <div class="review-card">
          <div class="review-card-top">
            <div>
              <span class="review-user">User #${r.user_id}</span>
              ${r.rating ? `<span class="review-score" style="margin-left:10px">&#9733; ${r.rating}/10</span>` : ''}
            </div>
            <span class="review-date">${new Date(r.created_at).toLocaleDateString()}</span>
          </div>
          <p class="review-text">${r.comment || ''}</p>
          ${isOwn ? `
            <div class="review-own-actions">
              <button class="btn btn-outline btn-sm" onclick="editReview(${r.id}, ${r.rating}, \`${(r.comment||'').replace(/`/g,"'")}\`)">Edit</button>
              <button class="btn btn-danger btn-sm" onclick="deleteReview(${r.id})">Delete</button>
            </div>` : ''}
        </div>`;
    }).join('');
  }

  // Show form only if logged in and hasn't reviewed yet
  const alreadyReviewed = user && reviews.some(r => r.user_id === user.id);
  if (user && !alreadyReviewed) box.style.display = 'block';
  else box.style.display = 'none';
}

async function submitReview() {
  const rating  = document.getElementById('reviewRating').value;
  const comment = document.getElementById('reviewComment').value.trim();

  if (!rating && !comment) {
    toast('Please add a rating or comment.', 'error'); return;
  }

  const res = await fetch(`${API}/user/reviews`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ movie_id: Number(movieId), rating: rating ? Number(rating) : null, comment })
  });

  if (res.ok) {
    toast('Review posted!', 'success');
    fetchReviews();
  } else {
    const d = await res.json();
    toast(d.error || 'Could not post review.', 'error');
  }
}

function editReview(id, rating, comment) {
  document.getElementById('reviewFormBox').style.display = 'block';
  document.getElementById('reviewRating').value  = rating || '';
  document.getElementById('reviewComment').value = comment || '';
  document.querySelector('#reviewFormBox h3').textContent = 'Edit Your Review';
  document.querySelector('#reviewFormBox .btn').onclick = () => updateReview(id);
  document.querySelector('#reviewFormBox .btn').textContent = 'Update Review';
  document.getElementById('reviewFormBox').scrollIntoView({ behavior: 'smooth' });
}

async function updateReview(id) {
  const rating  = document.getElementById('reviewRating').value;
  const comment = document.getElementById('reviewComment').value.trim();

  const res = await fetch(`${API}/user/reviews/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ rating: rating ? Number(rating) : null, comment })
  });

  if (res.ok) { toast('Review updated!', 'success'); fetchReviews(); }
  else        { toast('Could not update review.', 'error'); }
}

async function deleteReview(id) {
  if (!confirm('Delete your review?')) return;
  const res = await fetch(`${API}/user/reviews/${id}`, { method: 'DELETE', credentials: 'include' });
  if (res.ok) { toast('Review deleted.'); fetchReviews(); }
  else        { toast('Could not delete review.', 'error'); }
}

// ── Recommendations ───────────────────────────────────────────────────────────
async function fetchRecommendations() {
  try {
    const res  = await fetch(`${API}/movies/${movieId}/recommendations`, { credentials: 'include' });
    const data = await res.json();
    const movies = (data.results || []).slice(0, 12);
    const list   = document.getElementById('recommendationsList');
    if (!movies.length) {
      list.innerHTML = '<p style="color:var(--text-muted)">No recommendations found.</p>';
      return;
    }
    list.innerHTML = movies.map(movieCard).join('');
  } catch {
    document.getElementById('recommendationsList').innerHTML =
      '<p style="color:var(--text-muted)">Could not load recommendations.</p>';
  }
}

init();
