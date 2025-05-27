document.addEventListener('DOMContentLoaded', function () {
  const programField = document.getElementById('study_program_id');
  const yearField = document.getElementById('starting_year');
  const codeField = document.getElementById('code');

  function updateCode() {
    const programId = programField.value;
    const year = yearField.value;
    if (programId && year.length === 4) {
      const shortYear = year.slice(-2);
      codeField.value = `TAD-u-${programId}${shortYear}-x`;
    } else {
      codeField.value = '';
    }
  }

  programField.addEventListener('change', updateCode);
  yearField.addEventListener('input', updateCode);
  yearField.addEventListener('keydown', function (event) {
    if (event.key === "ArrowUp" || event.key === "ArrowDown") {
      setTimeout(updateCode, 0);
    }
  });
});
