/**
 * Plan Entry Form - Outfit Card Selection JavaScript
 * Handles interactive outfit selection with visual feedback
 */

document.addEventListener('DOMContentLoaded', function() {
  const radioButtons = document.querySelectorAll('.outfit-radio-input');

  if (radioButtons.length === 0) {
    return;
  }

  /**
   * Handle radio button change events
   * Manages the selected state for outfit cards
   */
  radioButtons.forEach(radio => {
    radio.addEventListener('change', function() {
      // Remove selected class from all cards
      document.querySelectorAll('.outfit-selection-card').forEach(card => {
        card.classList.remove('selected');
      });

      // Add selected class to the parent card of checked radio
      if (this.checked) {
        const parentCard = this.closest('.outfit-selection-card');
        if (parentCard) {
          parentCard.classList.add('selected');
        }
      }
    });

    // Initialize selected state on page load
    if (radio.checked) {
      const parentCard = radio.closest('.outfit-selection-card');
      if (parentCard) {
        parentCard.classList.add('selected');
      }
    }
  });
});
