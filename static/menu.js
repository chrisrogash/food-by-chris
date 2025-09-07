fetch('static/data.json')
  .then(res => res.json())
  .then(data => {
    const dishes = data.dishes;
    const tagsMap = Object.fromEntries(data.tags.map(t => [t.tag, t])); // map tag id → tag info

    const container = document.getElementById('dishList');
    const searchBox = document.getElementById('searchBox');
    const tagInputs = document.querySelectorAll('#tagFilters input');

    function render() {
      const search = searchBox.value.toLowerCase();
      const checked = [...tagInputs].filter(cb => cb.checked).map(cb => cb.value);
      container.innerHTML = '';

      dishes.forEach(d => {
        // Filter by search
        if (!d.name.toLowerCase().includes(search)) return;
        // Filter by selected tags
        if (checked.length && !checked.every(t => d.tags.includes(t))) return;

        const col = document.createElement('div');
        col.className = 'col-12 col-md-6 col-lg-4';

        const tagSpans = d.tags
          .map(t => {
            const tag = tagsMap[t];
            return `<span class="badge ${tag?.class || 'bg-dark'} me-1">${tag?.tag_readable || t}</span>`;
          })
          .join('');
        
        const imgHtml = d.image ? `<div class="ratio ratio-16x9 mb-2">
        <img src="${d.image}" class="img-fluid rounded mb-2" alt="${d.name}"></div>` : '';

        col.innerHTML = `
          <div class="card shadow-sm rounded-3">
            <div class="card-body bg-dark rounded-3">
            ${imgHtml}
              <h5 class="card-title text-white">${d.name}</h5>
              <p class="card-text text-white">Prep: ${d.prep_time}m | Cook: ${d.cook_time}m</p>
              <p>${tagSpans}</p>
              <a href="dish.html?id=${d.id}" class="btn btn-outline-light">View Recipe</a>
            </div>
          </div>`;
        container.appendChild(col);
      });
    }

    searchBox.addEventListener('input', render);
    tagInputs.forEach(cb => cb.addEventListener('change', render));

    render();
  });
