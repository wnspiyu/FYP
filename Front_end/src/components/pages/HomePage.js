// import React, { useState } from "react";
// // //import { Link } from 'react-router-dom'
import '../../App.css'
// function DataEntryForm() {
//   const [formData, setFormData] = useState({
//     electricityConsumption: null,
//     dieselConsumption: null,
//     furnaceOilConsumption: null,
//     rooftopArea: "",
//     boilerEfficency: "",
//     hoursOfBoiler: "",
//     phone: "",
//   });

//   const handleChange = (event) => {
//     const name = event.target.name;
//     const value = event.target.type === "file" ? event.target.files[0] : event.target.value;

//     setFormData({
//       ...formData,
//       [name]: value,
//     });
//   };

//   const handleSubmit = (event) => {
//     event.preventDefault();

//     const formdata = new FormData();
//     formdata.append("electricityConsumption", formData.electricityConsumption);
//     formdata.append("dieselConsumption", formData.dieselConsumption);
//     formdata.append("furnaceOilConsumption", formData.furnaceOilConsumption);
//     formdata.append("rooftopArea", formData.rooftopArea);
//     formdata.append("boilerEfficency", formData.boilerEfficency);
//     formdata.append("hoursOfBoiler", formData.hoursOfBoiler);
//     formdata.append("phone", formData.phone);

//     fetch("http://localhost:3100/upload", {
//       method: "POST",
//       body: formdata,
//     })
//       .then((response) => response.json())
//       .then((data) => console.log(data))
//       .catch((error) => console.error(error));
//   };

//   return (
//     <form onSubmit={handleSubmit}>
//       <h1>Please Fill the Below List!</h1>
//       <label>
//         Electricity Consumption:
//         <input type="file" name="electricityConsumption" onChange={handleChange} />
//       </label>
//       <label>
//         Diesel Consumption:
//         <input type="file" name="dieselConsumption" onChange={handleChange} />
//       </label>
//       <label>
//         Furnace Oil Consumption:
//         <input type="file" name="furnaceOilConsumption" onChange={handleChange} />
//       </label>
//       <label>
//         Available Rooftop Area for Solar $(m^2):
//         <input type="text" name="rooftopArea" value={formData.rooftopArea} onChange={handleChange} />
//       </label>
//       <label>
//         Boiler Efficency:
//         <input type="text" name="boilerEfficency" value={formData.boilerEfficency} onChange={handleChange} />
//       </label>
//       <label>
//         Hours of Boiler:
//         <input type="text" name="hoursOfBoiler" value={formData.hoursOfBoiler} onChange={handleChange} />
//       </label>
//       <label>
//         Phone:
//         <input type="text" name="phone" value={formData.phone} onChange={handleChange} />
//       </label>
//       <button type="submit">Submit</button>
//     </form>
//   );
// }

// export default DataEntryForm;


///////////////////////////////////////////////////////////////



// import React, { useState } from "react";
// import "../../App.css";

// function DataEntryForm() {
//   const [formData, setFormData] = useState({
//     electricityConsumption: null,
//     dieselConsumption: null,
//     furnaceOilConsumption: null,
//     rooftopArea: "",
//     boilerEfficency: "",
//     hoursOfBoiler: "",
//     phone: "",
//   });

//   const handleChange = (event) => {
//     const name = event.target.name;
//     const value =
//       event.target.type === "file" ? event.target.files[0] : event.target.value;

//     setFormData({
//       ...formData,
//       [name]: value,
//     });
//   };

//   const handleSubmit = (event) => {
//     event.preventDefault();

//     const formdata = new FormData();
//     formdata.append('electricityConsumption', formData.electricityConsumption);
//     formdata.append('dieselConsumption', formData.dieselConsumption);
//     formdata.append(
//       'furnaceOilConsumption',
//       formData.furnaceOilConsumption
//     );
//     formdata.append('rooftopArea', formData.rooftopArea);
//     formdata.append('boilerEfficency', formData.boilerEfficency);
//     formdata.append('hoursOfBoiler', formData.hoursOfBoiler);
//     formdata.append('phone', formData.phone);

//     fetch("http://localhost:3100/upload", {
//       method: "POST",
//       body: formdata,
//     })
//       .then((response) => response.json())
//       .then((data) => console.log(data))
//       .catch((error) => console.error(error));
//   };

//   return (
//     <form onSubmit={handleSubmit}>
//       <h1>Please Fill the Below List!</h1>
//       <label>
//         Electricity Consumption:
//         <input
//           type="file"
//           name="electricityConsumption"
//           onChange={handleChange}
//         />
//       </label>
//       <label>
//         Diesel Consumption:
//         <input type="file" name="dieselConsumption" onChange={handleChange} />
//       </label>
//       <label>
//         Furnace Oil Consumption:
//         <input
//           type="file"
//           name="furnaceOilConsumption"
//           onChange={handleChange}
//         />
//       </label>
//       <label>
//         Available Rooftop Area for Solar $(m^2):
//         <input
//           type="text"
//           name="rooftopArea"
//           value={formData.rooftopArea}
//           onChange={handleChange}
//         />
//       </label>
//       <label>
//         Boiler Efficency:
//         <input
//           type="text"
//           name="boilerEfficency"
//           value={formData.boilerEfficency}
//           onChange={handleChange}
//         />
//       </label>
//       <label>
//         Hours of Boiler:
//         <input
//           type="text"
//           name="hoursOfBoiler"
//           value={formData.hoursOfBoiler}
//           onChange={handleChange}
//         />
//       </label>
//       <label>
//         Phone:
//         <input
//           type="text"
//           name="phone"
//           value={formData.phone}
//           onChange={handleChange}
//         />
//       </label>
//       <button type="submit">Submit</button>
//     </form>
//   );
// }

// export default DataEntryForm;
import React, { useState } from 'react';

function App() {
  const [files, setFiles] = useState([]);
  const [area, setArea] = useState(0);
  const [diesel, setDiesel] = useState(0);
  const [district, setDistrict] = useState('');

  const handleFileChange = (event) => {
    const newFiles = [...event.target.files];
    setFiles([...files, ...newFiles]);
  };

  const handleAreaChange = (event) => {
    setArea(parseInt(event.target.value));
  };

  const handleDieselChange = (event) => {
    setDiesel(parseInt(event.target.value));
  };

  const handleDistrictChange = (event) => {
    setDistrict(event.target.value);
  };

  const handleUpload = () => {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append('files', file);
    });
    formData.append('area', area);
    formData.append('diesel', diesel);
    formData.append('district', district);

    fetch('http://localhost:3100/upload', {
      method: 'POST',
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => console.log(data))
      .catch((error) => console.error(error));
  };

  return (
    <div>
      <form>
        <h1>Please Fill the Below List!</h1>
        <label>Electricity consumption:</label>
        <input type="file" name="file1" onChange={handleFileChange} />
        <label>Boiler consumption:</label>
        <input type="file" name="file2" onChange={handleFileChange} />
        <label>Levelized Cost:</label>
        <input type="file" name="file3" onChange={handleFileChange} />
        <label>Available Rooftop Area for Solar (m²):</label>
        <input type="number" name="area" onChange={handleAreaChange} />
        <label>Annual Diesel Consumption: </label>
        <input type="number" name="diesel" onChange={handleDieselChange} />
        <label>District:</label>
        <input type="text" name="district" onChange={handleDistrictChange} />
        <button type="button" onClick={handleUpload}>Submit</button>
      </form>
    </div>
  );
}

export default App;



