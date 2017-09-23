/* global Dropzone, getCookie */
{
  const ready = () => {
    const id = 'new_file_upload';
    // const uploadDiv = document.getElementById(id);
    // uploadDiv.addEventListener('mouseover', () => {
    //   document.getElementById(id).classList.add('hide');
    // });
    // uploadDiv.addEventListener('mouseout', () => {
    //   document.getElementById('bodyupload').classList.add('hide');
    // });

    // Not only files can be drag&dropped but also links, images...
    // We need to detect only files
    function containsFiles(e) {
      const t = e.dataTransfer.types;
      if (t) {
        if (t.length > 1 && t[0] === 'text/x-moz-url') {
          return false;
        }
        for (let i = 0; i < t.length; i += 1) {
          if (t[i] === 'Files') {
            return true;
          }
        }
      }
      return false;
    }
    let counter = 0;
    // let hide = function (e) { document.getElementById('bodyupload').classList.add('hide') }
    /* eslint-disable no-new */
    new Dropzone(document.getElementById(id), {
      url: '/_/files/upload', // Set the url
      // previewsContainer: "#previews", // Define the container to display the previews
      clickable: false, // Define the element that should be used as click trigger to select files.
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
      },
      drop: () => {
        counter = 0;
        // document.getElementById('bodyupload').classList.add('hide');
      },
      dragend: () => {
        // document.getElementById('bodyupload').classList.add('hide');
      },
      dragstart: () => {
        // document.getElementById('bodyupload').classList.add('hide');
      },
      dragenter: () => {
        // console.log(e.dataTransfer);
        // console.log(e);
        // console.log(e.dataTransfer.types);
        // counter += 1;
        // if (containsFiles(e)) {
        //   document.getElementById('bodyupload').classList.remove('hide');
        // }
      },
      dragover: (e) => {
        if (containsFiles(e)) {
          // document.getElementById('bodyupload').classList.remove('hide');
        }
      },
      dragleave: () => {
        counter -= 1;
        if (counter === 0) {
          document.getElementById('bodyupload').classList.add('hide');
        }
      },
      // uploadprogress: function(file, progress, bytesSent) {
      uploadprogress: (file, progress) => {
        let node;
        let ref;
        if (file.previewElement) {
          ref = file.previewElement.querySelectorAll('[data-dz-uploadprogress]');
          const results = [];
          for (let i = 0, len = ref.length; i < len; i += 1) {
            node = ref[i];
            if (node.nodeName === 'PROGRESS') {
              results.push(node.value = progress);
            } else {
              results.push(node.style.width = `${progress}%`);
            }
          }
          return results;
        }
        return null;
      },
      // addedfile: (file) => null,
      addedfile: () => null,
    });
  };
  if (document.readyState === 'complete' || document.readyState !== 'loading') {
    ready();
  } else {
    document.addEventListener('DOMContentLoaded', ready);
  }
}
