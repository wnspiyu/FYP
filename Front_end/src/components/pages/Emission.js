import React from 'react'
//import { Link } from 'react-router-dom'
import '../../App.css'
// import HomePage from './HomePage'

import ImageSlider from "./ImageSlider";
const Emission = () => {
  const slides = [
    { url: "http://localhost:3000/image-1.jpg", title: "beach" },
    { url: "http://localhost:3000/image-2.jpg", title: "boat" },
    { url: "http://localhost:3000/image-3.jpg", title: "forest" },
    { url: "http://localhost:3000/image-4.jpg", title: "city" },
    { url: "http://localhost:3000/image-5.jpg", title: "italy" },
  ];
  const containerStyles = {
    width: "500px",
    height: "280px",
    margin: "0 auto",
  };
  return (
    <div className='center' style={{backgroundColor: "#E6E6FA" }}>
        <div className="emission-container">
            <div>
                <br></br>
                <center><h1>Reducing Emissions in Your Factory: Effective Strategies for Sustainability</h1></center>
                <br></br><br></br>
            </div>
            <div style={containerStyles}>
                <ImageSlider slides={slides} parentWidth={500} />
            </div>
            <div>
                <br></br><br></br>
                <center><h3>ENERGY EFFICIENCY IMPROVEMENTS </h3></center>
                        <p>Maximize emission reductions achieve substantial emission reductions by enhancing energy efficiency throughout your operations. Our experts recommend the following measures to optimize your energy consumption:</p><br></br>
                        <ul>
                            <li>Conduct comprehensive energy audits to identify areas for improvement and prioritize efficiency upgrades.</li>
                            <li>Upgrade your machinery and equipment to energy-efficient models that minimize power consumption without compromising productivity.</li>
                            <li>Illuminate your facilities with state-of-the-art LED lighting and motion sensors, ensuring optimized energy use and cost savings.</li>
                            <li>Reduce heat loss and energy requirements by implementing effective insulation strategies for your buildings.</li>
                            <li>Implement automated systems that intelligently control energy usage during non-operational hours, further reducing waste.</li>
                        </ul>
                <center><h3>SUPPLY CHAIN OPTIMIZATION</h3></center>
                <p>Collaborative Emission Reduction Our website takes a holistic approach to emissions reduction by considering both scope 1 and 2 emissions. Additionally, we address scope 3 emissions, which include transportation and activities outside the factory. Collaborating with suppliers and logistics partners is crucial to optimize transportation and reduce emissions. Explore these approaches:</p><br></br>
                <ul>
                    <li>Consolidate shipments and adopt efficient logistics routes to minimize transportation distances, resulting in fewer emissions.</li>
                    <li>Encourage the use of low-emission vehicles or transition to electric vehicles (EVs) for transportation and delivery operations.</li>
                    <li>Implement sustainable packaging practices, such as utilizing recycled materials and actively reducing packaging waste, thereby minimizing the carbon footprint.</li>
                    <li>Sustainable Materials and Production: Champion Eco-Friendly Practices Our website prioritizes environmentally friendly materials and sustainable production processes.Consider the following strategies</li>
                        <ul>
                            <li>Choose organic, recycled, or responsibly sourced fibers and materials to reduce the environmental impact of your products.</li>
                            <li>Adopt waterless or low-water dyeing techniques that minimize water consumption and associated energy usage.</li>
                            <li>Implement lean manufacturing principles to optimize production efficiency and reduce waste generation.</li>
                            <li>Encourage circular economy practices by designing products that prioritize durability, repairability, and recyclability.</li>
                        </ul>
                </ul>
                <center><h3>Emission Offsetting</h3></center>
                <p>Achieve carbon neutrality for emissions that cannot be eliminated through direct reduction efforts, our website offers innovative solutions for carbon offsetting. Invest in carbon offset projects, such as reforestation initiatives, renewable energy projects, or waste management programs. These initiatives help balance out the remaining emissions, fostering a climate-neutral factory.</p><br></br>
            </div>
        </div>
    </div>
  );
};

export default Emission;


