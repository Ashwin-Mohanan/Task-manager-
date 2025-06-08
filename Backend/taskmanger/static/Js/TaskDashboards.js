function filterTasks() {
        const searchInput = document.getElementById('searchBar').value.toLowerCase();
        const tagFilter = document.getElementById('tagFilter').value.toLowerCase();  
        const table = document.getElementById('taskTable');
        const rows = table.getElementsByTagName('tr');

        for (let i = 1; i < rows.length; i++) {
            const taskName = rows[i].getElementsByTagName('td')[0].textContent.toLowerCase();
            const taskTag = rows[i].getElementsByTagName('td')[2].textContent.toLowerCase(); 
            if (taskName.includes(searchInput) && (tagFilter === "" || taskTag === tagFilter)) {
                rows[i].style.display = "";
            } else {
                rows[i].style.display = "none";
            }
        }
    }