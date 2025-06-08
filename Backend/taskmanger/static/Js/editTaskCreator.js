    const id = window.taskId;

    function getCSRFToken() {
      const cookieValue = document.cookie.match('(^|;)\s*csrftoken\s*=\s*([^;]+)');
        return cookieValue ? cookieValue.pop() : '';
    }

   
    function filesUpload(inputElem) {
        const fileDict = {};
        if (inputElem && inputElem.files.length > 0) {
            for (let i = 0; i < inputElem.files.length; i++) {
                const file = inputElem.files[i];
                fileDict[file.name] = file;
            }
        }
        return fileDict;
    }
    async function createTask() {
            const formData = new FormData();
            const taskData = [];

            $('.DynRows tr').each(function(index, row) {
                const $row = $(row);

                const title = $row.find('.TaskTitle').val();
                const description = $row.find('.TaskDescription').val();
                const dueDate = $row.find('.due_date').val();
                const tagInput = $row.find('.tag-input').val();
                const typeofTag = $row.find('.typeofTag').val();
                
                const filesInput = $row.find('input[type="file"]')[0];
                const fileUp = filesUpload(filesInput);

                const fileNames = [];

                for (const [filename, file] of Object.entries(fileUp)) {
                    formData.append('files', file);         
                    fileNames.push(filename);               
                }
                
                taskData.push({
                    id: id,
                    title: title,
                    description: description,
                    due_date: dueDate,
                    tag: tagInput,
                    tag_type: typeofTag,
                    file_names: fileNames                  
                });
            });

            formData.append('Data', JSON.stringify(taskData));

            try {
                    const response = await fetch("/editSave", {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': getCSRFToken(),
                    },
                        body: formData,
                        credentials: 'include'
                    });

                    const data = await response.json();
                    alert(data.Succeass);
                    window.location.href = "/";
            } catch (error) {
                console.error('Fetch error:', error);
                alert('An error occurred while submitting the form.');
            }
        }
    
    function typeofTag(vals){
        
        var id = vals.id.split('_')[1]
        let selectedValue = vals.value;
        $("#tagType_"+id).empty()
        if(selectedValue == 'select-files'){
            
            var cre = `<input type="file" class="form-control files" id="files_${id}" name="files" accept=".pdf,image/*">`
            $("#tagType_"+id).append(cre)
        }
        else{
            var cre = `<input type="text" class="form-control tag-input" id="tag-input_${id}" placeholder="Type a tag and press Enter">`
            $("#tagType_"+id).append(cre)
        }
    }
