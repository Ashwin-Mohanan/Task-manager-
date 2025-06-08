function getCSRFToken() {
      const cookieValue = document.cookie.match('(^|;)\s*csrftoken\s*=\s*([^;]+)');
        return cookieValue ? cookieValue.pop() : '';
    }
    
    count=0
    function AddRow(){
        
        count++
        var CreateRow = `
        <tbody class='DynRows'>
            <tr>
            
                <td>
                    <input type="text" class="form-control TaskTitle" id="TaskTitle_${count}" placeholder="Task Name" required> 
                </td>
                <td>
                    <textarea type="text" class="form-control TaskDescription" id="TaskDescription_${count}" placeholder="Task Description" required></textarea>
                </td>
                <td>
                    <div id="datepicker">
                        <input type="date" class="form-control due_date" id="due_date_${count}" name="due_date" required>
                    </div>
                </td>
                <td id="tagType_${count}">
                    <input type="text" class="form-control tag-input" id="tag-input_${count}" placeholder="Type a tag and press Enter">
                    
                </td>
                <td>
                    <select class="selectpicker typeofTag" id="typeofTag_${count}" onchange="typeofTag(this)">
                        <option selected value="Custom Add">Custom Add</option>
                        <option value="select-files">Select Files</option>
                    </select>
                </td>
                <td>
                    <button type="button" class="btn btn-primary btn-sm delete">
                        <i class="material-icons">delete</i>
                    </button>
                </td>
            </tr>
            
        </tbody>
        `

        $('.table').append(CreateRow)
        $('.delete').click(function(){
            
            $(this).parent().parent().parent().remove()
        })
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
            var cre = `<input type="text" class="form-control tag-input" id="tag-input_${count}" placeholder="Type a tag and press Enter">`
            $("#tagType_"+id).append(cre)
        }
    }


    // async function filesUpload(vals) {
    //     debugger
    //     const formData = new FormData();
    //     debugger
    //     id = vals.id
    //     formData.append('id',id)
    //     // Add file(s) to formData
    //     const fileInput = document.querySelector('#'+id); // Change selector as needed
    //     if (fileInput && fileInput.files.length > 0) {
    //         for (let i = 0; i < fileInput.files.length; i++) {
    //             // formData.append('files[]', fileInput.files[i]);
    //             formData.append(id, fileInput.files[i]);

    //         }
    //     }

    //     try {
    //         const response = await fetch(fileSaveURL , {
    //             method: 'POST',
    //             headers: {
    //                 'X-Requested-With': 'XMLHttpRequest',
    //                 'X-CSRFToken': getCSRFToken(),
    //             },
    //             body: formData,
    //             credentials: 'include'
    //         })
    //         .then(response => response.json())
    //         .then(data => {
    //             alert(data.status)
    //         });
    //     } catch (error) {
    //         console.error('Fetch error:', error);
    //         alert('An error occurred while submitting the form.');
    //     }
    // }

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
                const response = await fetch("/taskSave", {
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
