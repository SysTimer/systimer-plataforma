if (document.getElementById("sorting-table") && typeof simpleDatatables.DataTable !== 'undefined') {
    const dataTable = new simpleDatatables.DataTable("#sorting-table", {
        searchable: false,
        perPageSelect: false,
        sortable: true,
        labels: {
            placeholder: "Pesquisar...", // Texto no campo de pesquisa
            perPage: "{select} resultados por página", // Texto para seleção de resultados por página
            noRows: "Nenhum resultado encontrado", // Texto para nenhuma linha encontrada
            info: "Mostrando {start} a {end} de {rows} entradas", // Texto de informação
        }
    });
}


document.addEventListener("DOMContentLoaded", function () {
    const tabelaExportacao = document.getElementById("tabelaExportacao");
    const tabelaPendencias = document.getElementById("tabelaPendencias");
    const tabelaAprovadas = document.getElementById("tabelaAprovadas");

    if (tabelaExportacao) {
        new DataTable(tabelaExportacao, {
            dom: 'Bfrtip',
            buttons: [
                {
                    extend: 'copy',
                    text: '<i class="fa-solid fa-copy"></i> Copiar',
                    className: 'bg-blue-700 text-white  px-3 py-0.5 rounded hover:bg-blue-500'
                },
                {
                    extend: 'csv',
                    text: '<i class="fa-solid fa-file-csv"></i> Exportar CSV',
                    className: 'bg-blue-700 text-white  px-3 py-0.5 rounded hover:bg-blue-500'
                },
                {
                    extend: 'excel',
                    text: '<i class="fa-solid fa-file-excel"></i> Exportar Excel',
                    className: 'bg-blue-700 text-white px-3 py-0.5 rounded hover:bg-blue-500'
                },
                {
                    extend: 'pdf',
                    text: '<i class="fa-solid fa-file-pdf"></i> Exportar PDF',
                    className: 'bg-blue-700 text-white  px-3 py-0.5 rounded hover:bg-blue-500'
                },
                {
                    extend: 'print',
                    text: '<i class="fa-solid fa-print"></i> Imprimir',
                    className: 'bg-blue-700 text-white px-3 py-0.5 rounded hover:bg-blue-500'
                }
            ],
            searching: false,
            searchable: false,
            perPageSelect: false,
            sortable: false,
            paging: false, // Desabilita a paginação
            info: false,    // Remove a mensagem de "Mostrando X de Y registros"
            language: {
                url: "http://127.0.0.1:8000/static/js/pt-BR.json"
            }
        });
    }



    if (tabelaAprovadas) {
        new DataTable(tabelaAprovadas, {
            dom: '21',
            buttons: [
                {
                    extend: 'copy',
                    text: '<i class="fa-solid fa-copy"></i> Copiar',
                    className: 'bg-blue-700 text-white  px-3 py-0.5 rounded hover:bg-blue-500'
                },
                {
                    extend: 'csv',
                    text: '<i class="fa-solid fa-file-csv"></i> Exportar CSV',
                    className: 'bg-blue-700 text-white  px-3 py-0.5 rounded hover:bg-blue-500'
                },
                {
                    extend: 'excel',
                    text: '<i class="fa-solid fa-file-excel"></i> Exportar Excel',
                    className: 'bg-blue-700 text-white px-3 py-0.5 rounded hover:bg-blue-500'
                },
                {
                    extend: 'pdf',
                    text: '<i class="fa-solid fa-file-pdf"></i> Exportar PDF',
                    className: 'bg-blue-700 text-white  px-3 py-0.5 rounded hover:bg-blue-500'
                },
                {
                    extend: 'print',
                    text: '<i class="fa-solid fa-print"></i> Imprimir',
                    className: 'bg-blue-700 text-white px-3 py-0.5 rounded hover:bg-blue-500'
                }
            ],
            searching: false,
            searchable: false,
            perPageSelect: false,
            sortable: false,
            paging: false, // Desabilita a paginação
            info: false,    // Remove a mensagem de "Mostrando X de Y registros"
            language: {
                url: "http://127.0.0.1:8000/static/js/pt-BR.json"
            }
        });
    }

    if (tabelaPendencias) {
        new DataTable(tabelaPendencias, {
            dom: '23',
            buttons: [
                {
                    extend: 'copy',
                    text: '<i class="fa-solid fa-copy"></i> Copiar',
                    className: 'bg-blue-700 text-white  px-3 py-0.5 rounded hover:bg-blue-500'
                },
                {
                    extend: 'csv',
                    text: '<i class="fa-solid fa-file-csv"></i> Exportar CSV',
                    className: 'bg-blue-700 text-white  px-3 py-0.5 rounded hover:bg-blue-500'
                },
                {
                    extend: 'excel',
                    text: '<i class="fa-solid fa-file-excel"></i> Exportar Excel',
                    className: 'bg-blue-700 text-white px-3 py-0.5 rounded hover:bg-blue-500'
                },
                {
                    extend: 'pdf',
                    text: '<i class="fa-solid fa-file-pdf"></i> Exportar PDF',
                    className: 'bg-blue-700 text-white  px-3 py-0.5 rounded hover:bg-blue-500'
                },
                {
                    extend: 'print',
                    text: '<i class="fa-solid fa-print"></i> Imprimir',
                    className: 'bg-blue-700 text-white px-3 py-0.5 rounded hover:bg-blue-500'
                }
            ],
            searching: false,
            searchable: false,
            perPageSelect: false,
            sortable: false,
            paging: false, // Desabilita a paginação
            info: false,    // Remove a mensagem de "Mostrando X de Y registros"
            language: {
                url: "http://127.0.0.1:8000/static/js/pt-BR.json"
            }
        });
    }
});




