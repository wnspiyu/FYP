import React, { Component } from "react";
import Fade from "react-reveal";

class About extends Component {
  render() {
    if (!this.props.data) return null;

    const name = this.props.data.name;
    const profilepic = "images/" + this.props.data.image;
    const step1 = this.props.data.step1;
    const step2 = this.props.data.step2;
    const step3 = this.props.data.step3;
    const step4 = this.props.data.step4;
    const step5 = this.props.data.step5;
    const bio = this.props.data.bio;
    // const street = this.props.data.address.street;
    // const city = this.props.data.address.city;
    // const state = this.props.data.address.state;
    // const zip = this.props.data.address.zip;
    // const phone = this.props.data.phone;
    // const email = this.props.data.email;
    // const resumeDownload = this.props.data.resumedownload;
    const electricity_templete=this.props.data.electricity_templete;
    const boiler_templete=this.props.data.boiler_templete;
    const diesel_templete=this.props.data.diesel_templete;
    

    return (
      <section id="about">
        <Fade duration={1000}>
          <div className="row">
            <div className="three columns">
              <img
                className="profile-pic"
                src={profilepic}
                alt="Nordic Giant Profile Pic"
              />
            </div>
            <div className="nine columns main-col">
              <h2>About the tool</h2>

              <p>{bio}</p>
              <br></br>
              <div className="row">
                <div className="columns contact-details">
                  <h3>USER INSTRUCTIONS</h3>
                  <p className="address">
                    <li>{step1}</li>
                    <li>{step2}</li>
                    <li>{step3}</li>
                    <li>{step4}</li>
                    <li>{step5}</li>
                    <a href="https://drive.google.com/file/d/1YhHDDb1olIG4TzCzeb-8_wKOJj5KVj_u/view?usp=sharing" target="_blank" rel="noopener noreferrer">Click here to read our assumptions</a>
                    <br></br><br></br>
                  </p>
                  
                </div>
                <div className="columns download">
                  <h3>DOWNLOAD REQUIRED TEMPLATES</h3>
                  <p>
                    <a href={electricity_templete} download className="button" target="_blank">
                      <i className="fa fa-download"></i>Electricity Consumption
                    </a>
                    <a href={boiler_templete} download className="button" target="_blank">
                      <i className="fa fa-download"></i>Boiler Consumption
                    </a>
                    <a href={diesel_templete} download className="button" target="_blank">
                      <i className="fa fa-download"></i>Diesel Consumption
                    </a>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </Fade>
      </section>
    );
  }
}

export default About;
