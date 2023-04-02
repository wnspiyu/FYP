import React, { useState } from "react";
import "../../App.css";

function DataEntryForm() {
  const [formData, setFormData] = useState({
    electricityConsumption: null,
    dieselConsumption: null,
    furnaceOilConsumption: null,
    rooftopArea: "",
    boilerEfficency: "",
    hoursOfBoiler: "",
    phone: "",
  });

  const handleChange = (event) => {
    const name = event.target.name;
    const value =
      event.target.type === "file" ? event.target.files[0] : event.target.value;

    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    const formdata = new FormData();
    formdata.append('electricityConsumption', formData.electricityConsumption);
    formdata.append('dieselConsumption', formData.dieselConsumption);
    formdata.append(
      'furnaceOilConsumption',
      formData.furnaceOilConsumption
    );
    formdata.append('rooftopArea', formData.rooftopArea);
    formdata.append('boilerEfficency', formData.boilerEfficency);
    formdata.append('hoursOfBoiler', formData.hoursOfBoiler);
    formdata.append('phone', formData.phone);

    fetch("http://localhost:3100/upload", {
      method: "POST",
      body: formdata,
    })
      .then((response) => response.json())
      .then((data) => console.log(data))
      .catch((error) => console.error(error));
  };

  return (
    <form onSubmit={handleSubmit}>
      <h1>Please Fill the Below List!</h1>
      <label>
        Electricity Consumption:
        <input
          type="file"
          name="electricityConsumption"
          onChange={handleChange}
        />
      </label>
      <label>
        Diesel Consumption:
        <input type="file" name="dieselConsumption" onChange={handleChange} />
      </label>
      <label>
        Furnace Oil Consumption:
        <input
          type="file"
          name="furnaceOilConsumption"
          onChange={handleChange}
        />
      </label>
      <label>
        Available Rooftop Area for Solar $(m^2):
        <input
          type="text"
          name="rooftopArea"
          value={formData.rooftopArea}
          onChange={handleChange}
        />
      </label>
      <label>
        Boiler Efficency:
        <input
          type="text"
          name="boilerEfficency"
          value={formData.boilerEfficency}
          onChange={handleChange}
        />
      </label>
      <label>
        Hours of Boiler:
        <input
          type="text"
          name="hoursOfBoiler"
          value={formData.hoursOfBoiler}
          onChange={handleChange}
        />
      </label>
      <label>
        Phone:
        <input
          type="text"
          name="phone"
          value={formData.phone}
          onChange={handleChange}
        />
      </label>
      <button type="submit">Submit</button>
    </form>
  );
}

export default DataEntryForm;