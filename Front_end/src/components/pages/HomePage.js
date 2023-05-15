import React, { useState } from 'react';
import '../../App.css'
import { Bar } from 'react-chartjs-2';
import { Pie } from 'react-chartjs-2';
import  Chart  from 'chart.js/auto';
import { Button, ButtonGroup } from '@chakra-ui/react'
import { Input } from '@chakra-ui/react'
import { Heading } from '@chakra-ui/react'
//import BarChart from  './barchart';


import {
  FormControl,
  FormLabel,
  //FormErrorMessage,
  //FormHelperText,
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
  const [chartData, setChartData] = useState(null);
  const [chartData1, setChartData1] = useState(null);
  const [chartData2, setChartData2] = useState(null);
  const [chartData3, setChartData3] = useState(null);
  const [chartData4, setChartData4] = useState(null);
  const [chartData5, setChartData5] = useState(null);
  const [chartData6, setChartData6] = useState(null);

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
        <center><h5>Building {i + 1} Rooftop Dimensions:</h5></center>
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
    formData.append('numBuildings', numBuildings);
    formData.append('dimensionsArray', JSON.stringify(dimensionsArray));
    formData.append('district', district);
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
          // console.log(data.data);
          setChartData([data.data.Grid_EM, data.data.diesel_emission, data.data.Fuel_oil_EM]);
          setChartData1([data.data.Solar_EM_Red, data.data.BESS_EM_Red, data.data.GreenDiesel_EM_Red,data.data.Biomass_EM_Red]);
          setChartData4([data.data.monthly_sum_elec[0],data.data.monthly_sum_elec[1],data.data.monthly_sum_elec[2],data.data.monthly_sum_elec[3],data.data.monthly_sum_elec[4],data.data.monthly_sum_elec[5],data.data.monthly_sum_elec[6],data.data.monthly_sum_elec[7],data.data.monthly_sum_elec[8],data.data.monthly_sum_elec[9],data.data.monthly_sum_elec[10],data.data.monthly_sum_elec[11]]);
          
          setChartData5([data.data.diesel_cosump_data[0],data.data.diesel_cosump_data[1],data.data.diesel_cosump_data[2],data.data.diesel_cosump_data[3],data.data.diesel_cosump_data[4],data.data.diesel_cosump_data[5],data.data.diesel_cosump_data[6],data.data.diesel_cosump_data[7],data.data.diesel_cosump_data[8],data.data.diesel_cosump_data[9],data.data.diesel_cosump_data[10],data.data.diesel_cosump_data[11]]);
          
          setChartData6([data.data.monthly_sum_boiler[0],data.data.monthly_sum_boiler[1],data.data.monthly_sum_boiler[2],data.data.monthly_sum_boiler[3],data.data.monthly_sum_boiler[4],data.data.monthly_sum_boiler[5],data.data.monthly_sum_boiler[6],data.data.monthly_sum_boiler[7],data.data.monthly_sum_boiler[8],data.data.monthly_sum_boiler[9],data.data.monthly_sum_boiler[10],data.data.monthly_sum_boiler[11]])
          setLoading(false);
        })
        .catch((error) => console.error(error));
    }
  };
  ////////////////////////2/////////////////////////////
  const handleUpload1 = () => {
    const formData1 = new FormData();
    formData1.append('target', target);
    formData1.append('Total_EM', responseData.data.Total_EM);
    formData1.append('Grid_EM', responseData.data.Grid_EM);
    formData1.append('diesel_emission', responseData.data.diesel_emission);
    formData1.append('Fuel_oil_EM', responseData.data.Fuel_oil_EM);
    formData1.append('numBuildings', responseData.data.buildings);
    formData1.append('dimensionsArray',JSON.stringify(responseData.data.dimensions));
    formData1.append('district', responseData.data.district);
    setLoading(true);
    fetch('http://localhost:3100/optimize', {
      method: 'POST',
      body: formData1,
    })
      .then((response) => response.json())
      .then((data1) => {
        console.log(data1);
        setResponseData1(data1);
        setChartData2([data1.data1.Ea,data1.data1.Eb,data1.data1.Ec,data1.data1.Ed]);
        setChartData3([data1.data1.E_elec,data1.data1.E_DiG,data1.data1.E_Boi]);
        setLoading(false);

      })
      .catch((error) => console.error(error));
  };

  Chart.register({
    id: 'category',
    afterBuildTicks: function(chart) {
      chart.ticks = chart.data.labels;
      return;
    }
  });
  
  const data = {
    labels: ["Grid", "Diesel", "Boiler"],
    datasets: [
      {
        label: "Sales",
        data: chartData,
        backgroundColor: ["Red", "Blue", "Green"],
        borderWidth: 1,
      },
      {
        label: "Sales 2",
        data: chartData3,
        backgroundColor: ["Orange", "LightBlue", "LightGreen"],
        borderWidth: 1,
      },
    ],
  };
  
  const options = {
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            const value = context.parsed;
            const label = context.label;
            return `${label}: ${value}`;
          }
        }
      }
    }
  };

  Chart.register({
    id: 'category',
    afterBuildTicks: function(chart) {
        chart.ticks = chart.data.labels;
        return;
    }
  });

  const data1 = {
    labels: ["Grid", "Diesel", "Boiler"],
    datasets: [
      {
        label: "Sales",
        data: chartData,
        backgroundColor: ["Red", "Blue", "Green"],
        // borderColor: "white",
        borderWidth: 1,
      },
    ],
  };

  const options1 = {
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          usePointStyle: true,
          padding: 20,
          boxWidth: 10,
        },
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            const value = context.parsed;
            const total = context.dataset.data.reduce((acc, curr) => acc + curr, 0);
            const percentage = ((value / total) * 100).toFixed(2);
            return context.label + ': ' + percentage + '%';
          },
        },
      },
    },
  };

  Chart.register({
    id: 'category',
    afterBuildTicks: function(chart) {
        chart.ticks = chart.data.labels;
        return;
    }
  });

  const data2 = {
    labels: ["Solar EM Reduction", "Battery EM Reduction", "Green Diesel EM Reduction","Biomass EM Reduction"],
    datasets: [
      {
        label: "Sales",
        data: chartData1,
        backgroundColor: ["Red", "Blue", "Green","Yellow"],
        // borderColor: "white",
        borderWidth: 1,
      },
    ],
  };

  const options2 = {
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            const value = context.parsed;
            const label = context.label;
            return `${label}: ${value}`;
          }
        }
      }
    }
  };
  Chart.register({
    id: 'category',
    afterBuildTicks: function(chart) {
        chart.ticks = chart.data.labels;
        return;
    }
  });

  const data3 = {
    labels: ["Solar EM Reduction", "Battery EM Reduction", "Green Diesel EM Reduction","Biomass EM Reduction"],
    datasets: [
      {
        label: "Sales",
        data: chartData2,
        backgroundColor: ["Red", "Blue", "Green","Yellow"],
        // borderColor: "white",
        borderWidth: 1,
      },
    ],
  };

  const options3 = {
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            const value = context.parsed;
            const label = context.label;
            return `${label}: ${value}`;
          }
        }
      }
    }
  };
  Chart.register({
    id: 'category',
    afterBuildTicks: function(chart) {
        chart.ticks = chart.data.labels;
        return;
    }
  });

  const data4 = {
    labels: ["Grid", "Diesel", "Boiler"],
    datasets: [
      {
        label: "Sales",
        data: chartData3,
        backgroundColor: ["Red", "Blue", "Green"],
        // borderColor: "white",
        borderWidth: 1,
      },
    ],
  };

  const options4 = {
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          usePointStyle: true,
          padding: 20,
          boxWidth: 10,
        },
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            const value = context.parsed;
            const total = context.dataset.data.reduce((acc, curr) => acc + curr, 0);
            const percentage = ((value / total) * 100).toFixed(2);
            return context.label + ': ' + percentage + '%';
          },
        },
      },
    },
  };
  Chart.register({
    id: 'category',
    afterBuildTicks: function(chart) {
        chart.ticks = chart.data.labels;
        return;
    }
  });

  const data5 = {
    labels: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
    datasets: [
      {
        label: "Sales",
        data: chartData4,
        backgroundColor: ["Red", "Red", "Red","Red","Red", "Red", "Red","Red","Red", "Red", "Red","Red"],
        // borderColor: "white",
        borderWidth: 1,
      },
    ],
  };

  const options5 = {
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            const value = context.parsed;
            const label = context.label;
            return `${label}: ${value}`;
          }
        }
      }
    }
  };
  Chart.register({
    id: 'category',
    afterBuildTicks: function(chart) {
        chart.ticks = chart.data.labels;
        return;
    }
  });

  const data6 = {
    labels: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
    datasets: [
      {
        label: "Sales",
        data: chartData5,
        backgroundColor: ["Blue", "Blue", "Blue","Blue","Blue", "Blue", "Blue","Blue","Blue", "Blue", "Blue","Blue"],
        // borderColor: "white",
        borderWidth: 1,
      },
    ],
  };

  const options6 = {
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            const value = context.parsed;
            const label = context.label;
            return `${label}: ${value}`;
          }
        }
      }
    }
  };
  Chart.register({
    id: 'category',
    afterBuildTicks: function(chart) {
        chart.ticks = chart.data.labels;
        return;
    }
  });

  const data7 = {
    labels: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
    datasets: [
      {
        label: "Sales",
        data: chartData6,
        backgroundColor: ["Green", "Green", "Green","Green","Green", "Green", "Green","Green","Green", "Green", "Green","Green"],
        // borderColor: "white",
        borderWidth: 1,
      },
    ],
  };

  const options7 = {
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            const value = context.parsed;
            const label = context.label;
            return `${label}: ${value}`;
          }
        }
      }
    }
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
              <FormLabel style={{fontSize:"20px"}} htmlFor='email'>Annual Electricity consumption</FormLabel>
              <input type="file" name="file1" onChange={handleFileChange} />
            </FormControl>

            <FormControl pb={3}>
              <FormLabel style={{fontSize:"20px"}} htmlFor='email'>Annual Boiler consumption</FormLabel>
              <input type="file" name="file2" onChange={handleFileChange} />
            </FormControl>

            <FormControl>
              <FormLabel style={{fontSize:"20px"}} htmlFor='email'>Annual Diesel Consumption</FormLabel>
              <input type="file" name="diesel" onChange={handleFileChange} />
            </FormControl>
            <FormControl>
              <FormLabel style={{fontSize:"15px"}} htmlFor='email'>Number of Buildings:</FormLabel>
              <Input type="number" name="numBuildings" onChange={handleNumBuildingsChange} />
              <center>{buildingInputs}</center><br></br>
            </FormControl>
            <center><label>District:</label></center>
                <center><input type="text" name="district" onChange={handleDistrictChange} /></center>

            <Button isLoading={loading} style={{ float: "right",minWidth: "100px", height: "40px", fontSize: "16px" }} type="button" onClick={handleUpload} colorScheme='orange'>Submit</Button>
          </form>
        </div>
        <form>
          <div className="card">
            {responseData &&
              <>
                <center><h2>GHG Emission for the Current System</h2></center>
                <center><p>Grid Emission: {responseData.data.Grid_EM}kgCO2e</p></center>
                <center><p>Diesel Emission: {responseData.data.diesel_emission}kgCO2e</p></center>
                <center><p>Boiler Emission: {responseData.data.Fuel_oil_EM}kgCO2e</p></center>
                <center><p>Total Emission: {responseData.data.Total_EM}kgCO2e</p></center><br></br>
                <div style={{ display: "flex", justifyContent: "center" }}>
                  <div style={{ width: "30%" }}>
                    <Pie data={data1} options={options1} />
                  </div>
                </div>
                <center><h2>EMISSION FROM IMPORTED ELECTRICITY.</h2></center>
                <div style={{ display: "flex", justifyContent: "center" }}>
                  <div style={{ width: "60%" }}>
                    <Bar data={data5} options={options5} />
                  </div>
                </div>
                <center><h2>EMISSION FROM BOILER.</h2></center>
                <div style={{ display: "flex", justifyContent: "center" }}>
                  <div style={{ width: "60%" }}>
                    <Bar data={data7} options={options7} />
                  </div>
                </div>
                <center><h2>EMISSION FROM Diesel.</h2></center>
                <div style={{ display: "flex", justifyContent: "center" }}>
                  <div style={{ width: "60%" }}>
                    <Bar data={data6} options={options6} />
                  </div>
                </div>
                {/* <center><p>Total buildings: {responseData.data.buildings}</p></center><br></br>
                <center><p>Total dimensions: {JSON.stringify(responseData.data.dimensions)}</p></center><br></br>
                <center><p>district: {responseData.data.district}</p></center><br></br> */}
                <center><h2>Maximum Emision Reduction from the Alternatives</h2></center>
                <center><p>Maximum Emission Reduction from Solar: {responseData.data.Solar_EM_Red}kgCO2e</p></center>
                <center><p>Maximum Emission Reduction from Battery: {responseData.data.BESS_EM_Red}kgCO2e</p></center>
                <center><p>Maximum Emission Reduction from Green Diesel:{responseData.data.GreenDiesel_EM_Red}kgCO2e</p></center>
                <center><p>Maximum Emission Reduction from Biomass boiler: {responseData.data.Biomass_EM_Red}kgCO2e</p></center>
                <center><p>Maximum Total Emission Reduction: {responseData.data.Total_max_EM_Red}kgCO2e</p></center><br></br>
                <div style={{ display: "flex", justifyContent: "center" }}>
                  <div style={{ width: "60%" }}>
                    <Bar data={data2} options={options2} />
                  </div>
                </div>
                
                <center><p>We can help you to reduce your current onsite emission by using low carbon energy sources.We use only SOLAR PV,BATTERY PACK,GREEN DIESEL and BIOMASS,Please set your emission target more than {responseData.data.Remaining}(kgCO2e)</p></center>
                <center><input type="text" name="target" onChange={handleTarget} /></center>
                
                
                
                <center><Button isLoading={loading} style={{ float: "right",minWidth: "100px", height: "40px", fontSize: "16px" }} type="button" onClick={handleUpload1} colorScheme='orange'>Optimize the Current System</Button></center>
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
                {/* <center><p>roof_sizes:{responseData1.data1.roof_sizes}</p></center><br></br>
                <center><p>target:{responseData1.data1.target}</p></center><br></br>
                <center><p>district:{responseData1.data1.district}</p></center><br></br>
                <center><p>Total_EM:{responseData1.data1.Total_EM}</p></center> */}
                {/* <center><p>No of panels:{responseData1.data.No_of_panels}</p></center> */}



                <center><p>DC capacity for solar PV: {responseData1.data1.DC_capacityforsolar}</p></center>




                {/* <center><p>Depth_of_discharge: {responseData1.data.Depth_of_discharge}</p></center> */}
                {/* <center><p>Annual Green Diesel Fuel Capacity: {responseData1.data.Annual_Green_Diesel_Fuel_Capacity}</p></center> */}
                {/* <center><p>Biomass Boiler Size:{responseData1.data.Biomass_Boiler_Size}</p></center> */}
                {/* <center><p>DC capacity for Solar PV:{responseData1.data.DC_capacity_for_Solar_PV}</p></center> */}




                <center><p>Battery Capacity:{responseData1.data1.Battery_Capacity}</p></center>
                <center><p>Annual_HVO fuel requirement:{responseData1.data1.Annual_HVO_fuel_requirement}</p></center>
                <center><p>Biomass Boiler Capacity:{responseData1.data1.Biomass_Boiler_Capacity}</p></center>
                <center><p></p></center><br></br>
                <center><h5>Solar System Sizing</h5></center>
                <center><p>PV system capacity:{responseData1.data1.PV_system_capacity}</p></center>
                <center><p>PV system generated energy:{responseData1.data1.PV_system_generated_energy}</p></center>
                <center><p>No. of solar panel:{responseData1.data1.No_of_solar_panel}</p></center>
                <center><p>No. of 100kW inverters:{responseData1.data1.No_of_100kW_inverters}</p></center>
                <center><p>No. of 60kW inverters:{responseData1.data1.No_of_60kW_inverters}</p></center>
                <center><p>Maximum number of panel for a string:{responseData1.data1.Maximum_number_of_panel_for_a_string}</p></center>
                <center><p>Minimum number of panel for a string:{responseData1.data1.Minimum_number_of_panel_for_a_string}</p></center>
                <center><p></p></center><br></br>
                <center><h5>BESS Sizing</h5></center>
                <center><p>BESS Voltage:{responseData1.data1.BESS_Voltage}</p></center>
                <center><p>No of batteries in Series per string:{responseData1.data1.No_of_batteries_in_Series_per_string}</p></center>
                <center><p>No of strings in parallel:{responseData1.data1.No_of_strings_in_parallel}</p></center>
                <center><p>Battery Bank Capacity:{responseData1.data1.Battery_Bank_Capacity}</p></center>
                <center><p></p></center><br></br>
                <center><h5>For the Suggested System</h5></center>
                <center><p>Net Present Value:{responseData1.data1.NPV}</p></center>
                <center><p>New Emission:{responseData1.data1.New_Emission}</p></center>
                <center><p>Capital cost of the overall energy system:{responseData1.data1.Capital_cost_of_the_overall_energy_system}</p></center>
                <center><p>IRR of the overall energy system:{responseData1.data1.IRR_of_the_overall_energy_system}</p></center>
                <center><p>NPV of the overall energy system:{responseData1.data1.NPV_of_the_overall_energy_system}</p></center>
                <center><p>Payback Period of the overall energy system:{responseData1.data1.Payback_Period_of_the_overall_energy_system}</p></center>
                <center><h5>GHG EMISSION REDUCTION FROM EACH FUEL TYPE IN THE SUGGESTED SYSTEM.</h5></center>
                <div style={{ display: "flex", justifyContent: "center" }}>
                  <div style={{ width: "60%" }}>
                    <Bar data={data3} options={options3} />
                  </div>
                </div>
                <center><h5>GHG EMISSION FOR THE SURRESTED SYSTEM.</h5></center>
                <center><p>Grid Emission: {responseData1.data1.E_elec}kgCO2e</p></center>
                <center><p>Diesel Emission: {responseData1.data1.E_DiG}kgCO2e</p></center>
                <center><p>Boiler Emission: {responseData1.data1.E_Boi}kgCO2e</p></center>
                <center><p>Total Emission: {responseData1.data1.E_Total}kgCO2e</p></center><br></br>
                <div style={{ display: "flex", justifyContent: "center" }}>
                  <div style={{ width: "30%" }}>
                    <Pie data={data4} options={options4} />
                  </div>
                </div>
                <center><h5>GHG EMISSION COMPARISION BETWEEN THE CURRENT AND THE SUGGESTED SYSTEM.</h5></center>
                <div style={{ display: "flex", justifyContent: "center" }}>
                  <div style={{ width: "60%" }}>
                    <Bar data={data} options={options} />
                  </div>
                </div>
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