const dishList = document.getElementById("dishList");
const searchBox = document.getElementById("searchBox");
const tagFilters = document.querySelectorAll("#tagFilters input[type='checkbox']");

fetch("food-by-chris/recipes_json/index/recipes_index.json")
  .then(res => res.json())
  .then(recipes => {
    // Render cards
    function renderCards(filtered) {
      dishList.innerHTML = "";
      filtered.forEach(r => {
        const tagsHtml = r.tags.map(tag => `<span class="badge bg-info me-1">${tag.replace('_', ' ')}</span>`).join(" ");
        const card = document.createElement("div");
        card.className = "col-12 col-md-6 col-lg-4";
        card.innerHTML = `
          <div class="card bg-dark text-white border-light h-100">
            <img src="${r.image}" class="card-img-top rounded-top" alt="${r.name}" style="max-height:200px; object-fit:cover;">
            <div class="card-body d-flex flex-column">
              <h5 class="card-title">${r.name}</h5>
              <p class="mb-2">${tagsHtml}</p>
              <p class="mb-2"><strong>🔪 Prep:</strong> ${r.prep_time || 0} min | <strong>👨‍🍳 Cook:</strong> ${r.cook_time || 0} min</p>
              <a href="${r.html}" class="btn btn-outline-light mt-auto">View Recipe</a>
            </div>
          </div>
        `;
        dishList.appendChild(card);
      });
    }

    // Filter function combining search + tags
    function getFilteredRecipes() {
      const query = searchBox.value.toLowerCase();
      const activeTags = Array.from(tagFilters).filter(i => i.checked).map(i => i.value);
      return recipes.filter(r => {
        const matchesSearch = r.name.toLowerCase().includes(query);
        const matchesTags = activeTags.every(tag => r.tags.includes(tag));
        return matchesSearch && matchesTags;
      });
    }

    // Initial render
    renderCards(recipes);

    // Event listeners
    searchBox.addEventListener("input", () => {
      renderCards(getFilteredRecipes());
    });

    tagFilters.forEach(input => {
      input.addEventListener("change", () => {
        renderCards(getFilteredRecipes());
      });
    });
  })
  .catch(err => console.error("Failed to load recipes_index.json:", err));
