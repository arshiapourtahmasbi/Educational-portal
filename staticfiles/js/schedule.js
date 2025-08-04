document.addEventListener('DOMContentLoaded', function() {
    const addScheduleBtn = document.getElementById('add-schedule'); // Button to add new schedule form
    const scheduleContainer = document.getElementById('schedule-forms'); // Container for schedule forms
    let formCount = document.querySelectorAll('.schedule-form').length; // Number of existing forms
    
    // Function to update schedule fields based on selected type
    function updateScheduleFields(form) {
        const scheduleType = form.querySelector('.schedule-type'); // Dropdown to select schedule type
        const specificDate = form.querySelector('.specific-date').parentElement; // Date input for specific date
        const weekday = form.querySelector('.weekday').parentElement; // Dropdown for weekday
        
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
        updateScheduleFields(form); // Set initial visibility based on type
        form.querySelector('.schedule-type').addEventListener('change', function() {
            updateScheduleFields(form); // Update visibility based on type
        });
    });
    
    if (addScheduleBtn) {
        addScheduleBtn.addEventListener('click', function() {
            const empty_form = document.querySelector('.schedule-form').cloneNode(true); // Clone the empty form
            empty_form.innerHTML = empty_form.innerHTML.replace(/__prefix__/g, formCount); // Replace prefix for new form
            scheduleContainer.appendChild(empty_form); // Append the new form to the container
            
            // Update the management form
            document.getElementById('id_schedules-TOTAL_FORMS').value = ++formCount; // Increment total forms count
            
            // Add event listener to new form
            updateScheduleFields(empty_form); // Set initial visibility based on type
            empty_form.querySelector('.schedule-type').addEventListener('change', function() {
                updateScheduleFields(empty_form); // Update visibility based on type
            });
        });
    }

    // Handle delete buttons
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('delete-schedule')) {
            e.preventDefault(); // Prevent form submission
            const scheduleForm = e.target.closest('.schedule-form'); // Get the parent form
            scheduleForm.style.display = 'none'; // Hide the form instead of removing it
            const deleteInput = scheduleForm.querySelector('input[name$="-DELETE"]'); // Find the delete input field
            if (deleteInput) { 
                deleteInput.value = 'on'; // Mark the form for deletion
            }
        }
    });
});