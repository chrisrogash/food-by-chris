fetch("static/produce.json")
  .then(response => response.json())
  .then(data => {
    const grid = document.getElementById("produceGrid");
    data.forEach(item => {
      const card = document.createElement("div");
      card.className = "col-6 col-md-4 col-lg-3";
      card.innerHTML = `
        <div class="card text-dark produce-card">
          <img src="${item.Image}" class="card-img-top rounded-top" alt="${item.Name}">
          <div class="card-body">
            <h5 class="card-title">${item.Name}</h5>
            <p class="card-text"><strong>${item.Type}</strong></p>
            <table class="table table-sm mb-0">
              <tr>
                <td>Spring</td>
                <td class="${item.Spring === 'Yes' ? 'bg-success text-white' : 'bg-secondary text-white'} text-center">${item.Spring}</td>
              </tr>
              <tr>
                <td>Summer</td>
                <td class="${item.Summer === 'Yes' ? 'bg-success text-white' : 'bg-secondary text-white'} text-center">${item.Summer}</td>
              </tr>
              <tr>
                <td>Autumn</td>
                <td class="${item.Autumn === 'Yes' ? 'bg-success text-white' : 'bg-secondary text-white'} text-center">${item.Autumn}</td>
              </tr>
              <tr>
                <td>Winter</td>
                <td class="${item.Winter === 'Yes' ? 'bg-success text-white' : 'bg-secondary text-white'} text-center">${item.Winter}</td>
              </tr>
            </table>
          </div>
        </div>
      `;
      grid.appendChild(card);
    });
  })
  .catch(err => console.error("Failed to load produce data:", err));

  //Detect the users season and highlight the appropriate row

  navigator.geolocation.getCurrentPosition(
  (pos) => {
    const lat = pos.coords.latitude;
    const hemisphere = lat >= 0 ? 'north' : 'south';

    const today = new Date();
    const month = today.getMonth() + 1;

    function getSeason(month, hemisphere) {
      if (hemisphere === 'north') {
        if (month >= 3 && month <= 5) return 'Spring';
        if (month >= 6 && month <= 8) return 'Summer';
        if (month >= 9 && month <= 11) return 'Autumn';
        return 'Winter';
      } else { // southern hemisphere
        if (month >= 9 && month <= 11) return 'Spring';
        if (month === 12 || month <= 2) return 'Summer';
        if (month >= 3 && month <= 5) return 'Autumn';
        return 'Winter';
      }
    }

    const currentSeason = getSeason(month, hemisphere);

    // Highlight the row in each card
    document.querySelectorAll(".produce-card table").forEach(table => {
      table.querySelectorAll("tr").forEach(row => {
        const seasonCell = row.cells[0];
        if (seasonCell.textContent === currentSeason) {
          row.classList.add("table-warning"); // or bg-info, your choice
        }
      });
    });
  },
  (err) => {
    console.warn("Geolocation failed, defaulting to Southern Hemisphere");
    // fallback: assume southern hemisphere, same logic as above
  }
);
