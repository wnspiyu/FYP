import React, { Component } from "react";
import ParticlesBg from "particles-bg";
import Fade from "react-reveal";
import { Center } from "@chakra-ui/react";

class Header extends Component {
  render() {
    if (!this.props.data) return null;

    
 
    const name = this.props.data.name;
    const description = this.props.data.description;

    return (
      <header id="home">
        <ParticlesBg type="cobweb" bg={true} />

        <nav id="nav-wrap">

          <a className="mobile-btn" href="#nav-wrap" title="Show navigation">
            Show navigation
          </a>
          <a className="mobile-btn" href="#home" title="Hide navigation">
            Hide navigation
          </a>
          <Center>
            <ul id="nav" className="nav">
              <li className="current" >
                <a className="smoothscroll" href="#home">
                  Home
                </a>
              </li>

              <li>
                <a className="smoothscroll" href="#about">
                  About
                </a>
              </li>

              <li>
                <a className="smoothscroll" href="#contact">
                  Contact
                </a>
              </li>
            </ul>
          </Center>
        </nav>



        <div className="row banner">
          <div className="banner-text">
            <Fade bottom>
              <h1 className="responsive-headline">{name}</h1>
            </Fade>
            <Fade bottom duration={1200}>
              <h3>{description}.</h3>
            </Fade>
            <hr />
            <Fade bottom duration={2000}>
              <ul className="social">
                <a href="/login" className="button btn project-btn">
                  <i className="fa fa-sign-in"></i>Login
                </a>
                <a href="register" className="button btn github-btn">
                  <i className="fa fa-user"></i>Register
                </a>
              </ul>
            </Fade>
          </div>
        </div>

        <p className="scrolldown">
          <a className="smoothscroll" href="#about">
            <i className="icon-down-circle"></i>
          </a>
        </p>
      </header>
    );
  }
}

export default Header;
