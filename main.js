// static/js/main.js
// document.getElementById('upload-form').addEventListener('submit', async (e) => {
//   e.preventDefault();
//   const input = document.getElementById('files');
//   if (!input.files.length) {
//     alert("Please upload at least one image");
//     return;
//   }

//   const formData = new FormData();
//   for (let i=0;i<input.files.length;i++) {
//     formData.append('files', input.files[i]);
//   }

//   // show loading
//   const btn = e.target.querySelector("button[type='submit']");
//   btn.disabled = true;
//   btn.textContent = "Predicting...";

//   const res = await fetch('/predict', {
//     method: 'POST',
//     body: formData
//   });

//   btn.disabled = false;
//   btn.textContent = "Predict & Speak";

//   if (!res.ok) {
//     const err = await res.json();
//     alert(err.error || "Prediction failed");
//     return;
//   }

//   const data = await res.json();
//   document.getElementById('results').style.display = 'block';
//   const predList = document.getElementById('pred-list');
//   predList.innerHTML = "";
//   data.predictions.forEach(p => {
//     const li = document.createElement('li');
//     li.className = 'list-group-item';
//     li.textContent = `${p.filename} → ${p.letter} (${p.confidence})`;
//     predList.appendChild(li);
//   });
//   document.getElementById('pred-text').textContent = data.text || "(none)";

//   if (data.audio_url) {
//     const audio = document.getElementById('audio-player');
//     audio.src = data.audio_url;
//     audio.style.display = 'block';
//     audio.play();
//   }
// });
////.////////////////.///////////
// document.addEventListener("DOMContentLoaded", function () {
//   const form = document.getElementById("upload-form");
//   const resultsDiv = document.getElementById("results");
//   const predList = document.getElementById("pred-list");
//   const predText = document.getElementById("pred-text");
//   const audioPlayer = document.getElementById("audio-player");

//   form.addEventListener("submit", async function (e) {
//     e.preventDefault();

//     const files = document.getElementById("files").files;
//     if (files.length === 0) {
//       alert("Please upload at least one Braille image.");
//       return;
//     }

//     // Prepare form data
//     const formData = new FormData();
//     for (let i = 0; i < files.length; i++) {
//       formData.append("files", files[i]);
//     }

//     // Show temporary feedback
//     predText.innerText = "🔄 Processing...";
//     resultsDiv.style.display = "block";
//     audioPlayer.style.display = "none";

//     try {
//       const response = await fetch("/predict", {
//         method: "POST",
//         body: formData,
//       });

//       if (!response.ok) throw new Error("Prediction request failed");

//       const data = await response.json();

//       // Show predicted letters
//       predList.innerHTML = "";
//       data.predictions.forEach((p) => {
//         const li = document.createElement("li");
//         li.className = "list-group-item";
//         li.textContent = `${p.filename} → ${p.letter}`;
//         predList.appendChild(li);
//       });

//       // Show combined text
//       predText.innerText = data.text || "No prediction";

//       // Play the generated speech
//       if (data.audio_url) {
//         audioPlayer.src = data.audio_url;
//         audioPlayer.style.display = "block";

//         // Try to auto-play
//         const playPromise = audioPlayer.play();
//         if (playPromise !== undefined) {
//           playPromise.catch(() => {
//             console.log("Autoplay blocked, click Play manually.");
//           });
//         }
//       }

//     } catch (error) {
//       console.error("Error:", error);
//       predText.innerText = "❌ Error during prediction.";
//     }
//   });
// });


document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("upload-form");
  const resultsDiv = document.getElementById("results");
  const predList = document.getElementById("pred-list");
  const predText = document.getElementById("pred-text");
  const audioPlayer = document.getElementById("audio-player");

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const files = document.getElementById("files").files;
    if (files.length === 0) {
      alert("Please upload at least one Braille image.");
      return;
    }

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append("files", files[i]);
    }

    predText.innerText = "🔄 Processing...";
    resultsDiv.style.display = "block";
    audioPlayer.style.display = "none";

    try {
      const response = await fetch("/predict", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Prediction request failed");

      const data = await response.json();

      // Show predicted letters in upload order
      predList.innerHTML = "";
      data.predictions.forEach((p) => {
        const li = document.createElement("li");
        li.className = "list-group-item";
        li.textContent = `${p.filename} → ${p.letter}`;
        predList.appendChild(li);
      });

      // Display both raw and corrected text
      const corrected = data.corrected_text || "";
      const raw = data.text || "";
      predText.innerHTML = `
        <strong>Raw:</strong> ${raw}<br>
        <strong>Corrected:</strong> ${corrected}
      `;

      // Play generated audio
      if (data.audio_url) {
        audioPlayer.src = data.audio_url;
        audioPlayer.style.display = "block";
        const playPromise = audioPlayer.play();
        if (playPromise !== undefined) {
          playPromise.catch(() =>
            console.log("Autoplay blocked; click play manually.")
          );
        }
      }
    } catch (error) {
      console.error("Error:", error);
      predText.innerText = "❌ Error during prediction.";
    }
  });
});
