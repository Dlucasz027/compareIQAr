$(document).ready(function() {
    
    // Inicializa o dropdown
    $('#estadoDropdown').dropdown({
        onChange: function(value, text, $selectedItem) {
            
            //Função de scroll
            $('html, body').animate({
                scrollTop: $('#iqarSection').offset().top - 100 
            }, 800);
        }
    });
});

fetch('/iqar/')
.then(res => res.json())
.then(data => {
    const iqarList = document.getElementById('iqarList');
    if (!data.resultados || data.resultados.length === 0) {
        iqarList.innerHTML = "<li>Dados indisponíveis</li>";
        return;
    }

    const cidades = data.resultados.map(item => ({
        cidade: item.cidade,
        aqi: item.aqi_eua ?? 0
    }));

    cidades.sort((a, b) => a.aqi - b.aqi);

    cidades.forEach(item => {
        const li = document.createElement('li');
        li.classList.add('city-aqi-item');

        let statusClass = "";
        let statusText = "";

        if (item.aqi <= 50) { 
            statusClass = "green"; 
            statusText = "Bom"; 
        }
        else if (item.aqi <= 200) { 
            statusClass = "yellow"; 
            statusText = "Insalubre"; 
        }
        else if (item.aqi <= 300) { 
            statusClass = "orange";
            statusText = "Muito prejudicial"; 
        }
        else if (item.aqi <= 400) { 
            statusClass = "red";
            statusText = "Perigoso"; 
        }
        else if (item.aqi <= 500) { 
            statusClass = "purple";
            statusText = "Perigoso / Muito perigoso"; 
        }
        else { 
            statusClass = "maroon";
            statusText = "Extremamente Perigoso"; 
        }
        li.innerHTML = `
            <div class="color-pill ${statusClass}" title="${statusText}"></div>
            <span class="city-name">${item.cidade}</span>
            <span class="aqi-value ${statusClass}" title="${statusText} (AQI: ${item.aqi})">${item.aqi}</span>
        `;
        iqarList.appendChild(li);
    });
})
.catch(err => {
    console.error(err);
    document.getElementById('iqarList').innerHTML = "<li>Erro ao carregar dados</li>";
});
