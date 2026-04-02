(function () {
  const params = new URLSearchParams(window.location.search);
  const query  = params.get('q') || '';

  // Pre-fill the search bar with the current query
  const input = document.getElementById('searchInput');
  if (input) input.value = query;

  // Update the page heading
  const titleEl = document.getElementById('searchTitle');
  if (titleEl) {
    titleEl.innerHTML = query
      ? `Results for "<span>${query}</span>"`
      : 'Search Results';
  }

  async function runSearch() {
    const grid = document.getElementById('movieGrid');
    if (!query) {
      grid.innerHTML = '<div class="empty-state"><h3>Enter a movie title to search</h3></div>';
      return;
    }
    grid.innerHTML = '<p class="loading">Searching...</p>';
    try {
      const res  = await fetch(`${API}/movies/search?q=${encodeURIComponent(query)}`, { credentials: 'include' });
      const data = await res.json();
      const movies = data.results || [];
      if (!movies.length) {
        grid.innerHTML = '<div class="empty-state"><h3>No results found</h3><p>Try a different search term</p></div>';
        return;
      }
      grid.innerHTML = movies.map(movieCard).join('');
    } catch {
      grid.innerHTML = '<p class="loading">Search failed. Make sure the backend is running.</p>';
    }
  }

  renderNav();
  setupSearchInput();
  runSearch();
})();
