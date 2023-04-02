import React, { useState } from 'react';

function App() {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };


  const handleUpload = () => {
    const reader = new FileReader();
    reader.readAsBinaryString(file);
    reader.onload = () => {
      const base64String = btoa(reader.result);
      fetch('http://localhost:3100/upload', {
        method: 'POST',
        body: JSON.stringify({ data: base64String }),
        headers: { 'Content-Type': 'application/json' },
      })
        .then((response) => response.json())
        .then((data) => console.log(data))
        .catch((error) => console.error(error));
    };
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
    </div>
  );
}

export default App;

/*
  const handleUpload = () => {
    const reader = new FileReader();
    reader.readAsArrayBuffer(file);
    reader.onload = () => {
      const base64String = btoa(
        String.fromCharCode.apply(null, new Uint8Array(reader.result))
      );
      fetch('http://localhost:3100/upload', {
        method: 'POST',
        body: JSON.stringify({ data: base64String }),
        headers: { 'Content-Type': 'application/json' },
      })
        .then((response) => response.json())
        .then((data) => console.log(data))
        .catch((error) => console.error(error));
    };
  };

  */