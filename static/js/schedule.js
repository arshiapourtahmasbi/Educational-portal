document.addEventListener('DOMContentLoaded', function() {
    const addScheduleBtn = document.getElementById('add-schedule');
    const scheduleContainer = document.getElementById('schedule-forms');
    let formCount = document.querySelectorAll('.schedule-form').length;
    
    // Store the template form HTML for later use
    const templateForm = document.querySelector('.schedule-form').cloneNode(true);
    
    function updateScheduleFields(form) {
        const scheduleType = form.querySelector('.schedule-type');
        const specificDate = form.querySelector('.specific-date').parentElement;
        const weekday = form.querySelector('.weekday').parentElement;
        
        if (scheduleType.value === 'date') {
            specificDate.style.display = 'block';
            weekday.style.display = 'none';
        } else {
            specificDate.style.display = 'none';
            weekday.style.display = 'block';
        }
    }
    
    // Initialize existing forms
    document.querySelectorAll('.schedule-form').forEach(form => {
        updateScheduleFields(form);
        form.querySelector('.schedule-type').addEventListener('change', function() {
            updateScheduleFields(form);
        });
    });
    
    if (addScheduleBtn) {
        addScheduleBtn.addEventListener('click', function() {
            // Create new form from stored template
            const newForm = templateForm.cloneNode(true);
            
            // Clear any values that might have been in the template
            newForm.querySelectorAll('input[type="text"], input[type="date"], input[type="time"], select').forEach(input => {
                input.value = '';
            });
            
            // Update form index
            newForm.innerHTML = newForm.innerHTML.replace(
                new RegExp('schedules-\\d+-', 'g'), 
                `schedules-${formCount}-`
            );
            
            // Add the new form to the container
            scheduleContainer.appendChild(newForm);
            
            // Update the management form
            document.getElementById('id_schedules-TOTAL_FORMS').value = ++formCount;
            
            // Add event listener to new form
            updateScheduleFields(newForm);
            newForm.querySelector('.schedule-type').addEventListener('change', function() {
                updateScheduleFields(newForm);
            });
        });
    }

    // Handle delete buttons
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('delete-schedule')) {
            e.preventDefault();
            const scheduleForm = e.target.closest('.schedule-form');
            scheduleForm.style.display = 'none';
            const deleteInput = scheduleForm.querySelector('input[name$="-DELETE"]');
            if (deleteInput) {
                deleteInput.value = 'on';
            }
        }
    });
});