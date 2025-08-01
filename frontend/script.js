document.getElementById("uploadForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const fileInput = document.getElementById("audioFile");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select a file first.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  const statusDiv = document.getElementById("status");
  const resultDiv = document.getElementById("result");
  const transcriptEl = document.getElementById("transcript");
  const contractEl = document.getElementById("contractText");
  const downloadLink = document.getElementById("downloadLink");

  statusDiv.textContent = "Processing...";
  resultDiv.style.display = "none";

  try {
    const response = await fetch("http://127.0.0.1:8000/generate_contract/", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Failed to generate contract.");
    }

    const data = await response.json();
    console.log("✅ Backend response:", data);

    transcriptEl.textContent = data.transcript;
    contractEl.textContent = data.contract_text;

    // Make sure this matches what FastAPI returns (e.g., "contracts/...")
    downloadLink.href = `http://127.0.0.1:8000/${data.pdf_path}`;
    downloadLink.style.display = "inline-block";

    resultDiv.style.display = "block";
    statusDiv.textContent = "✅ Contract ready!";

  } catch (err) {
    console.error("❌ Error occurred:", err);
    statusDiv.textContent = "❌ Something went wrong.";
  }
});
