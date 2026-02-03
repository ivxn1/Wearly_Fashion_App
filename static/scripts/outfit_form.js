document.addEventListener('DOMContentLoaded', function() {
  const checkboxes = document.querySelectorAll('.garment-checkbox');
  const selectedCountEl = document.getElementById('selected-count');

  function updateSelectedCount() {
    const checkedCount = document.querySelectorAll('.garment-checkbox:checked').length;
    selectedCountEl.textContent = checkedCount;
  }

  checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function() {
      updateSelectedCount();

      // Add/remove selected class to card
      const card = this.closest('.garment-selection-card');
      if (this.checked) {
        card.classList.add('selected');
      } else {
        card.classList.remove('selected');
      }
    });

    // Initialize selected state on page load
    if (checkbox.checked) {
      checkbox.closest('.garment-selection-card').classList.add('selected');
    }
  });

  // Initialize count
  updateSelectedCount();
});
