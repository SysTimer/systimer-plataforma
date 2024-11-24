window.addEventListener('load', function() {
        var tempos = document.querySelectorAll('.tempo_inicio');
        
        tempos.forEach((i) => {
            if (i.textContent != '00:00:00') {
                
                var partes = i.textContent.split(':');
                var horas = parseInt(partes[0], 10);
                var minutos = parseInt(partes[1], 10);
                var segundos = parseInt(partes[2], 10);

                setInterval(function() {


                        segundos += 1;


                        if (segundos == 60) { 
                                segundos = 0;
                                minutos += 1;
                        }
                        
                        if (minutos == 60) { 
                                minutos = 0;
                                horas += 1;
                        }

                        i.textContent = formatarTempo(horas, minutos, segundos);

                }, 1000);
            }
        });
    });


function formatarTempo(horas, minutos, segundos) {
        horas = horas < 10 ? '0' + horas : horas;
        minutos = minutos < 10 ? '0' + minutos : minutos;
        segundos = segundos < 10 ? '0' + segundos : segundos;
        return horas + ':' + minutos + ':' + segundos;
 }

function iniciarTarefa(trf_cod) {
        const formData = new URLSearchParams();
        formData.append('trf_cod', trf_cod); 
      
        fetch('/plataforma/iniciar_tarefa/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken') 
          },
          body: formData.toString()  
        })
        .then(response => response.json())
        .then(data => {
          window.location.reload()
        })
        .catch(error => {
          console.error('Erro ao iniciar a tarefa:', error);
        });
 }


 function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }