const form = document.getElementById('attributes-form');
    const saveBtn = form.querySelector('button[type="submit"]');
    const cancelBtn = document.getElementById('btn-cancel');
    const expertiseSelect = document.getElementById('expertise');
    const availabilitySelect = document.getElementById('availability');
    const levelCheckboxes = form.querySelectorAll('input[name="levels"]');
    const message = document.getElementById('form-message');

    function validateForm() {
      const expertiseValid = expertiseSelect.value !== "";
      const availabilityValid = availabilitySelect.value !== "";
      const levelsChecked = Array.from(levelCheckboxes).some(cb => cb.checked);

      // Enable save button only if all required fields are filled and at least one level selected
      saveBtn.disabled = !(expertiseValid && availabilityValid && levelsChecked);
    }

    // Add event listeners to validate on change
    expertiseSelect.addEventListener('change', validateForm);
    availabilitySelect.addEventListener('change', validateForm);
    levelCheckboxes.forEach(cb => cb.addEventListener('change', validateForm));

    form.addEventListener('submit', e => {
      e.preventDefault();
      if (saveBtn.disabled) return;

      // Gather data
      const expertise = expertiseSelect.value;
      const availability = availabilitySelect.value;
      const levels = Array.from(levelCheckboxes)
        .filter(cb => cb.checked)
        .map(cb => cb.value);

      // Simulate saving to DB - in real app, do AJAX/fetch here
      console.log("Saving trainer attributes:", {expertise, availability, levels});

      message.textContent = "Your attributes have been saved successfully.";
      message.className = "message success";

      // Optionally reset or disable form
      form.reset();
      validateForm();
    });

    cancelBtn.addEventListener('click', () => {
      // Reset form and message, simulate "cancel" action
      form.reset();
      message.textContent = "You have canceled entering your attributes.";
      message.className = "message error";
      validateForm();
    });

    // Initial validation on page load
    validateForm();