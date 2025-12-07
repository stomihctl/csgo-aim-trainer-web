const requestForm = document.getElementById('request-reset-form');
  const resetForm = document.getElementById('reset-password-form');
  const messageBox = document.getElementById('message');
  const requestError = document.getElementById('request-error');
  const resetError = document.getElementById('reset-error');
  const backToLogin = document.getElementById('back-to-login');

  // Simulate email sending and showing reset form
  requestForm.addEventListener('submit', e => {
    e.preventDefault();
    requestError.classList.add('hidden');
    const email = requestForm.email.value.trim();

    if (!validateEmail(email)) {
      requestError.textContent = 'Please enter a valid email address.';
      requestError.classList.remove('hidden');
      return;
    }

    // Simulate async email send
    messageBox.textContent = '';
    requestForm.querySelector('button').disabled = true;
    setTimeout(() => {
      requestForm.classList.add('hidden');
      messageBox.textContent = 'Reset link sent! Please check your email.';
      messageBox.classList.remove('hidden');
      resetForm.classList.remove('hidden');
      requestForm.querySelector('button').disabled = false;
    }, 1000);
  });

  // Validate and confirm new password
  resetForm.addEventListener('submit', e => {
    e.preventDefault();
    resetError.classList.add('hidden');

    const pw1 = resetForm['new-password'].value;
    const pw2 = resetForm['confirm-password'].value;

    if (pw1.length < 8) {
      resetError.textContent = 'Password must be at least 8 characters long.';
      resetError.classList.remove('hidden');
      return;
    }
    if (pw1 !== pw2) {
      resetError.textContent = 'Passwords do not match.';
      resetError.classList.remove('hidden');
      return;
    }

    resetForm.querySelector('button').disabled = true;

    // Simulate password update
    setTimeout(() => {
      resetForm.classList.add('hidden');
      messageBox.textContent = 'Password successfully reset! You can now log in with your new password.';
      resetForm.querySelector('button').disabled = false;
    }, 1000);
  });

  // Simple email format validation
  function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  // "Back to login" link (just a placeholder)
  backToLogin.addEventListener('click', () => {
    alert('Redirecting to login page...');
  });