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