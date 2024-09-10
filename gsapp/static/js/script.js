document.addEventListener('DOMContentLoaded', function () {
  // Function to get the CSRF token from the meta tag
  function getCsrfToken() {
      const csrfTokenMeta = document.querySelector('meta[name="csrf-token"]');
      return csrfTokenMeta ? csrfTokenMeta.getAttribute('content') : null;
  }

  const csrfToken = getCsrfToken();

  // Log the CSRF token to verify it's being fetched correctly
  console.log('CSRF Token:', csrfToken);

  if (!csrfToken) {
      console.error('CSRF token not found. Ensure the CSRF token meta tag is present in your HTML.');
      alert('CSRF token not found. Form submission has been blocked.');
      return;
  }

  // Hamburger menu handling
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.querySelector('.nav-links');
  hamburger.addEventListener('click',   
function () {
      navLinks.classList.toggle('active');   

  });

  // Data fetching and form submission
  const districtDropdown = document.getElementById('district-dropdown');
  const localAreaDropdown = document.getElementById('local-area-dropdown');
  const servicesDropdown = document.getElementById('services-dropdown');
  const form = document.getElementById('service-form');
  const nameInput = document.getElementById('name');
  const phoneInput = document.getElementById('phone');
  const errorMessages = document.getElementById('error-messages');

  // Fetch districts data
  fetch('/api/districts/')
      .then(response => response.json())
      .then(data => {
          data.forEach(district => {
              const option = createOption(district.district_id, district.district_name);
              districtDropdown.appendChild(option);
          });
      })
      .catch(error => console.error('Error fetching districts:', error));

  // Fetch local areas data based on selected district
  districtDropdown.addEventListener('change', function () {
      const selectedDistrict = this.value;
      fetchLocalAreas(selectedDistrict)
          .then(data => {
              localAreaDropdown.innerHTML = '<option value="">Select Local Area</option>';
              data.forEach(localArea => {
                  const option = createOption(localArea.local_area_id, localArea.local_area_name);
                  localAreaDropdown.appendChild(option);
              });
          })
          .catch(error => console.error('Error fetching local areas:', error));
  });

  // Fetch services data
  fetch('/api/services/')
      .then(response => response.json())
      .then(data => {
          data.forEach(service => {
              const option = createOption(service.service_id, service.service_name);
              servicesDropdown.appendChild(option);
          });
      })
      .catch(error => console.error('Error fetching services:', error));

  // Form submission code
  form.addEventListener('submit', function (event) {
      event.preventDefault();
      console.log('Form submitted');

      const formData = new FormData(form);   

      const data = Object.fromEntries(formData.entries());
      console.log('Data to be sent:', data);

      // Reset error messages and styles
      errorMessages.innerHTML = '';
      form.querySelectorAll('select, input').forEach(field => {
          field.classList.remove('error');
      });

      // Validation checks
      let hasErrors = false;

      function validateField(input, errorMessage) {
          if (input.value.trim() === '') {
              const errorSpan = document.createElement('span');
              errorSpan.textContent = errorMessage;
              errorSpan.style.color = 'red';
              errorSpan.style.fontSize = '12px';
              input.parentNode.appendChild(errorSpan);
              input.classList.add('error');
              return false;
          } else {
              const errorSpan = input.parentNode.querySelector('span');
              if (errorSpan) {
                  errorSpan.remove();
              }
              input.classList.remove('error');
              return true;
          }
      }

      // Name validation
      if (!validateField(nameInput, 'Please enter your name')) {
          hasErrors = true;
      }

      // Phone number validation
      if (!validateField(phoneInput, 'Phone number must be exactly 10 digits') || phoneInput.value.trim().length !== 10) {
          hasErrors = true;
      }

      // District validation
      if (districtDropdown.value === '') {
          validateField(districtDropdown, 'Please select a district');
          hasErrors = true;
      }

      // Local Area validation
      if (localAreaDropdown.value === '') {
          validateField(localAreaDropdown, 'Please select a local area');
          hasErrors = true;
      }

      // Services validation
      if (servicesDropdown.value === '') {
          validateField(servicesDropdown, 'Please select a service');
          hasErrors = true;
      }

      if (hasErrors) {
          return;
      }

      // Log CSRF token and headers before the fetch call
      console.log('CSRF Token before fetch:', csrfToken);
      console.log('Headers before fetch:', {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
      });

      fetch('/api/submit-lead/', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken,  // Add CSRF token to headers
          },
          body: JSON.stringify(data),
      })
          .then(response => {
              if (!response.ok) {
                  // If the response is not ok, log the entire response object for debugging
                  console.error('Response not ok:', response);
                  throw new Error(`Network response was not ok: ${response.statusText}`);
              }
              return response.json();
          })
          .then(data => {
              console.log('Success:', data);   


              window.location.href = '/success';  // Redirect to the success page
          })
          .catch(error => {
              console.error('Error:', error);
              alert('An error occurred. Please try again.');
          });
  });

  // Utility functions
  function createOption(value, text) {
      const option = document.createElement('option');
      option.value = value;
      option.text = text;
      return option;
  }

  function   
fetchLocalAreas(districtId) {
      return fetch(`/api/local-areas/${districtId}/`)
          .then(response => response.json())
          .catch(error => console.error('Error fetching local areas:', error));
  }
});