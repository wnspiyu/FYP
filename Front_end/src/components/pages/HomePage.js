import React, { useState } from 'react';
import '../../App.css'

import { Button, ButtonGroup } from '@chakra-ui/react'
import { Input } from '@chakra-ui/react'
import { Heading } from '@chakra-ui/react'

import {
  FormControl,
  FormLabel,
  FormErrorMessage,
  FormHelperText,
} from '@chakra-ui/react'
import {
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
} from '@chakra-ui/react'

function App() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isError, setIsError] = useState(false);
  const [district, setDistrict] = useState('');
  const [numBuildings, setNumBuildings] = useState(0);
  const [buildingDimensions, setBuildingDimensions] = useState([]);
  const [target, setTarget] = useState(0);
  const [responseData, setResponseData] = useState(null);
  const [responseData1, setResponseData1] = useState(null);

  const handleFileChange = (event) => {
    const newFiles = [...event.target.files];
    setFiles([...files, ...newFiles]);
  };

  const handleDistrictChange = (event) => {
    setDistrict(event.target.value);
  };
  //////////////////2///////////////////////
  const handleTarget = (event) => {
    setTarget(parseInt(event.target.value));
  };

  const handleNumBuildingsChange = (event) => {
    const numBuildings = parseInt(event.target.value);
    setNumBuildings(numBuildings);

    const buildingDims = [];
    for (let i = 0; i < numBuildings; i++) {
      buildingDims.push({ width: '', length: '' });
    }
    setBuildingDimensions(buildingDims);
  };

  const handleWidthChange = (event, index) => {
    const newBuildingDims = [...buildingDimensions];
    newBuildingDims[index].width = parseFloat(event.target.value);
    setBuildingDimensions(newBuildingDims);
  };

  const handleLengthChange = (event, index) => {
    const newBuildingDims = [...buildingDimensions];
    newBuildingDims[index].length = parseFloat(event.target.value);
    setBuildingDimensions(newBuildingDims);
  };

  const buildingInputs = [];

  for (let i = 0; i < numBuildings; i++) {
    buildingInputs.push(
      <div key={i}>
        <center><h5>Building {i + 1} dimensions:</h5></center>
        <FormControl>
          <FormLabel>Width (m):</FormLabel>
          <Input type="number" name="width" value={buildingDimensions[i].width} onChange={(event) => handleWidthChange(event, i)} />
          <br></br><br></br>
        </FormControl>
        <FormControl>
          <FormLabel>Length (m):</FormLabel>
          <Input type="number" name="length" value={buildingDimensions[i].length} onChange={(event) => handleLengthChange(event, i)} />
          <br></br><br></br><br></br>
        </FormControl>
      </div>
    );
  };
  const dimensionsArray = buildingDimensions.map(({ width, length }) => [width, length]);
  //////////////////////////////////2/////////////////////////////////////////////////////////////////////////

  const handleUpload = () => {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append('files', file);
    });
    if (files.length < 3) {
      setIsError(true);
    } else {
      setLoading(true);
      setIsError(false);
      fetch('http://localhost:3100/upload', {
        method: 'POST',
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          setResponseData(data);
          setLoading(false);
        })
        .catch((error) => console.error(error));
    }
  };

  ////////////////////////2/////////////////////////////
  const handleUpload1 = () => {
    const formData1 = new FormData();
    formData1.append('target', target);
    formData1.append('numBuildings', numBuildings);
    formData1.append('dimensionsArray', JSON.stringify(dimensionsArray));
    formData1.append('district', district);
    formData1.append('Total_EM', responseData.data.Total_EM);
    fetch('http://localhost:3100/optimize', {
      method: 'POST',
      body: formData1,
    })
      .then((response) => response.json())
      .then((data1) => {
        console.log(data1);
        setResponseData1(data1);

      })
      .catch((error) => console.error(error));
  };

  return (
    <div style={{backgroundColor: "white", height: "100vh"}}>


      <div className='center' style={{ padding: "20px", width: "70%" }}>
        <div className='card'>
          <form>

            <Heading pb={3} as='h2' size='xl'>Fill Your Industry Details</Heading>

            {isError ?
              <Alert status='error' mb={5}>
                <AlertIcon />
                <AlertTitle>Fill all files!</AlertTitle>
                <AlertDescription>You need to upload all three files to continue</AlertDescription>
              </Alert> : null}


            <FormControl pb={3}>
              <FormLabel style={{fontSize:"20px"}} htmlFor='email'>Electricity consumption</FormLabel>
              <input type="file" name="file1" onChange={handleFileChange} />
            </FormControl>

            <FormControl pb={3}>
              <FormLabel htmlFor='email'>Boiler consumption</FormLabel>
              <input type="file" name="file2" onChange={handleFileChange} />
            </FormControl>

            <FormControl>
              <FormLabel htmlFor='email'>Annual Diesel Consumption(l)</FormLabel>
              <input type="file" name="diesel" onChange={handleFileChange} />
            </FormControl>

            <Button isLoading={loading} style={{ float: "right" }} type="button" onClick={handleUpload} colorScheme='orange'>Submit</Button>
          </form>
        </div>
        <form>
          <div className="card">
            {responseData &&
              <>
                <center><h3>GHG Emission for Current System</h3></center>
                <center><p>Grid Emission: {responseData.data.Grid_EM}kgCO2e</p></center>
                <center><p>Diesel Emission: {responseData.data.diesel_emission}kgCO2e</p></center>
                <center><p>Boiler Emission: {responseData.data.Fuel_oil_EM}kgCO2e</p></center>
                <center><p>Total Emission: {responseData.data.Total_EM}kgCO2e</p></center><br></br>
                <center><p>We can help you to reduce your current onsite emission by using low carbon energy sources.Please set your emission target(kgCO2e)</p></center>
                <center><input type="text" name="target" onChange={handleTarget} /></center>
                <FormControl>
                  <FormLabel htmlFor='email'>Number of Buildings:</FormLabel>
                  <Input type="number" name="numBuildings" onChange={handleNumBuildingsChange} />
                </FormControl>
                <center>{buildingInputs}</center><br></br>
                <center><label>District:</label></center>
                <center><input type="text" name="district" onChange={handleDistrictChange} /></center><br></br>
                <center><button type="button" onClick={handleUpload1}>Optimize the Current System</button></center>
                <p></p><br></br>
                <p></p>
              </>
            }
          </div>
        </form>
        <form>
          <div className="card">
            {responseData1 &&
              <>
                <center><h5>Suggested System for Desired Emission Reduction</h5></center>
                {/* <center><p>No of panels:{responseData1.data.No_of_panels}</p></center> */}
                <center><p>DC capacity for solar PV: {responseData1.data1.DC_capacityforsolar}</p></center>
                {/* <center><p>Depth_of_discharge: {responseData1.data.Depth_of_discharge}</p></center> */}
                {/* <center><p>Annual Green Diesel Fuel Capacity: {responseData1.data.Annual_Green_Diesel_Fuel_Capacity}</p></center> */}
                {/* <center><p>Biomass Boiler Size:{responseData1.data.Biomass_Boiler_Size}</p></center> */}
                {/* <center><p>DC capacity for Solar PV:{responseData1.data.DC_capacity_for_Solar_PV}</p></center> */}
                <center><p>Battery Capacity:{responseData1.data1.Battery_Capacity}</p></center>
                <center><p>Annual_HVO fuel requirement:{responseData1.data1.Annual_HVO_fuel_requirement}</p></center>
                <center><p>Biomass Boiler Capacity:{responseData1.data1.Biomass_Boiler_Capacity}</p></center>
                <center><p></p></center>
                <center><h5>Solar System Sizing</h5></center>
                <center><p>PV system capacity:{responseData1.data1.PV_system_capacity}</p></center>
                <center><p>PV system generated energy:{responseData1.data1.PV_system_generated_energy}</p></center>
                <center><p>No. of solar panel:{responseData1.data1.No_of_solar_panel}</p></center>
                <center><p>No. of 100kW inverters:{responseData1.data1.No_of_100kW_inverters}</p></center>
                <center><p>No. of 60kW inverters:{responseData1.data1.No_of_60kW_inverters}</p></center>
                <center><p>Maximum number of panel for a string:{responseData1.data1.Maximum_number_of_panel_for_a_string}</p></center>
                <center><p>Minimum number of panel for a string:{responseData1.data1.Minimum_number_of_panel_for_a_string}</p></center>
                <center><p></p></center>
                <center><h5>BESS Sizing</h5></center>
                <center><p>BESS Voltage:{responseData1.data1.BESS_Voltage}</p></center>
                <center><p>No of batteries in Series per string:{responseData1.data1.No_of_batteries_in_Series_per_string}</p></center>
                <center><p>No of strings in parallel:{responseData1.data1.No_of_strings_in_parallel}</p></center>
                <center><p>Battery Bank Capacity:{responseData1.data1.Battery_Bank_Capacity}</p></center>
                <center><p></p></center>
                <center><h5>For Suggested System</h5></center>
                <center><p>Net Present Value:{responseData1.data1.NPV}</p></center>
                <center><p>New Emission:{responseData1.data1.New_Emission}</p></center>
                <center><p>Capital cost of the overall energy system:{responseData1.data1.Capital_cost_of_the_overall_energy_system}</p></center>
                <center><p>IRR of the overall energy system:{responseData1.data1.IRR_of_the_overall_energy_system}</p></center>
                <center><p>NPV of the overall energy system:{responseData1.data1.NPV_of_the_overall_energy_system}</p></center>
                <center><p>Payback Period of the overall energy system:{responseData1.data1.Payback_Period_of_the_overall_energy_system}</p></center>
              </>
            }
          </div>
        </form>
      </div>
    </div>
  );
}

export default App;


//onClick={handleClick}