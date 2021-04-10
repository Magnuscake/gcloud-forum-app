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

  const fileInput = document.querySelector('#file-upload input[type=file]');
  fileInput.onchange = () => {
    if (fileInput.files.length > 0) {
      const fileName = document.querySelector('#file-upload .file-name');
      fileName.textContent = fileInput.files[0].name;
    }
  };
});
