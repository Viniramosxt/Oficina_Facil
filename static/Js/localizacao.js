document.addEventListener("DOMContentLoaded", function () {
    const locationButton = document.getElementById("locationButton");

    locationButton.addEventListener("click", () => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(showPosition, showError);
        } else {
            alert("Geolocation is not supported by this browser.");
        }
    });

    function showPosition(position) {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;

        // Exibe o mapa com a localização do usuário
        showMap(lat, lon);

        // Aqui, você pode fazer uma requisição AJAX para buscar as oficinas próximas (usando Flask)
        // Passar lat e lon para o servidor e obter as oficinas mais próximas
        fetch(`/oficinas-proximas?lat=${lat}&lon=${lon}`)
            .then(response => response.json())
            .then(data => {
                if (data.officinas && data.officinas.length > 0) {
                    data.officinas.forEach(officina => {
                        // Adiciona cada oficina no mapa
                        addOfficinaMarker(officina.lat, officina.lon, officina.nome);
                    });
                } else {
                    alert("Nenhuma oficina próxima encontrada.");
                }
            })
            .catch(error => console.error('Erro ao buscar oficinas:', error));
    }

    function showError(error) {
        switch (error.code) {
            case error.PERMISSION_DENIED:
                alert("Usuário negou a solicitação de Geolocalização.");
                break;
            case error.POSITION_UNAVAILABLE:
                alert("Informações de localização não estão disponíveis.");
                break;
            case error.TIMEOUT:
                alert("A solicitação para obter a localização expirou.");
                break;
            case error.UNKNOWN_ERROR:
                alert("Ocorreu um erro desconhecido.");
                break;
        }
    }

    // Função para exibir o mapa do Mapbox
    function showMap(lat, lon) {
        mapboxgl.accessToken = 'pk.eyJ1IjoidmluaXJhbW9zN3hpdHQiLCJhIjoiY20zN2luMXlxMGgxMjJocHZhNXU2NjU0ZCJ9.Dqm5Tv_sN58rSLQExS74iQ';
        var map = new mapboxgl.Map({
            container: 'map', // ID do elemento onde o mapa será exibido
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [lon, lat], // Coordenadas centrais do mapa
            zoom: 12 // Nível de zoom
        });

        // Marcador para a localização do usuário
        new mapboxgl.Marker()
            .setLngLat([lon, lat])
            .addTo(map);
    }

    // Função para adicionar marcadores de oficinas no mapa
    function addOfficinaMarker(lat, lon, nome) {
        new mapboxgl.Marker()
            .setLngLat([lon, lat])
            .setPopup(new mapboxgl.Popup().setHTML(`<h3>${nome}</h3>`)) // Exibe o nome da oficina no popup
            .addTo(map);
    }
});
