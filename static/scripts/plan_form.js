/**
 * Plan Entry Form - Outfit Card Selection JavaScript
 * Handles interactive outfit selection with visual feedback
 */

document.addEventListener('DOMContentLoaded', function() {
  const radioButtons = document.querySelectorAll('.outfit-radio-input');

  if (radioButtons.length === 0) {
    return; // Exit if no outfit selection on this page
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

  /**
   * Optional: Add keyboard navigation support
   * Allows arrow key navigation between outfit cards
   */
  const outfitCards = document.querySelectorAll('.outfit-selection-card');

  outfitCards.forEach((card, index) => {
    const label = card.querySelector('.outfit-card-label');

    if (label) {
      label.addEventListener('keydown', function(e) {
        let targetIndex = index;

        // Arrow key navigation
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
          e.preventDefault();
          targetIndex = (index + 1) % outfitCards.length;
        } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
          e.preventDefault();
          targetIndex = (index - 1 + outfitCards.length) % outfitCards.length;
        } else if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          const radio = card.querySelector('.outfit-radio-input');
          if (radio) {
            radio.checked = true;
            radio.dispatchEvent(new Event('change'));
          }
          return;
        } else {
          return; // Don't handle other keys
        }

        // Focus the target card
        const targetLabel = outfitCards[targetIndex].querySelector('.outfit-card-label');
        if (targetLabel) {
          targetLabel.focus();
        }
      });

      // Make labels focusable
      label.setAttribute('tabindex', '0');
    }
  });
});
