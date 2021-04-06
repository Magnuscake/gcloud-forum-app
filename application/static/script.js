document.addEventListener('DOMContentLoaded', () => {
  // Functionality for message flash close button
  (document.querySelectorAll('.notification .delete') || []).forEach(
    $delete => {
      const $notification = $delete.parentNode;

      $delete.addEventListener('click', () => {
        $notification.parentNode.removeChild($notification);
      });
    }
  );
  document.querySelectorAll('.button').forEach(btn =>
    btn.addEventListener('click', () => {
      btn.classList.add('is-loading');
    })
  );
});
