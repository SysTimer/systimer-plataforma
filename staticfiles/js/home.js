const btnClique = document.getElementById('verMais');

window.addEventListener('load', function () {
        // Seleciona o elemento com a classe 'timestamp'
        let spanIniciada = document.querySelector('.timestamp');
    
        if (spanIniciada) {
            // Obtém o texto inicial do elemento e divide em horas, minutos e segundos
            console.log('Início:', spanIniciada.textContent);
            let partes = spanIniciada.textContent.split(':');
            let horas = parseInt(partes[0], 10) || 0;
            let minutos = parseInt(partes[1], 10) || 0;
            let segundos = parseInt(partes[2], 10) || 0;
    
            setInterval(function () {
                segundos += 1;
    
                if (segundos === 60) {
                    segundos = 0;
                    minutos += 1;
                }
    
                if (minutos === 60) {
                    minutos = 0;
                    horas += 1;
                }
    
                // Atualiza o texto do elemento
                spanIniciada.textContent = formatarTempo(horas, minutos, segundos);
            }, 1000);
        }
    });
    


document.querySelectorAll('button[data-task-id]').forEach(button => {
        button.addEventListener('click', function() {
            var taskId = this.getAttribute('data-task-id');
            enviarHoras(taskId);
        });
});
    
function enviarHoras(taskId) {
    console.log('Task ID ', taskId);

    const formData = new URLSearchParams();
    formData.append('trf_cod', taskId);
    formData.append('trf_acao', 'P');

    fetch('/plataforma/enviar_banco_horas/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken') 
        },
        body: formData.toString()
    })
    .then(response => response.json())
    .then(data => {
        console.log('Tarefa iniciada com sucesso:', data);
    })
    .catch(error => {
        console.error('Erro ao iniciar a tarefa:', error);
    });
}


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

