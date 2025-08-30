document.getElementById("convertBtn").addEventListener("click", convert);
document.getElementById("openBtn").addEventListener("click", () => eel.open_output_folder() );

async function convert() {
  const status = document.getElementById("status");
  let fileInput = document.getElementById("fileInput");
  let format = document.getElementById("formatSelect").value;
  
  // Check if a file is selected
  if (fileInput.files.length === 0) {
    status.textContent = "Please choose a file.";
    return;
  }

  let file = fileInput.files[0];
  status.textContent = "Uploading and converting…";

  // Read file as Base64 and send to Python
  const reader = new FileReader();
  reader.onload = async () => {
    try {
      const base64Data = reader.result.split(",")[1]; // strip "data:*/*;base64,"
      const resp = await eel.upload_and_convert(file.name, base64Data, format)();

      if (resp.status === "success") {
        status.textContent = "✅ Saved: " + resp.path;
      } else {
        status.textContent = "❌ " + resp.message;
      }
    } catch (err) {
      status.textContent = "❌ " + err.toString();
    }
  };
  reader.readAsDataURL(file);
}
