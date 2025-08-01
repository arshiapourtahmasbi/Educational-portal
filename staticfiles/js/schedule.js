document.addEventListener('DOMContentLoaded', function() {
    const addScheduleBtn = document.getElementById('add-schedule');
    const scheduleContainer = document.getElementById('schedule-forms');
    let formCount = document.querySelectorAll('.schedule-form').length;
    
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
            const empty_form = document.querySelector('.schedule-form').cloneNode(true);
            empty_form.innerHTML = empty_form.innerHTML.replace(/__prefix__/g, formCount);
            scheduleContainer.appendChild(empty_form);
            
            // Update the management form
            document.getElementById('id_schedules-TOTAL_FORMS').value = ++formCount;
            
            // Add event listener to new form
            updateScheduleFields(empty_form);
            empty_form.querySelector('.schedule-type').addEventListener('change', function() {
                updateScheduleFields(empty_form);
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