// navigation side bar  
document.addEventListener("DOMContentLoaded", function () {
    const toggler = document.querySelector(".btn[data-bs-theme='dark']");
    const closeBtn = document.querySelector(".close-btn");
    const sidebar = document.querySelector("#sidebar");

    toggler.addEventListener("click", function () {
        sidebar.classList.toggle("collapsed");
    });

    closeBtn.addEventListener("click", function () {
        sidebar.classList.add("collapsed");
    });
});
// destination stored path
function storePath() {
    var input = document.getElementById("destination");
    var storedPath = document.getElementById("storedPath");
  
    if (input.value.trim() !== "") {
      storedPath.textContent = "Stored Destination Path: " + input.value;
      // You can store the input value in a variable, send it to a server, or use it in further operations
    } else {
      storedPath.textContent = "Please enter a valid destination path!";
    }
  }

//export table pdf
function exportToPDF() {
    const doc = new jsPDF();
    const tables = document.querySelectorAll('.dynamic-table');
    tables.forEach(table => {
      // Convert each table to PDF
      doc.autoTable({ html: table });
      // Add space between tables in the PDF
      doc.addPage();
    });
    // Save the PDF file
    doc.save("tables.pdf");
  }
  document.getElementById('fileInput').addEventListener('change', function () {
      var fileInput = document.getElementById('fileInput');
      var fileListContainer = document.getElementById('file-list');
      //var fileListContainer = document.getElementById('fileListContainer'); // Use the new container ID
      var uploadForm = document.getElementById('uploadForm');
      var uploadButton = document.getElementById('uploadButton');
      // Clear previous file list
      fileListContainer.innerHTML = '';

      for (var i = 0; i < fileInput.files.length; i++) {
          var fileName = fileInput.files[i].name;

          var listItem = document.createElement('div');
          //listItem.classList.add("file-info-container");
          //listItem.className = 'd-flex justify-content-between align-items-center mb-2';

          // Add BODS text
          var bodsText = document.createElement('span');
          bodsText.textContent = 'BODS';
          bodsText.style.marginRight = '100px'; // Add right margin for spacing
          listItem.appendChild(bodsText);

          // Add fileName
          var fileNameElement = document.createElement('span');
          fileNameElement.textContent = fileName;
          fileNameElement.style.marginRight = '100px';
          listItem.appendChild(fileNameElement);

          // Add file size
          var fileSizeElement = document.createElement('span');
          var fileSize = formatFileSize(fileInput.files[i].size);
          fileSizeElement.textContent = fileSize;
          fileSizeElement.style.marginRight = '100px';
          listItem.appendChild(fileSizeElement);

          // Remove icon
          // var removeIcon = document.createElement('i');
          // removeIcon.className = 'bi bi-x cursor-pointer';
          // removeIcon.setAttribute('data-index', i);
          // removeIcon.addEventListener('click', function (e) {
          //     var index = e.target.getAttribute('data-index');
          //     fileListContainer.removeChild(fileListContainer.childNodes[index]);

          //     var filesArray = Array.from(fileInput.files);
          //     filesArray.splice(index, 1);
          //     fileInput.files = new FileList(...filesArray);

          //     updateFileListDisplay();
          // });

          // Custom styles for the cross icon
          // removeIcon.style.color = 'black';
          // removeIcon.style.transition = 'color 0.3s';

          // Hover effect
          // removeIcon.addEventListener('mouseenter', createHoverEffect(removeIcon, 'red'));

          // Reset color on mouse leave
          // removeIcon.addEventListener('mouseleave', createHoverEffect(removeIcon, 'black'));

          // listItem.appendChild(removeIcon);

          fileListContainer.appendChild(listItem);
      }

      // Show the form if at least one file is uploaded
      if (fileInput.files.length > 0) {
          uploadForm.style.display = 'block';
          uploadButton.style.display = 'block';
      } else {
          uploadForm.style.display = 'none';
          uploadButton.style.display = 'none';
      }

      // Function to create a closure for the hover effect
      function createHoverEffect(icon, hoverColor) {
          return function () {
              icon.style.color = hoverColor;
          };
      }

      // Function to format file size in human-readable format
      function formatFileSize(size) {
          if (size === 0) return '0 Bytes';
          var units = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
          var i = parseInt(Math.floor(Math.log(size) / Math.log(1024)));
          return Math.round(size / Math.pow(1024, i), 2) + ' ' + units[i];
      }
  });

  // Change the text on the upload button to "Next"
  document.getElementById('uploadButton').value = 'Next';

  function redirectToNextPage() {
      // For now, simply redirecting to another page
      window.location.href = "complexity.html";
      return false; // Prevents the form from submitting
  }
